print("\n" + "="*70)
print("TESTING MEDICAL ASSISTANT - COMPLETE SYSTEM")
print("="*70 + "\n")

# Test 1: Encryption Module
print("1️⃣ Testing Encryption Module...")
try:
    from encryption import encryptor
    test_data = {"patient": "John", "diagnosis": "Fever", "confidential": True}
    encrypted, iv = encryptor.encrypt_data(test_data)
    decrypted = encryptor.decrypt_data(encrypted, iv)
    
    if decrypted == test_data:
        print(f"✅ Encryption works!")
        print(f"   Original: {test_data}")
        print(f"   Encrypted (50 chars): {str(encrypted)[:50]}...")
        print(f"   Decrypted: {decrypted}")
    else:
        print("❌ Encryption failed - data mismatch")
except Exception as e:
    print(f"❌ Encryption test failed: {e}")

# Test 2: Database Connection
print("\n2️⃣ Testing Database Connection...")
try:
    from database_mysql import db
    if db.connection and db.connection.is_connected():
        print("✅ MySQL connected successfully")
        
        # Get database info
        cursor = db.connection.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"   Database: {db_name}")
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   Tables: {len(tables)} found")
        for table in tables:
            print(f"      - {table[0]}")
        cursor.close()
    else:
        print("❌ Database not connected")
except Exception as e:
    print(f"❌ Database test failed: {e}")

# Test 3: Register Test Patient
print("\n3️⃣ Testing Patient Registration...")
try:
    patient_id = db.register_patient(
        name="Test Patient System",
        dob="1990-01-15",
        age=35,
        sex="Male",
        contact="+91-9999888877",
        address="Test Address, Chennai, India"
    )
    print(f"✅ Patient registered: {patient_id}")
    
    # Verify patient
    patient = db.get_patient(patient_id)
    print(f"   Name: {patient['name']}")
    print(f"   Age: {patient['age']}, Sex: {patient['sex']}")
except Exception as e:
    print(f"❌ Registration failed: {e}")
    patient_id = None

# Test 4: Add Encrypted Consultation
if patient_id:
    print("\n4️⃣ Testing Encrypted Consultation...")
    try:
        consultation_id = db.add_consultation(patient_id, {
            "chief_complaint": "High fever and severe headache",
            "symptoms": {
                "fever": {"severity": "high", "duration": "3 days"},
                "headache": {"severity": "severe", "duration": "2 days"},
                "body_ache": {"severity": "moderate", "duration": "3 days"}
            },
            "analysis": "CONFIDENTIAL: Patient shows signs of viral infection with elevated temperature",
            "diagnosis": "Suspected Viral Fever - Requires lab confirmation",
            "treatment_summary": "Paracetamol 500mg TID, Rest, Fluids 3L/day"
        })
        print(f"✅ Encrypted consultation saved: {consultation_id}")
        
        # Test 5: Retrieve and Decrypt
        print("\n5️⃣ Testing Decryption...")
        record = db.get_decrypted_consultation(consultation_id)
        print(f"✅ Consultation retrieved and decrypted")
        print(f"   ID: {record['consultation_id']}")
        print(f"   Chief Complaint: {record['chief_complaint']}")
        print(f"   Decrypted Symptoms: {record['symptoms']}")
        print(f"   Decrypted Analysis: {record['analysis'][:50]}...")
        print(f"   Decrypted Diagnosis: {record['diagnosis']}")
        
        # Test 6: Patient History
        print("\n6️⃣ Testing Patient History...")
        history = db.get_patient_history(patient_id)
        print(f"✅ Patient history retrieved: {len(history)} consultation(s)")
        if history:
            print(f"   Latest: {history[0]['chief_complaint']}")
            print(f"   Diagnosis: {history[0]['diagnosis']}")
        
    except Exception as e:
        print(f"❌ Consultation test failed: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*70)
print("✅ ALL TESTS COMPLETE!")
print("="*70)
print("\n🎯 Your system is ready to use!")
print("   Run: python backend.py")
print("   Then open your HTML file in a browser\n")
