# 🏥 AI Medical Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Multilingual AI-Powered Healthcare Consultation Platform**

*Voice & Text Input • 10 Static Questions • Gemma3 Reports • AES-256 Encryption*

[Features](#-features) • [Quick Start](#-quick-start) • [Demo](#-demo) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 📋 Overview

AI Medical Assistant is a comprehensive healthcare consultation platform that combines **Browser Web Speech API** for voice input, **10 static medical questions**, and **Gemma3 AI** for generating professional medical reports. The system supports **English, Hindi, and Tamil** in both voice and text modes, with all patient data encrypted using **AES-256**.

### ✨ Key Highlights

- 🎤 **Browser-Native Voice Input** - No server-side speech processing required
- 🔒 **AES-256 Encryption** - All patient data encrypted in MySQL database
- 🌍 **Multilingual Support** - English, हिंदी, and தமிழ் (voice + text)
- 📋 **10 Static Questions** - Consistent medical assessment every time
- 🤖 **Gemma3 AI Reports** - Comprehensive medical analysis with ICD-10 codes
- 💾 **MySQL Storage** - Secure patient records and consultation history

---

## 🎯 Features

### Patient Management
- ✅ Patient registration with auto-generated unique IDs
- ✅ Secure patient login system
- ✅ Complete patient history tracking
- ✅ Encrypted medical records storage

### Consultation Flow
- ✅ **Voice Mode**: Questions spoken aloud + voice answers (one-by-one)
- ✅ **Text Mode**: All questions displayed as forms (fill all at once)
- ✅ Real-time speech-to-text transcription (EN/HI/TA)
- ✅ Text-to-speech for questions in patient's language
- ✅ Automatic language detection and translation

### Medical Reports
- ✅ Clinical summary with ICD-10 diagnosis codes
- ✅ Differential diagnosis with probability ratings
- ✅ Recommended laboratory tests
- ✅ Immediate care plan and prescriptions
- ✅ Lifestyle recommendations
- ✅ Red flag warnings and urgency levels
- ✅ Specialist referral recommendations
- ✅ Download reports as text files

### Security & Privacy
- ✅ AES-256 Fernet encryption for all sensitive data
- ✅ Unique encryption IV per record
- ✅ Encrypted Q&A pairs stored separately
- ✅ HIPAA-compliant data handling practices

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **MySQL 8.0+**
- **Ollama** with Gemma3:4b model
- **Modern Web Browser** (Chrome/Edge/Safari for Web Speech API)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-medical-assistant.git
cd ai-medical-assistant
```

#### 2. Install Python Dependencies
```bash
pip install fastapi uvicorn mysql-connector-python cryptography ollama
```

#### 3. Install Ollama and Gemma3
```bash
# Install Ollama (https://ollama.ai)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Gemma3:4b model
ollama pull gemma3:4b
```

#### 4. Setup MySQL Database
```sql
-- Create database
CREATE DATABASE medical_assistant;

-- Create user (optional)
CREATE USER 'medical_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON medical_assistant.* TO 'medical_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 5. Configure Database Connection

Edit `database_mysql.py` (lines 23 and 37):
```python
self.connection = mysql.connector.connect(
    host='localhost',
    user='root',  # Your MySQL username
    password='your_password',  # Your MySQL password
    database='medical_assistant'
)
```

#### 6. Start the Backend
```bash
python backend.py
```

Expected output:
```
✅ Connected to MySQL database
✅ Database tables created/verified

======================================================================
AI MEDICAL ASSISTANT - FORM STYLE WITH 10 STATIC QUESTIONS
======================================================================
✅ 10 Static Questions (Same Every Time)
✅ Browser Web Speech API (No Whisper)
✅ Gemma3 Report Generation
✅ MySQL Encrypted Storage
✅ Form-Based UI Compatible
======================================================================

INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 7. Open the Frontend
```bash
# Option 1: Direct file
# Double-click index.html

# Option 2: Via backend
# Open browser: http://localhost:8000
```

---

## 🎬 Demo

### Voice Mode (Tamil Example)

```
1. Patient selects தமிழ் language
2. Patient clicks 🎤 Voice tab
3. Patient speaks: "எனக்கு மூன்று நாளாக காய்ச்சல் இருக்கிறது"
4. System transcribes in Tamil
5. Patient clicks "Start 10-Question Consultation"
6. System asks Question 1 in Tamil (displayed + spoken aloud)
7. Patient speaks answer in Tamil
8. Repeat for all 10 questions
9. Gemma3 generates comprehensive medical report
10. Report saved encrypted in MySQL database
```

### Text Mode (Hindi Example)

```
1. Patient selects हिंदी language
2. Patient clicks ✍️ Text tab
3. Patient types: "मुझे बुखार और सिरदर्द है"
4. Patient clicks "Start 10-Question Consultation"
5. All 10 questions appear in Hindi
6. Patient fills all text boxes
7. Patient clicks "Generate Report"
8. Gemma3 analyzes all answers
9. Report generated and stored
```

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────┐
│ FRONTEND (index.html)                                │
│ - Browser Web Speech API (Voice Input/Output)       │
│ - Multilingual UI (EN/HI/TA)                        │
│ - Voice Mode: One-by-one questions with TTS         │
│ - Text Mode: Form-based all-at-once questions       │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/JSON
┌──────────────────────▼──────────────────────────────┐
│ BACKEND (backend.py - FastAPI)                      │
│ - 10 Static Questions (hard-coded)                  │
│ - Gemma3:4b Report Generation                       │
│ - Symptom extraction with Gemma3                    │
│ - Session management                                │
└──────────────────────┬──────────────────────────────┘
                       │ Encrypted Operations
┌──────────────────────▼──────────────────────────────┐
│ ENCRYPTION (encryption.py)                          │
│ - AES-256 Fernet encryption                         │
│ - Unique IV per record                              │
│ - Secure key management                             │
└──────────────────────┬──────────────────────────────┘
                       │ Encrypted Storage
┌──────────────────────▼──────────────────────────────┐
│ DATABASE (MySQL - database_mysql.py)                │
│ - Patients table (basic info)                       │
│ - Medical_history table (chronic conditions)        │
│ - Consultations table (encrypted Q&A, reports)      │
│ - Medical_records table (encrypted files)           │
└─────────────────────────────────────────────────────┘
```

### Data Flow

```
User Voice/Text Input
    ↓
Browser Speech API (for voice)
    ↓
Transcribed Text
    ↓
FastAPI Backend
    ↓
Gemma3 Symptom Extraction
    ↓
10 Static Questions Returned
    ↓
User Answers (Voice/Text)
    ↓
Gemma3 Report Generation
    ↓
AES-256 Encryption
    ↓
MySQL Database Storage
    ↓
Report Displayed & Downloadable
```

---

## 📚 Documentation

### API Endpoints

#### Patient Management

**POST /register-patient**
```python
# Register new patient
FormData: {
    "name": "John Doe",
    "dob": "1990-05-15",
    "age": 35,
    "sex": "Male",
    "contact": "+91 1234567890",
    "address": "123 Main St"
}
Response: {
    "success": true,
    "patient_id": "PT0754BC16"
}
```

**POST /patient-login**
```python
# Login existing patient
FormData: {
    "patient_id": "PT0754BC16"
}
Response: {
    "success": true,
    "patient": {...},
    "consultation_count": 3
}
```

**GET /patient/{patient_id}/history**
```python
# Get consultation history
Response: {
    "success": true,
    "history": [...],
    "count": 3
}
```

#### Consultation

**POST /test-with-text**
```python
# Initialize consultation with symptoms
FormData: {
    "symptoms_text": "I have fever and headache",
    "patient_id": "PT0754BC16"
}
Response: {
    "success": true,
    "symptoms": {...},
    "questions": [10 static questions],
    "has_history": true
}
```

**POST /analyze-with-history**
```python
# Generate Gemma3 report from answers
FormData: {
    "patient_id": "PT0754BC16",
    "symptoms": "{...}",
    "answers": "[...]"
}
Response: {
    "success": true,
    "patient_report": "...",
    "consultation_id": "CONS_20251031093000",
    "qa_count": 10
}
```

### Database Schema

#### Patients Table
```sql
CREATE TABLE patients (
    patient_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    age INT NOT NULL,
    sex ENUM('Male', 'Female', 'Other'),
    contact VARCHAR(20),
    address TEXT,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Consultations Table
```sql
CREATE TABLE consultations (
    consultation_id VARCHAR(30) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    chief_complaint TEXT,
    encrypted_symptoms BLOB,
    encrypted_analysis BLOB,
    encrypted_diagnosis BLOB,
    encrypted_treatment BLOB,
    encrypted_qa_pairs BLOB,
    encrypted_full_report BLOB,
    encryption_iv VARBINARY(16),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
```

### 10 Static Questions

The system uses these 10 medical questions (same every consultation):

1. How long have you been experiencing these symptoms?
2. On a scale of 1-10, how severe are your symptoms?
3. When did the symptoms first start (date/time)?
4. Do the symptoms come and go, or are they constant?
5. Have you experienced this before?
6. Have you taken any medication for this? If yes, which ones?
7. Does anything make the symptoms better or worse?
8. Do you have any other symptoms you haven't mentioned?
9. How does this affect your daily activities (work, sleep, exercise)?
10. Have you noticed any recent changes in your health or lifestyle?

*Questions automatically translated to Hindi and Tamil*

---

## 🧪 Testing

### Run System Tests
```bash
python test_complete_system.py
```

Expected output:
```
1️⃣ Testing Encryption Module...
✅ Encryption works!

2️⃣ Testing Database Connection...
✅ MySQL connected successfully

3️⃣ Testing Patient Registration...
✅ Patient registered: PT0754BC16

4️⃣ Testing Encrypted Consultation...
✅ Consultation saved (encrypted)

5️⃣ Testing Decryption...
✅ Consultation retrieved and decrypted

6️⃣ Testing Patient History...
✅ Patient history retrieved
```

### Manual Testing Checklist

- [ ] Patient registration works
- [ ] Patient login works
- [ ] English voice input transcribes correctly
- [ ] Hindi voice input transcribes correctly
- [ ] Tamil voice input transcribes correctly
- [ ] Questions spoken aloud in selected language (TTS)
- [ ] Voice answers recorded correctly
- [ ] Text mode displays all 10 questions
- [ ] Gemma3 report generates successfully
- [ ] Report contains all required sections
- [ ] Report saved to database encrypted
- [ ] Report download works

---

## 🔐 Security Features

### Encryption
- **Algorithm**: AES-256 using Fernet
- **Key Generation**: Cryptographically secure random keys
- **Unique IVs**: Each record has unique initialization vector
- **Key Storage**: Environment variables (production) or secure key manager

### Data Protection
- All symptoms, diagnoses, and Q&A pairs encrypted at rest
- Encryption IV stored separately from encrypted data
- Patient IDs generated using SHA-256 hash
- No plain-text storage of sensitive medical information

### Best Practices
- Regular security audits recommended
- Key rotation every 90 days (production)
- Access logs for all database operations
- HTTPS/TLS for all network communications

---

## 🌍 Multilingual Support

### Supported Languages

| Language | Code | Voice Input | Voice Output | Text Input | Translation |
|----------|------|-------------|--------------|------------|-------------|
| English  | `en` | ✅ `en-US`  | ✅ `en-US`   | ✅         | -           |
| Hindi    | `hi` | ✅ `hi-IN`  | ✅ `hi-IN`   | ✅         | ✅          |
| Tamil    | `ta` | ✅ `ta-IN`  | ✅ `ta-IN`   | ✅         | ✅          |

### Adding New Languages

1. Add language code to `QUESTIONS_TRANSLATIONS` in `index.html`
2. Translate all 10 questions to target language
3. Add language button to UI
4. Update speech recognition language mapping
5. Test voice and text input thoroughly

---

## 📊 Project Structure

```
medical_assistant/
├── backend.py                  # FastAPI backend server
├── database_mysql.py           # MySQL operations & encryption
├── encryption.py               # AES-256 Fernet encryption
├── index.html                  # Frontend UI (voice/text modes)
├── test_complete_system.py     # System integration tests
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── reports/                    # Generated reports (auto-created)
│   └── patient_report_*.txt
└── .env                        # Environment variables (create manually)
```

---

## 🛠️ Configuration

### Environment Variables

Create a `.env` file:
```bash
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=medical_assistant
OLLAMA_HOST=http://localhost:11434
ENCRYPTION_KEY=your_fernet_key  # Generate with: from cryptography.fernet import Fernet; print(Fernet.generate_key())
```

### Ollama Configuration

Ensure Ollama is running:
```bash
# Check Ollama status
ollama list

# Verify Gemma3:4b is installed
ollama run gemma3:4b "Hello"
```

---

## 🐛 Troubleshooting

### Common Issues

**1. MySQL Connection Failed**
```
❌ Error: 1045 (28000): Access denied for user 'root'@'localhost'
```
**Solution**: Update password in `database_mysql.py` lines 23 & 37

**2. Voice Input Not Working**
```
❌ Not supported
```
**Solution**: Use Chrome/Edge/Safari. Firefox has limited support.

**3. Questions Not Spoken Aloud**
```
Questions display but no TTS
```
**Solution**: Check browser TTS permissions. Test in browser console:
```javascript
window.speechSynthesis.speak(new SpeechSynthesisUtterance("Test"));
```

**4. Gemma3 Report Generation Fails**
```
❌ Gemma3 error
```
**Solution**: 
- Check Ollama is running: `ollama list`
- Verify Gemma3 installed: `ollama run gemma3:4b`
- Check backend logs for detailed error

**5. Database Tables Not Created**
```
❌ Table 'consultations' doesn't exist
```
**Solution**: Drop and recreate database:
```sql
DROP DATABASE medical_assistant;
CREATE DATABASE medical_assistant;
```
Then restart backend.

---

## 📈 Performance

### Benchmarks

| Operation | Time (avg) | Notes |
|-----------|------------|-------|
| Patient Registration | ~200ms | MySQL insert |
| Speech Transcription | Real-time | Browser-native |
| Symptom Extraction | ~2-3s | Gemma3 inference |
| Question Loading | ~1s | Static questions |
| Report Generation | ~8-12s | Gemma3 full report |
| Database Encryption | ~50ms | AES-256 per record |
| Database Decryption | ~30ms | AES-256 per record |

### Optimization Tips

- Use connection pooling for MySQL (production)
- Cache Gemma3 responses for similar symptoms
- Implement rate limiting for API endpoints
- Use Redis for session management (scale)
- Consider GPU acceleration for Ollama

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linters
flake8 backend.py
black backend.py

# Run tests
pytest tests/
```

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Ollama** - Local LLM inference
- **Google Gemma** - Medical AI model
- **FastAPI** - Modern Python web framework
- **MySQL** - Reliable database system
- **Web Speech API** - Browser-native speech recognition

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-medical-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-medical-assistant/discussions)
- **Email**: support@example.com

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: This system is an AI-assisted preliminary assessment tool and is **NOT a substitute for professional medical advice, diagnosis, or treatment**. 

- Always consult a qualified healthcare provider for medical concerns
- Do NOT start medications without doctor approval
- Seek emergency medical care for severe symptoms
- Use this tool for educational and preliminary assessment purposes only

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Additional languages (Spanish, French, Arabic)
- [ ] Video consultation integration
- [ ] Lab report upload and analysis
- [ ] Mobile app (React Native)
- [ ] Doctor dashboard with patient management
- [ ] Appointment scheduling system
- [ ] Insurance claim integration
- [ ] Telemedicine video calls
- [ ] Prescription management
- [ ] Medicine reminder notifications

### Version 3.0 (Future)
- [ ] AI-powered diagnosis suggestions
- [ ] Medical imaging analysis (X-ray, CT scans)
- [ ] Wearable device integration
- [ ] Chronic disease management
- [ ] Mental health assessment module
- [ ] Multilingual report translation
- [ ] Voice assistant (Alexa/Google Home)

---

<div align="center">

**Made with ❤️ for accessible healthcare**

⭐ Star this repository if you find it helpful!

[Report Bug](https://github.com/yourusername/ai-medical-assistant/issues) • [Request Feature](https://github.com/yourusername/ai-medical-assistant/issues)

</div>
