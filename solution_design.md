# 🚗 Car Selling Platform - Solution Design

## Architecture Overview

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Streamlit Web App]
        Upload[Image Upload]
        TextInput[Text Description Input]
    end
    
    subgraph "Processing Layer"
        IC[Image Classifier]
        TP[Text Processor]
        AI[Azure OpenAI GPT-4o mini]
    end
    
    subgraph "Data Layer"
        JSON[Structured JSON]
        Image[Car Image]
        Metadata[Processing Metadata]
    end
    
    subgraph "Output Layer"
        Email[Gmail SMTP]
        Recipient[msamy@orion360.com]
    end
    
    UI --> Upload
    UI --> TextInput
    
    Upload --> IC
    TextInput --> TP
    
    IC --> JSON
    TP --> AI
    AI --> JSON
    
    JSON --> Email
    Image --> Email
    Metadata --> Email
    
    Email --> Recipient
    
    style UI fill:#e1f5fe
    style IC fill:#f3e5f5
    style TP fill:#e8f5e8
    style AI fill:#fff3e0
    style Email fill:#fce4ec
```

## Component Architecture

### 1. User Interface (Streamlit)
- **Technology**: Streamlit 1.32.0
- **Features**: 
  - Drag & drop image upload
  - Rich text input for car descriptions
  - Real-time validation and feedback
  - Responsive design with custom CSS
  - Sidebar configuration panel

### 2. Image Classification Module
- **Current**: Dummy classifier with realistic simulation
- **Future**: Integration with real CV model
- **Output**: Car type detection with confidence scores
- **Supported Types**: sedan, SUV, hatchback, coupe, convertible, wagon, pickup, minivan, sports car, luxury car

### 3. Text Processing Engine
- **AI Model**: Azure OpenAI GPT-4o mini
- **Features**:
  - Prompt injection prevention
  - Input sanitization and validation
  - Structured JSON extraction
  - Error handling and fallbacks
- **Extracted Fields**: make, model, year, price, mileage, condition, fuel_type, transmission, color, features

### 4. Email Delivery System
- **Protocol**: Gmail SMTP with TLS
- **Attachments**: 
  - Car image (embedded)
  - Structured JSON data
  - HTML formatted email body
- **Recipient**: msamy@orion360.com

### 5. Security & Validation
- **Prompt Injection Prevention**: Pattern-based filtering
- **Input Sanitization**: Regex-based content cleaning
- **File Validation**: Size and format restrictions
- **Rate Limiting**: Built-in Streamlit session management

## Data Flow

1. **Image Upload** → Image validation → Car type classification
2. **Text Input** → Sanitization → AI processing → JSON extraction
3. **Data Integration** → Combined car information → Email composition
4. **Email Delivery** → SMTP transmission → Confirmation feedback

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Web Framework | Streamlit | 1.32.0 |
| AI Model | Azure OpenAI GPT-4o mini | Latest |
| Image Processing | Pillow (PIL) | 10.2.0 |
| Email | SMTP with SSL/TLS | Standard |
| Language | Python | 3.8+ |
| Dependencies | See requirements.txt | - |

## Security Features

### Prompt Injection Prevention
- Pattern-based filtering of suspicious inputs
- Input length limitations
- Content sanitization before AI processing
- System prompt isolation

### Data Validation
- File type restrictions
- Size limitations (10MB max)
- Content appropriateness checks
- Error handling for malformed inputs

## Performance Considerations

- **Image Processing**: Optimized for common formats (JPG, PNG, BMP)
- **AI Processing**: Low temperature (0.1) for consistent outputs
- **Email Delivery**: Asynchronous processing with user feedback
- **Memory Management**: Temporary file cleanup after processing

## Scalability Features

- **Modular Design**: Easy to replace components
- **Configuration Management**: Environment-based settings
- **Error Handling**: Graceful degradation
- **Session Management**: Streamlit-based state handling

## Future Integration Points

1. **Real CV Model**: Replace dummy classifier
2. **Database Storage**: Add persistent storage
3. **User Authentication**: Implement user management
4. **API Endpoints**: RESTful API for external access
5. **Analytics**: Usage tracking and reporting
6. **Multi-language Support**: Internationalization

## Deployment Considerations

- **Platform**: Windows PC (as specified)
- **Dependencies**: Python 3.8+ with pip
- **Environment**: Virtual environment recommended
- **Configuration**: Update Gmail credentials in config.py
- **Network**: Internet access required for Azure OpenAI and Gmail
