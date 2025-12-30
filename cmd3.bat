# Terminal 3: VIEW LATEST REPORT
cd D:\etyu\medical_assistant
ls patient_report*.txt | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content
