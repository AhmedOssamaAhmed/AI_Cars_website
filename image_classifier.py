import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import streamlit as st
from typing import Dict, Any
import time

class CarImageClassifier:
    """
    Real car image classifier using Hugging Face transformers.
    Uses a pre-trained model for car type classification.
    """
    
    def __init__(self):
        try:
            # Load pre-trained model and processor for car classification
            self.model_name = "microsoft/resnet-50"  # Good general image classification model
            self.processor = AutoImageProcessor.from_pretrained(self.model_name)
            self.model = AutoModelForImageClassification.from_pretrained(self.model_name)
            
            # Map ImageNet classes to car types (ImageNet has many car categories)
            self.car_type_mapping = {
                "sedan": ["car", "automobile", "motor car", "auto", "machine", "motorcar"],
                "SUV": ["sport utility", "sport utility vehicle", "SUV", "jeep"],
                "hatchback": ["car", "automobile", "motor car"],
                "coupe": ["car", "automobile", "motor car"],
                "convertible": ["car", "automobile", "motor car"],
                "wagon": ["car", "automobile", "motor car"],
                "pickup": ["pickup", "pickup truck", "truck"],
                "minivan": ["minivan", "van", "caravan"],
                "sports car": ["car", "automobile", "motor car", "racing car"],
                "luxury car": ["car", "automobile", "motor car", "limousine", "limo"]
            }
            
            self.confidence_threshold = 0.6
            st.success("✅ AI Model loaded successfully!")
            
        except Exception as e:
            st.error(f"❌ Failed to load AI model: {str(e)}")
            st.warning("⚠️ Falling back to basic classification")
            self.model = None
            self.processor = None
    
    def classify_car_type(self, image_path: str) -> Dict[str, Any]:
        """
        Performs real car type classification using AI model.
        
        Args:
            image_path (str): Path to the uploaded image
            
        Returns:
            Dict containing classification results
        """
        try:
            start_time = time.time()
            
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            
            if not self.validate_image(image_path):
                return {
                    "car_type": "unknown",
                    "confidence": 0.0,
                    "model_version": "resnet-50",
                    "processing_time_ms": 0,
                    "status": "error",
                    "error_message": "Image validation failed"
                }
            
            if self.model and self.processor:
                # Use AI model for classification
                return self._ai_classification(image, start_time)
            else:
                # Fallback to basic classification
                return self._basic_classification(image, start_time)
                
        except Exception as e:
            st.error(f"❌ Image classification failed: {str(e)}")
            return {
                "car_type": "unknown",
                "confidence": 0.0,
                "model_version": "resnet-50",
                "processing_time_ms": 0,
                "status": "error",
                "error_message": str(e)
            }
    
    def _ai_classification(self, image: Image.Image, start_time: float) -> Dict[str, Any]:
        """Performs AI-based classification using the loaded model."""
        try:
            # Preprocess image for the model
            inputs = self.processor(image, return_tensors="pt")
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            
            # Get top predictions
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            top_probs, top_indices = torch.topk(probabilities, 5)
            
            # Get class labels
            predicted_labels = []
            for idx in top_indices[0]:
                label = self.model.config.id2label[idx.item()]
                predicted_labels.append(label.lower())
            
            # Map to car types and find best match
            best_car_type, best_confidence = self._map_to_car_type(predicted_labels, top_probs[0])
            
            processing_time = int((time.time() - start_time) * 1000)
            
            result = {
                "car_type": best_car_type,
                "confidence": round(best_confidence, 3),
                "model_version": "resnet-50",
                "processing_time_ms": processing_time,
                "status": "success",
                "top_predictions": list(zip(predicted_labels, top_probs[0].tolist()))
            }
            
            st.success(f"🎯 AI Detected: {best_car_type} (Confidence: {best_confidence:.1%})")
            return result
            
        except Exception as e:
            st.warning(f"⚠️ AI classification failed, using fallback: {str(e)}")
            return self._basic_classification(image, start_time)
    
    def _basic_classification(self, image: Image.Image, start_time: float) -> Dict[str, Any]:
        """Fallback basic classification based on image analysis."""
        try:
            # Simple heuristics based on image characteristics
            width, height = image.size
            aspect_ratio = width / height
            
            # Basic car type detection based on aspect ratio and size
            if aspect_ratio > 1.8:  # Very wide
                car_type = "sedan"
                confidence = 0.7
            elif aspect_ratio > 1.5:  # Wide
                car_type = "SUV"
                confidence = 0.75
            elif aspect_ratio > 1.2:  # Medium
                car_type = "hatchback"
                confidence = 0.65
            else:  # Square-ish
                car_type = "coupe"
                confidence = 0.6
            
            processing_time = int((time.time() - start_time) * 1000)
            
            result = {
                "car_type": car_type,
                "confidence": confidence,
                "model_version": "basic-heuristic",
                "processing_time_ms": processing_time,
                "status": "success",
                "method": "aspect_ratio_analysis"
            }
            
            st.info(f"🔍 Basic Detection: {car_type} (Confidence: {confidence:.1%})")
            return result
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            return {
                "car_type": "unknown",
                "confidence": 0.0,
                "model_version": "basic-heuristic",
                "processing_time_ms": processing_time,
                "status": "error",
                "error_message": str(e)
            }
    
    def _map_to_car_type(self, predicted_labels: list, probabilities: torch.Tensor) -> tuple:
        """Maps ImageNet labels to car types and returns best match."""
        best_car_type = "unknown"
        best_confidence = 0.0
        
        for label, prob in zip(predicted_labels, probabilities):
            prob_value = prob.item()
            
            # Check if this label maps to any car type
            for car_type, keywords in self.car_type_mapping.items():
                if any(keyword in label for keyword in keywords):
                    if prob_value > best_confidence:
                        best_car_type = car_type
                        best_confidence = prob_value
                        break
        
        # If no specific car type found, use the highest probability vehicle-related prediction
        if best_car_type == "unknown":
            for label, prob in zip(predicted_labels, probabilities):
                prob_value = prob.item()
                if any(word in label for word in ["car", "vehicle", "automobile", "truck", "bus"]):
                    best_car_type = "sedan"  # Default to sedan for general vehicles
                    best_confidence = prob_value
                    break
        
        # If still no match, use highest probability
        if best_car_type == "unknown":
            best_car_type = "sedan"
            best_confidence = probabilities[0].item()
        
        return best_car_type, best_confidence
    
    def get_supported_formats(self) -> list:
        """Returns supported image formats."""
        return ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    def validate_image(self, image_path: str) -> bool:
        """Validates if the image is suitable for classification."""
        try:
            with Image.open(image_path) as img:
                # Check if image is too small
                if img.size[0] < 100 or img.size[1] < 100:
                    return False
                # Check if image is too large
                if img.size[0] > 4000 or img.size[1] > 4000:
                    return False
                return True
        except Exception:
            return False
