import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
from typing import Dict, Any, Optional
import streamlit as st
from config import GMAIL_USER, GMAIL_PASSWORD, RECIPIENT_EMAIL

class EmailSender:
    """
    Handles sending car information and images via Gmail SMTP.
    """
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = GMAIL_USER
        self.sender_password = GMAIL_PASSWORD
        self.recipient_email = RECIPIENT_EMAIL
        
    def validate_credentials(self) -> bool:
        """
        Validates Gmail credentials before sending.
        
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        if not self.sender_email or self.sender_email == "your-email@gmail.com":
            st.error("❌ Please update Gmail credentials in config.py")
            return False
        
        if not self.sender_password or self.sender_password == "your-app-password":
            st.error("❌ Please update Gmail app password in config.py")
            return False
        
        return True
    
    def create_email_content(self, car_info: Dict[str, Any], image_path: str, user_email: str = None) -> MIMEMultipart:
        """
        Creates the email content with car information and image attachment.
        
        Args:
            car_info (Dict): Structured car information
            image_path (str): Path to the car image
            user_email (str): User's email address to send the details to
            
        Returns:
            MIMEMultipart: Email message object
        """
        # Create message container
        msg = MIMEMultipart('alternative')
        
        # Use user email if provided, otherwise use default recipient
        recipient = user_email if user_email else self.recipient_email
        
        car_data = car_info.get('car', {})
        msg['Subject'] = f"🚗 Car Details - {car_data.get('brand', 'Unknown')} {car_data.get('model', 'Unknown')}"
        msg['From'] = self.sender_email
        msg['To'] = recipient
        
        # Create HTML content
        html_content = self._create_html_content(car_info, user_email)
        msg.attach(MIMEText(html_content, 'html'))
        
        # Attach image
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as img_file:
                    img_data = img_file.read()
                    image = MIMEImage(img_data, name=os.path.basename(image_path))
                    msg.attach(image)
            except Exception as e:
                st.warning(f"⚠️ Could not attach image: {str(e)}")
        
        # Attach JSON data as text file
        json_content = self._create_json_content(car_info)
        json_attachment = MIMEText(json_content, 'plain')
        json_attachment.add_header('Content-Disposition', 'attachment', 
                                 filename=f"car_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        msg.attach(json_attachment)
        
        return msg
    
    def _create_html_content(self, car_info: Dict[str, Any], user_email: str = None) -> str:
        """
        Creates HTML email content for better presentation.
        
        Args:
            car_info (Dict): Car information dictionary
            
        Returns:
            str: HTML formatted email content
        """
        # Extract car data from the new structure
        car_data = car_info.get('car', {})
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; }}
                .car-info {{ margin: 20px 0; }}
                .field {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #333; }}
                .value {{ color: #666; }}
                .notice {{ background-color: #fff3cd; padding: 8px; margin: 5px 0; border-radius: 3px; border-left: 3px solid #ffc107; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🚗 Car Details</h2>
                <p><strong>Submission Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="car-info">
                <h3>Car Details</h3>
                
                <div class="field">
                    <span class="label">Brand:</span>
                    <span class="value">{car_data.get('brand', 'Not specified')}</span>
                </div>
                
                <div class="field">
                    <span class="label">Model:</span>
                    <span class="value">{car_data.get('model', 'Not specified')}</span>
                </div>
                
                <div class="field">
                    <span class="label">Year:</span>
                    <span class="value">{car_data.get('manufactured_year', 'Not specified')}</span>
                </div>
                
                <div class="field">
                    <span class="label">Body Type:</span>
                    <span class="value">{car_data.get('body_type', 'Not specified')}</span>
                </div>
                
                <div class="field">
                    <span class="label">Color:</span>
                    <span class="value">{car_data.get('color', 'Not specified')}</span>
                </div>
                
                <div class="field">
                    <span class="label">Engine Size:</span>
                    <span class="value">{car_data.get('motor_size_cc', 'Not specified')} cc</span>
                </div>
                
                <div class="field">
                    <span class="label">Price:</span>
                    <span class="value">{car_data.get('price', {}).get('amount', 'Not specified')} {car_data.get('price', {}).get('currency', '')}</span>
                </div>
                
                <div class="field">
                    <span class="label">Windows:</span>
                    <span class="value">{car_data.get('windows', 'Not specified')}</span>
                </div>
                
                <div class="field">
                    <span class="label">Tires:</span>
                    <span class="value">{car_data.get('tires', {}).get('type', 'Not specified')} ({car_data.get('tires', {}).get('manufactured_year', 'Not specified')})</span>
                </div>
                
                <div class="field">
                    <span class="label">Notices:</span>
                    <span class="value">{self._format_notices_html(car_data.get('notices', []))}</span>
                </div>
            </div>
            
            <hr>
            <p><em>This listing was automatically processed using AI-powered text extraction and image classification.</em></p>
        </body>
        </html>
        """
        return html
    
    def _format_notices_html(self, notices: list) -> str:
        """
        Formats notices list for HTML display.
        
        Args:
            notices (list): List of car notices/issues
            
        Returns:
            str: HTML formatted notices
        """
        if not notices:
            return '<span class="value">No notices specified</span>'
        
        if isinstance(notices, str):
            notices = [notices]
        
        notice_html = ""
        for notice in notices:
            if notice and isinstance(notice, dict):
                notice_type = notice.get('type', 'Unknown')
                description = notice.get('description', 'No description')
                notice_html += f'<div class="notice"><strong>{notice_type}:</strong> {description}</div>'
            elif notice and notice != "not specified":
                notice_html += f'<div class="notice">{notice}</div>'
        
        return notice_html if notice_html else '<span class="value">No notices specified</span>'
    
    def _create_json_content(self, car_info: Dict[str, Any]) -> str:
        """
        Creates JSON content for attachment.
        
        Args:
            car_info (Dict): Car information dictionary
            
        Returns:
            str: JSON formatted string
        """
        import json
        return json.dumps(car_info, indent=2, ensure_ascii=False)
    
    def send_email(self, car_info: Dict[str, Any], image_path: str, user_email: str = None) -> bool:
        """
        Sends the email with car information and image.
        
        Args:
            car_info (Dict): Structured car information
            image_path (str): Path to the car image
            user_email (str): User's email address to send the details to
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Validate credentials
            if not self.validate_credentials():
                return False
            
            # Create email content
            msg = self.create_email_content(car_info, image_path, user_email)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            st.success("✅ Email sent successfully!")
            return True
            
        except smtplib.SMTPAuthenticationError:
            st.error("❌ Gmail authentication failed. Please check your credentials.")
            return False
        except smtplib.SMTPException as e:
            st.error(f"❌ SMTP error: {str(e)}")
            return False
        except Exception as e:
            st.error(f"❌ Failed to send email: {str(e)}")
            return False
