"""
Generate sample patient symptom descriptions in Tamil, Hindi, and English
For testing without voice input during hackathon
"""

import json
import os

# Sample patient cases
test_cases = {
    "case1_fever_hindi": {
        "language": "hi",
        "text": "मुझे तीन दिन से बुखार है। सिर में बहुत दर्द हो रहा है और खांसी भी आ रही है। शरीर में दर्द है और बहुत कमजोरी महसूस हो रही है। रात को नींद नहीं आती।",
        "translation": "I have had fever for three days. Severe headache and coughing. Body aches and feeling very weak. Not able to sleep at night.",
        "patient_info": {
            "age": 35,
            "sex": "Male",
            "weight": 72,
            "height": 172,
            "medical_history": "Hypertension",
            "medications": "Amlodipine 5mg"
        }
    },
    
    "case2_stomach_tamil": {
        "language": "ta",
        "text": "எனக்கு இரண்டு நாளாக வயிற்று வலி இருக்கிறது. சாப்பிட்ட பிறகு வாந்தி வருகிறது. வயிறு உப்பி இருக்கிறது. எதுவும் சாப்பிட முடியவில்லை.",
        "translation": "I have had stomach pain for two days. Vomiting after eating. Stomach is bloated. Unable to eat anything.",
        "patient_info": {
            "age": 28,
            "sex": "Female",
            "weight": 58,
            "height": 160,
            "medical_history": "None",
            "medications": "None"
        }
    },
    
    "case3_chest_english": {
        "language": "en",
        "text": "I have been experiencing chest pain for the past week. The pain is sharp and gets worse when I breathe deeply. I also feel short of breath sometimes. There's mild discomfort in my left arm.",
        "translation": "Same as above",
        "patient_info": {
            "age": 52,
            "sex": "Male",
            "weight": 85,
            "height": 175,
            "medical_history": "Diabetes, High Cholesterol",
            "medications": "Metformin 500mg, Atorvastatin 10mg"
        }
    },
    
    "case4_joint_hindi": {
        "language": "hi",
        "text": "मेरे घुटनों में बहुत दर्द रहता है। सुबह उठने के बाद अकड़न होती है। सीढ़ियां चढ़ने में परेशानी होती है। हाथों की उंगलियों में भी सूजन है।",
        "translation": "I have severe knee pain. Stiffness after waking up in the morning. Difficulty climbing stairs. Swelling in fingers too.",
        "patient_info": {
            "age": 58,
            "sex": "Female",
            "weight": 68,
            "height": 158,
            "medical_history": "Arthritis",
            "medications": "Diclofenac 50mg"
        }
    },
    
    "case5_breathing_tamil": {
        "language": "ta",
        "text": "எனக்கு சுவாசிக்க சிரமமாக இருக்கிறது। மூச்சு வாங்குகிறது. இருமல் வருகிறது. கபம் வெளியேறுகிறது. இரவில் மூச்சு விட முடியவில்லை.",
        "translation": "I am having difficulty breathing. Feeling breathless. Coughing with phlegm. Unable to breathe properly at night.",
        "patient_info": {
            "age": 45,
            "sex": "Male",
            "weight": 75,
            "height": 168,
            "medical_history": "Asthma",
            "medications": "Salbutamol inhaler"
        }
    }
}

def save_test_cases():
    """Save test cases to JSON file"""
    os.makedirs("test_data", exist_ok=True)
    
    with open("test_data/sample_cases.json", "w", encoding="utf-8") as f:
        json.dump(test_cases, f, ensure_ascii=False, indent=2)
    
    print("✅ Test cases saved to test_data/sample_cases.json")
    
    # Also create individual text files
    for case_name, case_data in test_cases.items():
        filename = f"test_data/{case_name}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(case_data["text"])
        print(f"✅ Created {filename}")

if __name__ == "__main__":
    save_test_cases()
    print("\n🎉 All test files created!")
    print("\nTest cases:")
    for i, (name, data) in enumerate(test_cases.items(), 1):
        print(f"\n{i}. {name}")
        print(f"   Language: {data['language']}")
        print(f"   Patient: {data['patient_info']['age']}y {data['patient_info']['sex']}")
        print(f"   Symptoms: {data['text'][:50]}...")
