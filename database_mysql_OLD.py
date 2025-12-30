"""
MySQL Database for AI Medical Assistant
Stores patient records and consultation history with encryption
FIXED VERSION - Compatible with backend_complete.py
"""

import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import hashlib
from encryption import encryptor  # Import encryption module


class MySQLDatabase:
    def __init__(self):
        """Initialize MySQL connection"""
        self.connection = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Create MySQL connection"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='hari',
                password='2429',  # ← PUT YOUR MYSQL PASSWORD HERE
                database='medical_assistant'
            )
            
            if self.connection.is_connected():
                print("✅ Connected to MySQL database")
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            # Fallback: create database if it doesn't exist
            try:
                self.connection = mysql.connector.connect(
                    host='localhost',
                    user='hari',
                    password='2429'  # ← PUT YOUR MYSQL PASSWORD HERE TOO
                )
                cursor = self.connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS medical_assistant")
                cursor.close()
                self.connection.database = 'medical_assistant'
                print("✅ Database created and connected")
            except Error as e2:
                print(f"❌ Fatal error: {e2}")
    
    def create_tables(self):
        """Create necessary tables"""
        cursor = self.connection.cursor()
        
        # Patients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                date_of_birth DATE NOT NULL,
                age INT NOT NULL,
                sex ENUM('Male', 'Female', 'Other') NOT NULL,
                contact VARCHAR(20) NOT NULL,
                address TEXT,
                weight_kg FLOAT,
                height_cm FLOAT,
                bmi FLOAT,
                registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_name (name),
                INDEX idx_contact (contact)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # Medical History table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id VARCHAR(20) NOT NULL,
                chronic_conditions TEXT,
                allergies TEXT,
                current_medications TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # Medical Records table (encrypted)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_records (
                record_id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id VARCHAR(20) NOT NULL,
                record_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                encrypted_data BLOB NOT NULL,
                encryption_iv VARBINARY(16) NOT NULL,
                record_type ENUM('consultation', 'lab_result', 'prescription', 'diagnosis') NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                INDEX idx_patient_date (patient_id, record_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # ============ FIXED: Consultations table with ALL required columns ============
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
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
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                INDEX idx_patient (patient_id),
                INDEX idx_date (date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        self.connection.commit()
        cursor.close()
        print("✅ Database tables created/verified")
    
    def generate_patient_id(self, name: str) -> str:
        """Generate unique patient ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        hash_input = f"{name}{timestamp}".encode()
        hash_short = hashlib.sha256(hash_input).hexdigest()[:8].upper()
        return f"PT{hash_short}"
    
    def register_patient(self, name: str, dob: str, age: int, sex: str, contact: str, address: str) -> str:
        """Register new patient"""
        cursor = self.connection.cursor()
        patient_id = self.generate_patient_id(name)
        
        try:
            # Insert patient
            cursor.execute("""
                INSERT INTO patients (patient_id, name, date_of_birth, age, sex, contact, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (patient_id, name, dob, age, sex, contact, address))
            
            # Create empty medical history
            cursor.execute("""
                INSERT INTO medical_history (patient_id, chronic_conditions, allergies, current_medications)
                VALUES (%s, %s, %s, %s)
            """, (patient_id, json.dumps([]), json.dumps([]), json.dumps([])))
            
            self.connection.commit()
            print(f"✅ Patient registered: {patient_id}")
            return patient_id
        except Error as e:
            self.connection.rollback()
            print(f"❌ Error registering patient: {e}")
            raise
        finally:
            cursor.close()
    
    def get_patient(self, patient_id: str) -> dict:
        """Get patient information"""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            # Get patient data
            cursor.execute("""
                SELECT p.*, 
                       m.chronic_conditions, m.allergies, m.current_medications
                FROM patients p
                LEFT JOIN medical_history m ON p.patient_id = m.patient_id
                WHERE p.patient_id = %s
            """, (patient_id,))
            
            patient = cursor.fetchone()
            
            if patient:
                # Parse JSON fields
                patient['chronic_conditions'] = json.loads(patient.get('chronic_conditions') or '[]')
                patient['allergies'] = json.loads(patient.get('allergies') or '[]')
                patient['current_medications'] = json.loads(patient.get('current_medications') or '[]')
                
                # Convert date to string
                if patient.get('date_of_birth'):
                    patient['date_of_birth'] = patient['date_of_birth'].strftime('%Y-%m-%d')
                if patient.get('registration_date'):
                    patient['registration_date'] = patient['registration_date'].isoformat()
                
                # Get consultation count
                cursor.execute("""
                    SELECT COUNT(*) as count FROM consultations WHERE patient_id = %s
                """, (patient_id,))
                count_result = cursor.fetchone()
                patient['consultation_count'] = count_result['count'] if count_result else 0
                
                return patient
            return None
        finally:
            cursor.close()
    
    # ============ FIXED: add_consultation() - Uses encrypted columns correctly ============
    def add_consultation(self, patient_id: str, consultation_data: dict) -> str:
        """Add consultation record with encryption"""
        cursor = self.connection.cursor()
        
        try:
            timestamp = datetime.now()
            consultation_id = f"CONS_{timestamp.strftime('%Y%m%d%H%M%S')}"
            
            # Encrypt all sensitive data
            symptoms_encrypted, iv = encryptor.encrypt_data(consultation_data.get('symptoms', {}))
            analysis_encrypted, _ = encryptor.encrypt_data({'analysis': consultation_data.get('analysis', '')})
            diagnosis_encrypted, _ = encryptor.encrypt_data({'diagnosis': consultation_data.get('diagnosis', '')})
            treatment_encrypted, _ = encryptor.encrypt_data({'treatment': consultation_data.get('treatment_summary', '')})
            qa_pairs_encrypted, _ = encryptor.encrypt_data({'qa_pairs': consultation_data.get('qa_pairs', [])})
            full_report_encrypted, _ = encryptor.encrypt_data({'report': consultation_data.get('full_report', '')})
            
            # Insert into encrypted columns
            cursor.execute("""
                INSERT INTO consultations 
                (consultation_id, patient_id, date, chief_complaint, 
                 encrypted_symptoms, encrypted_analysis, encrypted_diagnosis, 
                 encrypted_treatment, encrypted_qa_pairs, encrypted_full_report, encryption_iv)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                consultation_id,
                patient_id,
                timestamp,
                consultation_data.get('chief_complaint'),
                symptoms_encrypted,
                analysis_encrypted,
                diagnosis_encrypted,
                treatment_encrypted,
                qa_pairs_encrypted,
                full_report_encrypted,
                iv
            ))
            
            self.connection.commit()
            print(f"✅ Consultation saved (encrypted): {consultation_id}")
            return consultation_id
        except Error as e:
            self.connection.rollback()
            print(f"❌ Error saving consultation: {e}")
            print(f"    Consultation data keys: {list(consultation_data.keys())}")
            raise
        finally:
            cursor.close()
    
    def get_decrypted_consultation(self, consultation_id: str) -> dict:
        """Get consultation with decrypted data"""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT * FROM consultations WHERE consultation_id = %s
            """, (consultation_id,))
            
            record = cursor.fetchone()
            
            if record:
                iv = record.get('encryption_iv')
                
                # Decrypt sensitive fields
                if record.get('encrypted_symptoms'):
                    record['symptoms'] = encryptor.decrypt_data(record['encrypted_symptoms'], iv)
                if record.get('encrypted_analysis'):
                    record['analysis'] = encryptor.decrypt_data(record['encrypted_analysis'], iv).get('analysis', '')
                if record.get('encrypted_diagnosis'):
                    record['diagnosis'] = encryptor.decrypt_data(record['encrypted_diagnosis'], iv).get('diagnosis', '')
                if record.get('encrypted_treatment'):
                    record['treatment'] = encryptor.decrypt_data(record['encrypted_treatment'], iv).get('treatment', '')
                if record.get('encrypted_qa_pairs'):
                    record['qa_pairs'] = encryptor.decrypt_data(record['encrypted_qa_pairs'], iv).get('qa_pairs', [])
                if record.get('encrypted_full_report'):
                    record['full_report'] = encryptor.decrypt_data(record['encrypted_full_report'], iv).get('report', '')
                
                # Remove encrypted fields from response
                for key in list(record.keys()):
                    if key.startswith('encrypted_') or key == 'encryption_iv':
                        del record[key]
                
                if record.get('date'):
                    record['date'] = record['date'].isoformat()
                
                return record
            return None
        finally:
            cursor.close()
    
    def get_patient_history(self, patient_id: str) -> list:
        """Get patient consultation history"""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT consultation_id, date, chief_complaint
                FROM consultations
                WHERE patient_id = %s
                ORDER BY date DESC
            """, (patient_id,))
            
            history = cursor.fetchall()
            
            # Decrypt each consultation
            for record in history:
                if record.get('date'):
                    record['date'] = record['date'].isoformat()
                
                # Get full decrypted record
                full_record = self.get_decrypted_consultation(record['consultation_id'])
                if full_record:
                    record['diagnosis'] = full_record.get('diagnosis', 'N/A')
                    record['treatment_summary'] = full_record.get('treatment', 'N/A')
            
            return history
        finally:
            cursor.close()
    
    def get_patient_summary(self, patient_id: str) -> dict:
        """Get patient summary for doctor"""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            patient = self.get_patient(patient_id)
            
            if not patient:
                return None
            
            cursor.execute("""
                SELECT consultation_id, date, chief_complaint
                FROM consultations
                WHERE patient_id = %s
                ORDER BY date DESC
                LIMIT 5
            """, (patient_id,))
            
            recent_consultations = cursor.fetchall()
            
            # Decrypt consultations
            for record in recent_consultations:
                if record.get('date'):
                    record['date'] = record['date'].isoformat()
                
                full_record = self.get_decrypted_consultation(record['consultation_id'])
                if full_record:
                    record['diagnosis'] = full_record.get('diagnosis', 'N/A')
            
            return {
                'patient': patient,
                'recent_consultations': recent_consultations,
                'total_visits': patient.get('consultation_count', 0)
            }
        finally:
            cursor.close()
    
    def list_all_patients(self) -> list:
        """List all patients"""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT patient_id, name, age, sex, contact, registration_date
                FROM patients
                ORDER BY registration_date DESC
            """)
            
            patients = cursor.fetchall()
            
            for patient in patients:
                if patient.get('registration_date'):
                    patient['registration_date'] = patient['registration_date'].isoformat()
            
            return patients
        finally:
            cursor.close()
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✅ MySQL connection closed")


# Create global database instance
db = MySQLDatabase()