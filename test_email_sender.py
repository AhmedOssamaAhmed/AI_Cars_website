import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import tempfile
from email_sender import EmailSender
from config import GMAIL_USER, GMAIL_PASSWORD


class TestEmailSender(unittest.TestCase):
    """Test cases for EmailSender class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.email_sender = EmailSender()
        self.sample_car_info = {
            "car": {
                "body_type": "sedan",
                "color": "Blue",
                "brand": "Ford",
                "model": "Fusion",
                "manufactured_year": 2015,
                "motor_size_cc": 2000,
                "tires": {
                    "type": "brand-new",
                    "manufactured_year": 2022
                },
                "windows": "tinted",
                "notices": [
                    {
                        "type": "collision",
                        "description": "The rear bumper has been replaced after a minor collision."
                    }
                ],
                "price": {
                    "amount": 1000000,
                    "currency": "L.E"
                }
            }
        }
        
        # Create a temporary image file for testing
        self.temp_image = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        self.temp_image.write(b'fake image data')
        self.temp_image.close()
        
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_image.name):
            os.unlink(self.temp_image.name)
    
    def test_init(self):
        """Test EmailSender initialization."""
        self.assertEqual(self.email_sender.smtp_server, "smtp.gmail.com")
        self.assertEqual(self.email_sender.smtp_port, 587)
        self.assertEqual(self.email_sender.sender_email, GMAIL_USER)
        self.assertEqual(self.email_sender.sender_password, GMAIL_PASSWORD)
    
    def test_validate_credentials_success(self):
        """Test credential validation with valid credentials."""
        with patch('streamlit.error') as mock_st_error:
            result = self.email_sender.validate_credentials()
            self.assertTrue(result)
            mock_st_error.assert_not_called()
    
    def test_validate_credentials_missing_email(self):
        """Test credential validation with missing email."""
        original_email = self.email_sender.sender_email
        self.email_sender.sender_email = "your-email@gmail.com"
        
        with patch('streamlit.error') as mock_st_error:
            result = self.email_sender.validate_credentials()
            self.assertFalse(result)
            mock_st_error.assert_called_once()
        
        self.email_sender.sender_email = original_email
    
    def test_validate_credentials_missing_password(self):
        """Test credential validation with missing password."""
        original_password = self.email_sender.sender_password
        self.email_sender.sender_password = "your-app-password"
        
        with patch('streamlit.error') as mock_st_error:
            result = self.email_sender.validate_credentials()
            self.assertFalse(result)
            mock_st_error.assert_called_once()
        
        self.email_sender.sender_password = original_password
    
    def test_create_email_content_with_user_email(self):
        """Test email content creation with user email."""
        user_email = "test@example.com"
        msg = self.email_sender.create_email_content(self.sample_car_info, self.temp_image.name, user_email)
        
        self.assertEqual(msg['To'], user_email)
        self.assertIn('🚗 Car Details - Ford Fusion', msg['Subject'])
        self.assertEqual(msg['From'], GMAIL_USER)
    
    def test_create_email_content_without_user_email(self):
        """Test email content creation without user email (uses default)."""
        msg = self.email_sender.create_email_content(self.sample_car_info, self.temp_image.name)
        
        self.assertEqual(msg['To'], self.email_sender.recipient_email)
        self.assertIn('🚗 Car Details - Ford Fusion', msg['Subject'])
        self.assertEqual(msg['From'], GMAIL_USER)
    
    def test_create_email_content_attachments(self):
        """Test that email content includes proper attachments."""
        msg = self.email_sender.create_email_content(self.sample_car_info, self.temp_image.name)
        
        # Check that we have HTML content
        html_parts = [part for part in msg.walk() if part.get_content_type() == 'text/html']
        self.assertTrue(len(html_parts) > 0)
        
        # Check that we have image attachment
        image_parts = [part for part in msg.walk() if part.get_content_type().startswith('image/')]
        self.assertTrue(len(image_parts) > 0)
        
        # Check that we have JSON attachment
        json_parts = [part for part in msg.walk() if part.get_content_maintype() == 'text' and part.get_filename().endswith('.json')]
        self.assertTrue(len(json_parts) > 0)
    
    def test_create_html_content(self):
        """Test HTML content creation."""
        html_content = self.email_sender._create_html_content(self.sample_car_info)
        
        # Check that HTML contains expected car information
        self.assertIn('Ford', html_content)
        self.assertIn('Fusion', html_content)
        self.assertIn('2015', html_content)
        self.assertIn('Blue', html_content)
        self.assertIn('sedan', html_content)
        self.assertIn('1000000', html_content)
        self.assertIn('L.E', html_content)
    
    def test_format_notices_html_with_notices(self):
        """Test notices formatting with actual notices."""
        notices = [
            {"type": "collision", "description": "Minor front bumper damage"},
            {"type": "maintenance", "description": "Oil change needed"}
        ]
        
        html = self.email_sender._format_notices_html(notices)
        self.assertIn('collision', html)
        self.assertIn('Minor front bumper damage', html)
        self.assertIn('maintenance', html)
        self.assertIn('Oil change needed', html)
    
    def test_format_notices_html_empty(self):
        """Test notices formatting with empty list."""
        html = self.email_sender._format_notices_html([])
        self.assertIn('No notices specified', html)
    
    def test_format_notices_html_none(self):
        """Test notices formatting with None."""
        html = self.email_sender._format_notices_html(None)
        self.assertIn('No notices specified', html)
    
    def test_create_json_content(self):
        """Test JSON content creation."""
        json_content = self.email_sender._create_json_content(self.sample_car_info)
        
        # Should be valid JSON
        import json
        parsed = json.loads(json_content)
        self.assertEqual(parsed['car']['brand'], 'Ford')
        self.assertEqual(parsed['car']['model'], 'Fusion')
    
    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test successful email sending."""
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        with patch('streamlit.success') as mock_st_success:
            result = self.email_sender.send_email(self.sample_car_info, self.temp_image.name)
            
            self.assertTrue(result)
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with(GMAIL_USER, GMAIL_PASSWORD)
            mock_server.send_message.assert_called_once()
            mock_st_success.assert_called_once_with("✅ Email sent successfully!")
    
    @patch('smtplib.SMTP')
    def test_send_email_authentication_error(self, mock_smtp):
        """Test email sending with authentication error."""
        # Mock SMTP server with authentication error
        mock_server = MagicMock()
        mock_server.login.side_effect = Exception("Authentication failed")
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        with patch('streamlit.error') as mock_st_error:
            result = self.email_sender.send_email(self.sample_car_info, self.temp_image.name)
            
            self.assertFalse(result)
            mock_st_error.assert_called()
    
    @patch('smtplib.SMTP')
    def test_send_email_smtp_error(self, mock_smtp):
        """Test email sending with SMTP error."""
        # Mock SMTP server with SMTP error
        mock_server = MagicMock()
        mock_server.send_message.side_effect = Exception("SMTP error")
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        with patch('streamlit.error') as mock_st_error:
            result = self.email_sender.send_email(self.sample_car_info, self.temp_image.name)
            
            self.assertFalse(result)
            mock_st_error.assert_called()
    
    def test_send_email_invalid_credentials(self):
        """Test email sending with invalid credentials."""
        # Temporarily set invalid credentials
        original_user = self.email_sender.sender_email
        original_password = self.email_sender.sender_password
        
        self.email_sender.sender_email = "your-email@gmail.com"
        self.email_sender.sender_password = "your-app-password"
        
        with patch('streamlit.error') as mock_st_error:
            result = self.email_sender.send_email(self.sample_car_info, self.temp_image.name)
            
            self.assertFalse(result)
            mock_st_error.assert_called()
        
        # Restore original credentials
        self.email_sender.sender_email = original_user
        self.email_sender.sender_password = original_password
    
    def test_send_email_with_user_email(self):
        """Test email sending with specific user email."""
        user_email = "user@example.com"
        
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            with patch('streamlit.success') as mock_st_success:
                result = self.email_sender.send_email(
                    self.sample_car_info, 
                    self.temp_image.name, 
                    user_email
                )
                
                self.assertTrue(result)
                mock_st_success.assert_called_once()
    
    def test_email_content_structure(self):
        """Test that email content has proper structure."""
        msg = self.email_sender.create_email_content(self.sample_car_info, self.temp_image.name)
        
        # Check required headers
        self.assertIn('Subject', msg)
        self.assertIn('From', msg)
        self.assertIn('To', msg)
        
        # Check content types
        content_types = [part.get_content_type() for part in msg.walk()]
        self.assertIn('text/html', content_types)
        self.assertIn('image/jpeg', content_types)  # Assuming jpg file
        self.assertIn('text/plain', content_types)  # JSON attachment


class TestEmailSenderIntegration(unittest.TestCase):
    """Integration tests for EmailSender with real configuration."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.email_sender = EmailSender()
        
    def test_config_loading(self):
        """Test that configuration is properly loaded."""
        # These should not be the placeholder values
        self.assertNotEqual(self.email_sender.sender_email, "your-email@gmail.com")
        self.assertNotEqual(self.email_sender.sender_password, "your-app-password")
        
        # Should have actual values
        self.assertTrue('@' in self.email_sender.sender_email)
        self.assertTrue(len(self.email_sender.sender_password) > 0)
    
    def test_credentials_validation(self):
        """Test that credentials are valid."""
        # This test will fail if credentials are not properly configured
        result = self.email_sender.validate_credentials()
        self.assertTrue(result, "Credentials validation failed. Check your .env file.")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
