import json
import re
from typing import Dict, Any, Optional
import streamlit as st
from openai import AzureOpenAI
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME

class TextProcessor:
    """
    Processes car descriptions using Azure OpenAI GPT-4o mini to extract structured information.
    Includes prompt injection prevention measures.
    """
    
    def __init__(self):
        try:
            # Initialize Azure OpenAI client
            self.client = AzureOpenAI(
                api_key=AZURE_OPENAI_API_KEY,
                api_version="2025-01-01-preview",
                azure_endpoint=AZURE_OPENAI_ENDPOINT
            )
            self.deployment_name = AZURE_OPENAI_DEPLOYMENT_NAME
        except Exception as e:
            st.error(f"❌ Failed to initialize Azure OpenAI client: {str(e)}")
            st.error("Please check your Azure OpenAI configuration and try again.")
            self.client = None
            self.deployment_name = AZURE_OPENAI_DEPLOYMENT_NAME
        
        # Prompt injection prevention patterns
        self.suspicious_patterns = [
            r'system:|assistant:|user:|<|>|script|javascript|vbscript|onload|onerror',
            r'ignore previous instructions|ignore above|forget everything',
            r'new instructions|override|bypass|hack|exploit',
            r'roleplay|pretend|act as|you are now',
            r'output|print|execute|run|command'
        ]
    
    def sanitize_input(self, text: str) -> str:
        """
        Sanitizes user input to prevent prompt injection attacks.
        
        Args:
            text (str): Raw user input
            
        Returns:
            str: Sanitized text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remove suspicious patterns
        sanitized = text
        for pattern in self.suspicious_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove excessive whitespace and newlines
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        # Limit length to prevent abuse
        if len(sanitized) > 2000:
            sanitized = sanitized[:2000] + "..."
        
        return sanitized
    
    def validate_input(self, text: str) -> tuple[bool, str]:
        """
        Validates input text for safety and appropriateness.
        
        Args:
            text (str): Input text to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not text or len(text.strip()) < 10:
            return False, "Description must be at least 10 characters long."
        
        if len(text) > 2000:
            return False, "Description is too long (max 2000 characters)."
        
        # Check for suspicious content
        for pattern in self.suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False, "Description contains inappropriate content."
        
        return True, ""
    
    def extract_car_info(self, description: str, car_type: str) -> Dict[str, Any]:
        """
        Extracts structured car information from description using GPT-4o mini.
        
        Args:
            description (str): Car description text
            car_type (str): Detected car type from image
            
        Returns:
            Dict containing structured car information
        """
        if not self.client:
            st.error("❌ Azure OpenAI client not initialized. Please check configuration.")
            return {}
            
        try:
            # Sanitize and validate input
            sanitized_desc = self.sanitize_input(description)
            is_valid, error_msg = self.validate_input(sanitized_desc)
            
            if not is_valid:
                st.error(f"❌ Input validation failed: {error_msg}")
                return {}
            
            # Create the prompt with safety measures for the new JSON format
            system_prompt = """You are a car information extraction assistant. Your task is to extract specific details about a car from a user's description and organize them into a structured JSON format.

IMPORTANT RULES:
1. ONLY extract information that is explicitly mentioned in the user's description
2. DO NOT make up or infer information that isn't stated
3. If a field is not mentioned, use "not specified" as the value
4. Always return valid JSON format matching the exact structure specified
5. Focus only on car-related information

SPECIFIC FORMATTING RULES:
- Color: Use proper capitalization (e.g., "Blue", "Red", "Silver")
- Notices: 
  * type should be descriptive (e.g., "collision", "maintenance", "damage")
  * description should start with capital letter and end with period
  * Use proper grammar and punctuation

Return the information in this EXACT JSON structure:
{
  "car": {
    "body_type": "car_type_from_image",
    "color": "car_color",
    "brand": "car_manufacturer",
    "model": "car_model",
    "manufactured_year": "year_as_integer",
    "motor_size_cc": "engine_size_in_cc",
    "tires": {
      "type": "tire_condition",
      "manufactured_year": "tire_year"
    },
    "windows": "window_description",
    "notices": [
      {
        "type": "issue_type",
        "description": "issue_description"
      }
    ],
    "price": {
      "amount": "price_as_integer",
      "currency": "L.E"
    }
  }
}

Return ONLY the JSON object, no additional text."""

            user_prompt = f"""Car Type Detected: {car_type}

User Description: {sanitized_desc}

Please extract the car information and return it as a JSON object."""

            # Make API call to Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for consistent output
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            # Extract and parse response
            response_content = response.choices[0].message.content
            car_info = json.loads(response_content)
            
            # Post-process to ensure proper formatting
            car_info = self._post_process_car_info(car_info)
            
            # Don't add metadata - keep only the car object
            # car_info already contains the clean structure from GPT
            
            st.success("✅ Car information extracted successfully!")
            return car_info
            
        except json.JSONDecodeError as e:
            st.error(f"❌ Failed to parse AI response: {str(e)}")
            return {}
        except Exception as e:
            st.error(f"❌ Text processing failed: {str(e)}")
            return {}
    
    def format_json_output(self, car_info: Dict[str, Any]) -> str:
        """
        Formats the extracted car information as pretty JSON.
        
        Args:
            car_info (Dict): Car information dictionary
            
        Returns:
            str: Formatted JSON string
        """
        try:
            return json.dumps(car_info, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"❌ JSON formatting failed: {str(e)}")
            return "{}"
    
    def _post_process_car_info(self, car_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post-processes car information to ensure proper formatting.
        
        Args:
            car_info (Dict): Raw car information from AI
            
        Returns:
            Dict: Formatted car information
        """
        try:
            car_data = car_info.get('car', {})
            # Fix color capitalization
            if 'color' in car_data and car_data['color'] != 'not specified':
                car_data['color'] = car_data['color'].capitalize()
            
            # Fix notices formatting and structure
            if 'notices' in car_data:
                notices = car_data['notices']
                
                # Handle malformed notices (e.g., {"0": {...}} instead of [{...}])
                if isinstance(notices, dict):
                    # Convert dict with numeric keys to list
                    fixed_notices = []
                    for key, notice in notices.items():
                        if isinstance(notice, dict):
                            fixed_notices.append(notice)
                    car_data['notices'] = fixed_notices
                
                # Handle malformed array with numeric prefixes (e.g., [0:{...}])
                if isinstance(car_data['notices'], list):
                    fixed_notices = []
                    for item in car_data['notices']:
                        if isinstance(item, dict):
                            # This is a proper notice object
                            fixed_notices.append(item)
                        elif isinstance(item, str) and ':' in item:
                            # Handle cases like "0:{...}" by extracting the JSON part
                            try:
                                # Find the start of the JSON object
                                json_start = item.find('{')
                                if json_start != -1:
                                    json_part = item[json_start:]
                                    # Try to parse the JSON part
                                    parsed_notice = json.loads(json_part)
                                    if isinstance(parsed_notice, dict):
                                        fixed_notices.append(parsed_notice)
                            except (json.JSONDecodeError, ValueError):
                                # If parsing fails, skip this item
                                continue
                    
                    car_data['notices'] = fixed_notices
                
                # Process notices if it's a list
                if isinstance(car_data['notices'], list):
                    for notice in car_data['notices']:
                        if isinstance(notice, dict):
                            # Fix type field
                            if 'type' in notice:
                                notice_type = notice['type'].lower()
                                # Map common variations to expected values
                                if 'collision' in notice_type or 'crash' in notice_type or 'accident' in notice_type:
                                    notice['type'] = 'collision'
                                elif 'maintenance' in notice_type or 'service' in notice_type:
                                    notice['type'] = 'maintenance'
                                elif 'damage' in notice_type:
                                    notice['type'] = 'damage'
                                else:
                                    notice['type'] = notice_type
                            
                            # Fix description formatting
                            if 'description' in notice:
                                desc = notice['description']
                                if desc and desc != 'not specified':
                                    # Ensure it starts with capital letter
                                    if desc[0].islower():
                                        desc = desc[0].upper() + desc[1:]
                                    # Ensure it ends with period
                                    if not desc.endswith('.'):
                                        desc = desc + '.'
                                    notice['description'] = desc
            
            return car_info
            
        except Exception as e:
            st.warning(f"⚠️ Post-processing warning: {str(e)}")
            return car_info
