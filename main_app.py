import streamlit as st
import os
import tempfile
from datetime import datetime
from PIL import Image
import json

# Import custom modules
from image_classifier import CarImageClassifier
from text_processor import TextProcessor
from email_sender import EmailSender
from config import MAX_IMAGE_SIZE, SUPPORTED_IMAGE_FORMATS, validate_credentials

# Page configuration
st.set_page_config(
    page_title="🚗 Car Selling Platform",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #333;
        font-weight: 500;
    }
    .info-box h4 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .info-box p {
        color: #2c3e50;
        margin: 0.3rem 0;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .info-box strong {
        color: #1a202c;
        font-weight: 600;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        color: #155724;
        font-weight: 500;
    }
    .success-box h4 {
        color: #0f5132;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .success-box p {
        color: #155724;
        margin: 0.3rem 0;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .success-box strong {
        color: #0f5132;
        font-weight: 600;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        color: #856404;
        font-weight: 500;
    }
    .warning-box h4 {
        color: #6c5204;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .warning-box p {
        color: #856404;
        margin: 0.3rem 0;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .warning-box strong {
        color: #6c5204;
        font-weight: 600;
    }
             .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2.5rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Validate credentials on startup
    try:
        validate_credentials()
    except ValueError as e:
        st.error(f"❌ Configuration Error: {str(e)}")
        st.info("📋 Please create a .env file with your credentials. See env_example.txt for reference.")
        st.stop()
    
    # Initialize session state
    if 'submission_time' not in st.session_state:
        st.session_state.submission_time = None
    if 'car_info' not in st.session_state:
        st.session_state.car_info = None
    if 'image_path' not in st.session_state:
        st.session_state.image_path = None
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Car Selling Platform</h1>
        <p>AI-Powered Car Listing with Image Classification & Text Processing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Application info
        st.subheader("ℹ️ About")
        st.info("""
        This platform uses:
        - **GPT-4o mini** for text processing
        - **AI Image Classification** for car type detection
        - **Gmail SMTP** for email delivery
        """)
        
        # Status indicators
        st.subheader("🔍 Status")
        st.success("✅ Gmail configured from .env file")
        st.success("✅ Azure OpenAI configured")
        st.success("✅ AI Image Model loaded")
        
        st.divider()
        
        # Setup instructions
        st.subheader("📋 Setup")
        st.info("""
        **Credentials** are configured in your `.env` file.
        
        Make sure to:
        1. Copy `env_example.txt` to `.env`
        2. Add your Gmail app password
        3. Add your Azure OpenAI API key
        4. Enable 2FA on Gmail
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Car Image")
        
        # Image upload
        uploaded_image = st.file_uploader(
            "Choose a car image",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Upload a clear image of the car (max 10MB)"
        )
        
        if uploaded_image is not None:
            # Display image
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Car Image", use_column_width=True)
            
            # Save image to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_image.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_image.getvalue())
                st.session_state.image_path = tmp_file.name
            
            # Image classification
            if st.button("🔍 Analyze Car Type", type="primary"):
                with st.spinner("Analyzing car image..."):
                    classifier = CarImageClassifier()
                    classification_result = classifier.classify_car_type(st.session_state.image_path)
                    
                    if classification_result['status'] == 'success':
                        st.session_state.car_type = classification_result['car_type']
                        st.session_state.classification_confidence = classification_result['confidence']
                        
                        st.success(f"🎯 **Car Type Detected:** {classification_result['car_type']}")
                        st.info(f"**Confidence:** {classification_result['confidence']:.1%}")
                    else:
                        st.error("❌ Image analysis failed")
    
    with col2:
        st.header("📝 Car Description & Contact")
        
        # User email input
        user_email = st.text_input(
            "Your Email Address",
            placeholder="Enter your email to receive the car details",
            help="We'll send the processed car information to this email"
        )
        
        # Text input
        car_description = st.text_area(
            "Describe the car",
            height=150,
            placeholder="Enter detailed description including: brand, model, year, color, engine size, price, condition, any issues, etc.",
            help="Provide comprehensive details about the car"
        )
        
        # Process description button
        if st.button("🧠 Process Description", type="primary") and car_description:
            if 'car_type' not in st.session_state:
                st.warning("⚠️ Please analyze the car image first to detect car type")
            elif not user_email or '@' not in user_email:
                st.warning("⚠️ Please enter a valid email address")
            else:
                with st.spinner("Processing description with AI..."):
                    processor = TextProcessor()
                    car_info = processor.extract_car_info(car_description, st.session_state.car_type)
                    
                    if car_info:
                        st.session_state.car_info = car_info
                        st.session_state.user_email = user_email
                        st.session_state.submission_time = datetime.now()
                        
                        # Display extracted information
                        st.success("✅ Information extracted successfully!")
                        
                        # st.json(car_info)
                        st.text(json.dumps(car_info, indent=4, ensure_ascii=False))
                    else:
                        st.error("❌ Failed to extract car information")
    
    # Submission section
    if st.session_state.car_info and st.session_state.image_path:
        st.divider()
        
        col3, col4, col5 = st.columns([1, 2, 1])
        
        with col4:
            st.header("📤 Submit Car Listing")
            
            # Display summary
            car_data = st.session_state.car_info.get('car', {})
            
            # Get confidence with fallback
            confidence = getattr(st.session_state, 'classification_confidence', 0.0)
            confidence_display = f"{confidence:.1%}" if confidence > 0 else "Not available"
            

            
            st.markdown("""
            <div class="info-box">
                <h4>📋 Submission Summary</h4>
                <p><strong>Car:</strong> {brand} {model} ({year})</p>
                <p><strong>Type:</strong> {body_type} (Confidence: {confidence})</p>
                <p><strong>Price:</strong> {price} {currency}</p>
                <p><strong>Send to:</strong> {user_email}</p>
                <p><strong>Status:</strong> Ready to submit</p>
            </div>
            """.format(
                brand=car_data.get('brand', 'Unknown'),
                model=car_data.get('model', 'Unknown'),
                year=car_data.get('manufactured_year', 'Unknown'),
                body_type=car_data.get('body_type', 'Unknown'),
                confidence=confidence_display,
                price=car_data.get('price', {}).get('amount', 'Unknown'),
                currency=car_data.get('price', {}).get('currency', ''),
                user_email=st.session_state.user_email
            ), unsafe_allow_html=True)
            
            # Submit button with better styling
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <h3>📤 Ready to Submit</h3>
                <p style="color: #666; margin-bottom: 1rem;">Click the button below to send the car details to your email</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
            with col_submit2:
                st.markdown("""
                <style>
                .main-submit-button {
                    background: linear-gradient(90deg, #28a745 0%, #20c997 100%) !important;
                    color: white !important;
                    border: none !important;
                    padding: 1rem 3rem !important;
                    border-radius: 30px !important;
                    font-weight: bold !important;
                    font-size: 1.2rem !important;
                    box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4) !important;
                    text-transform: uppercase !important;
                    letter-spacing: 1px !important;
                }
                .main-submit-button:hover {
                    background: linear-gradient(90deg, #218838 0%, #1ea085 100%) !important;
                    transform: translateY(-3px) !important;
                    box-shadow: 0 8px 25px rgba(40, 167, 69, 0.5) !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                if st.button("🚀 SUBMIT & SEND EMAIL", type="primary", use_container_width=True, key="main_submit"):
                    with st.spinner("Sending car listing via email..."):
                        email_sender = EmailSender()
                        success = email_sender.send_email(
                            st.session_state.car_info,
                            st.session_state.image_path,
                            st.session_state.user_email
                        )
                        
                        if success:
                            st.markdown("""
                            <div class="success-box">
                                <h4>🎉 Success!</h4>
                                <p>Your car listing has been submitted and sent via email.</p>
                                <p><strong>Submission Time:</strong> {}</p>
                                <p><strong>Sent to:</strong> {}</p>
                            </div>
                            """.format(
                                st.session_state.submission_time.strftime("%Y-%m-%d %H:%M:%S"),
                                st.session_state.user_email
                            ), 
                            unsafe_allow_html=True)
                            
                            # Clean up temporary files
                            try:
                                os.unlink(st.session_state.image_path)
                                st.session_state.image_path = None
                            except:
                                pass
                            
                            # Reset session state
                            st.session_state.car_info = None
                            st.session_state.submission_time = None
                            
                            st.rerun()
                        else:
                            st.error("❌ Failed to send email. Please check your Gmail configuration.")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚗 Car Selling Platform | Powered by AI & Azure OpenAI</p>
        <p>Built with Streamlit, GPT-4o mini, and Computer Vision</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
