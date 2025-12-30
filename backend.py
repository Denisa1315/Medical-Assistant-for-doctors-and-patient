from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import ollama
import json
import os
from datetime import datetime
from typing import List, Optional
import uvicorn

# Import database
from database_mysql import db

app = FastAPI(title="AI Medical Assistant API - Form Style")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 10 STATIC QUESTIONS (same every time)
STATIC_QUESTIONS = [
    "How long have you been experiencing these symptoms?",
    "On a scale of 1-10, how severe are your symptoms?",
    "When did the symptoms first start (date/time)?",
    "Do the symptoms come and go, or are they constant?",
    "Have you experienced this before?",
    "Have you taken any medication for this? If yes, which ones?",
    "Does anything make the symptoms better or worse?",
    "Do you have any other symptoms you haven't mentioned?",
    "How does this affect your daily activities (work, sleep, exercise)?",
    "Have you noticed any recent changes in your health or lifestyle?"
]

session_data = {}

@app.get("/")
def home():
    return {
        "status": "healthy",
        "message": "AI Medical Assistant API - Form Style with 10 Static Questions",
        "features": ["10 Static Questions", "Browser Speech API", "Gemma3 Reports", "MySQL Storage"]
    }

# ============ PATIENT MANAGEMENT ============

@app.post("/register-patient")
async def register_patient(
    name: str = Form(...),
    dob: str = Form(...),
    age: int = Form(...),
    sex: str = Form(...),
    contact: str = Form(...),
    address: str = Form(...)
):
    """Register new patient"""
    try:
        patient_id = db.register_patient(name, dob, age, sex, contact, address)
        return JSONResponse({
            "success": True,
            "patient_id": patient_id,
            "message": "Patient registered successfully"
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/patient-login")
async def patient_login(patient_id: str = Form(...)):
    """Patient login"""
    patient = db.get_patient(patient_id)
    if patient:
        session_data['current_patient'] = patient_id
        return JSONResponse({
            "success": True,
            "patient": patient,
            "consultation_count": patient.get('consultation_count', 0)
        })
    return JSONResponse({"success": False, "error": "Patient not found"}, status_code=404)

@app.get("/patient/{patient_id}")
def get_patient_info(patient_id: str):
    """Get patient information"""
    patient = db.get_patient(patient_id)
    if patient:
        return JSONResponse({"success": True, "patient": patient})
    return JSONResponse({"success": False, "error": "Patient not found"}, status_code=404)

@app.get("/patient/{patient_id}/history")
def get_patient_history(patient_id: str):
    """Get patient consultation history"""
    history = db.get_patient_history(patient_id)
    return JSONResponse({"success": True, "history": history, "count": len(history)})

# ============ SYMPTOM ANALYSIS + STATIC QUESTIONS ============

@app.post("/test-with-text")
async def test_with_text(
    symptoms_text: str = Form(...),
    patient_id: str = Form(...)
):
    """Analyze symptoms and return 10 static questions"""
    
    patient = db.get_patient(patient_id)
    if not patient:
        return JSONResponse({"success": False, "error": "Patient not found"}, status_code=404)
    
    # Extract symptoms using Gemma3
    symptoms = await extract_symptoms_internal(symptoms_text)
    
    # Get patient history context
    history = db.get_patient_history(patient_id)
    history_context = ""
    if history:
        last_visit = history[-1] if history else None
        if last_visit:
            history_context = f"Previous visit: {last_visit.get('chief_complaint', 'N/A')}"
    
    # Store in session for later use
    session_data[patient_id] = {
        'symptoms': symptoms,
        'symptoms_text': symptoms_text
    }
    
    # Return 10 STATIC QUESTIONS (same every time)
    return JSONResponse({
        "success": True,
        "patient": patient,
        "symptoms": symptoms,
        "questions": STATIC_QUESTIONS,
        "has_history": len(history) > 0,
        "history_context": history_context
    })

async def extract_symptoms_internal(text: str) -> dict:
    """Extract symptoms using Gemma3"""
    prompt = f"""Extract symptoms from this text. Return ONLY JSON format.

Patient says: "{text}"

Return exactly this JSON structure:
{{
    "chief_complaint": "main reason for visit",
    "symptoms": [{{"name": "symptom", "severity": "mild/moderate/severe", "duration": "how long"}}]
}}

Only JSON, no explanations."""

    try:
        response = ollama.chat(
            model='gemma3:4b',
            messages=[
                {'role': 'system', 'content': 'Extract symptoms. Return ONLY valid JSON.'},
                {'role': 'user', 'content': prompt}
            ],
            options={'temperature': 0.2, 'num_predict': 300}
        )
        
        content = response['message']['content']
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start >= 0 and end > start:
            return json.loads(content[start:end])
    except Exception as e:
        print(f"❌ Symptom extraction error: {e}")
    
    # Fallback
    return {
        "chief_complaint": text[:100],
        "symptoms": [{"name": text, "severity": "unknown", "duration": "unknown"}]
    }

# ============ GEMMA3 REPORT GENERATION ============

def generate_gemma3_report(patient: dict, symptoms: dict, answers: list) -> str:
    """Generate comprehensive medical report using Gemma3"""
    
    # Build Q&A context
    qa_text = "\n".join([f"Q: {STATIC_QUESTIONS[i]}\nA: {answers[i]}" for i in range(min(len(STATIC_QUESTIONS), len(answers)))])
    
    prompt = f"""You are a medical doctor. Generate a comprehensive medical report in BULLET POINT format.

PATIENT INFORMATION:
- Age: {patient['age']} years
- Sex: {patient['sex']}
- Chronic Conditions: {', '.join(patient.get('chronic_conditions', [])) or 'None'}
- Current Medications: {', '.join(patient.get('current_medications', [])) or 'None'}
- Allergies: {', '.join(patient.get('allergies', [])) or 'None'}

CHIEF COMPLAINT: {symptoms.get('chief_complaint', 'Not specified')}

SYMPTOMS: {json.dumps(symptoms.get('symptoms', []), indent=2)}

PATIENT ANSWERS TO 10 QUESTIONS:
{qa_text}

Generate a CONCISE medical report using this EXACT format with ONLY bullet points:

CLINICAL SUMMARY
• [Key finding 1]
• [Key finding 2]
• [Key finding 3]

DIFFERENTIAL DIAGNOSIS
• Condition 1 - HIGH/MEDIUM/LOW probability - ICD-10: [code]
• Condition 2 - HIGH/MEDIUM/LOW probability - ICD-10: [code]
• Condition 3 - HIGH/MEDIUM/LOW probability - ICD-10: [code]

RECOMMENDED TESTS
• [Test 1] - ROUTINE/URGENT
• [Test 2] - ROUTINE/URGENT
• [Test 3] - ROUTINE/URGENT

IMMEDIATE CARE PLAN
• [Action 1]
• [Action 2]
• [Action 3]

PRESCRIPTION
1. [Drug] - Dose: [amount] - Frequency: [timing] - Duration: [days]
2. [Drug] - Dose: [amount] - Frequency: [timing] - Duration: [days]
3. [Drug] - Dose: [amount] - Frequency: [timing] - Duration: [days]

LIFESTYLE RECOMMENDATIONS
• [Recommendation 1]
• [Recommendation 2]
• [Recommendation 3]

RED FLAG WARNINGS
• [Warning 1]
• [Warning 2]
• [Warning 3]

URGENCY LEVEL: ROUTINE/URGENT/EMERGENCY
Follow-up: [X days] - [Reason]

SPECIALIST REFERRAL: YES/NO - [If yes, which specialty]

Use ONLY bullet points. Be concise. Include specific medical details."""

    try:
        print("🔄 Generating report with Gemma3...")
        response = ollama.chat(
            model='gemma3:4b',
            messages=[
                {'role': 'system', 'content': 'You are a medical doctor. Respond in BULLET POINTS only. Be concise and specific.'},
                {'role': 'user', 'content': prompt}
            ],
            options={
                'temperature': 0.3,
                'num_predict': 1200,
                'top_p': 0.95
            }
        )
        
        report = response['message']['content']
        print(f"✅ Report generated ({len(report)} chars)")
        return report
        
    except Exception as e:
        print(f"❌ Gemma3 error: {e}")
        return generate_fallback_report(patient, symptoms, answers)

def generate_fallback_report(patient: dict, symptoms: dict, answers: list) -> str:
    """Fallback report if Gemma3 fails"""
    chief = symptoms.get('chief_complaint', 'multiple symptoms')
    
    return f"""CLINICAL SUMMARY
• {patient['age']}-year-old {patient['sex'].lower()} presenting with {chief}
• Symptoms require further clinical evaluation
• Patient is stable, no immediate emergency indicators

DIFFERENTIAL DIAGNOSIS
• Viral Upper Respiratory Infection - MEDIUM - ICD-10: J06.9
• Influenza - MEDIUM - ICD-10: J11.1
• Bacterial Infection - LOW - ICD-10: A49.9

RECOMMENDED TESTS
• Complete Blood Count (CBC) - ROUTINE
• C-Reactive Protein (CRP) - ROUTINE
• Chest X-ray (if indicated) - ROUTINE

IMMEDIATE CARE PLAN
• Rest and adequate hydration (2-3 liters/day)
• Monitor temperature regularly
• Avoid strenuous activities

PRESCRIPTION
1. Paracetamol - Dose: 500mg - Frequency: Every 6 hours as needed - Duration: 5 days
2. Ibuprofen - Dose: 400mg - Frequency: Every 8 hours with food - Duration: 5 days
3. Vitamin C - Dose: 1000mg - Frequency: Once daily - Duration: 7 days

LIFESTYLE RECOMMENDATIONS
• Maintain proper sleep hygiene (7-8 hours)
• Eat nutritious, balanced meals
• Practice good hand hygiene

RED FLAG WARNINGS
• High fever (>103°F/39.5°C) not responding to medication
• Difficulty breathing or chest pain
• Severe persistent headache or confusion

URGENCY LEVEL: ROUTINE
Follow-up: 3-5 days - Reassess symptoms and review test results

SPECIALIST REFERRAL: NO - General physician follow-up adequate"""

# ============ ANALYZE WITH HISTORY (Final Report) ============

@app.post("/analyze-with-history")
async def analyze_with_history(
    patient_id: str = Form(...),
    symptoms: str = Form(...),
    answers: str = Form(...)
):
    """Generate comprehensive report from all answers"""
    
    patient = db.get_patient(patient_id)
    if not patient:
        return JSONResponse({"success": False, "error": "Patient not found"}, status_code=404)
    
    symptoms_dict = json.loads(symptoms)
    answers_list = json.loads(answers)
    
    # Generate report using Gemma3
    analysis = generate_gemma3_report(patient, symptoms_dict, answers_list)
    
    # Format patient report
    timestamp = datetime.now()
    consultation_id = f"CONS_{timestamp.strftime('%Y%m%d%H%M%S')}"
    history = db.get_patient_history(patient_id)
    
    patient_report = f"""PATIENT HEALTH ASSESSMENT REPORT
===============================================================

Date: {timestamp.strftime("%B %d, %Y at %I:%M %p")}
Patient: {patient['name']} (ID: {patient_id})
Visit: #{len(history) + 1}

===============================================================

{analysis}

===============================================================

IMPORTANT DISCLAIMER

• This is an AI-assisted preliminary assessment
• NOT a substitute for professional medical advice
• ALWAYS consult a qualified healthcare provider
• Do NOT start medications without doctor approval
• Seek emergency care for RED FLAGS

===============================================================
Consultation ID: {consultation_id}
System: AI Medical Assistant (Gemma3:4B)
==============================================================="""

    # Build Q&A pairs for database storage
    qa_pairs = [
        {"question": STATIC_QUESTIONS[i], "answer": answers_list[i]}
        for i in range(min(len(STATIC_QUESTIONS), len(answers_list)))
    ]
    
    # Save to database with Q&A pairs
    try:
        db.add_consultation(patient_id, {
            "chief_complaint": symptoms_dict.get('chief_complaint'),
            "symptoms": symptoms_dict,
            "qa_pairs": qa_pairs,
            "analysis": analysis,
            "diagnosis": "AI assessment - requires physician review",
            "treatment_summary": "See prescription in report",
            "full_report": patient_report
        })
        print(f"✅ Report saved to database: {consultation_id}")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Save to file
    try:
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/patient_report_{consultation_id}.txt", "w", encoding="utf-8") as f:
            f.write(patient_report)
        print(f"✅ Report saved to file")
    except Exception as e:
        print(f"❌ File save error: {e}")
    
    return JSONResponse({
        "success": True,
        "consultation_id": consultation_id,
        "patient_report": patient_report,
        "visit_number": len(history) + 1,
        "qa_count": len(qa_pairs)
    })

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AI MEDICAL ASSISTANT - FORM STYLE WITH 10 STATIC QUESTIONS")
    print("=" * 70)
    print("✅ 10 Static Questions (Same Every Time)")
    print("✅ Browser Web Speech API (No Whisper)")
    print("✅ Gemma3 Report Generation")
    print("✅ MySQL Encrypted Storage")
    print("✅ Form-Based UI Compatible")
    print("=" * 70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
