import pymysql
from abc import ABC, abstractmethod

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',  
        password='1234',  
        database='hospitality_system',
        cursorclass=pymysql.cursors.DictCursor
    )

# Abstract Employee class
class Employee(ABC):
    def __init__(self, emp_id: int):
        self.emp_id = emp_id
        self.name = None
        self.role = None
        self.fetch_employee_data()
    
    def fetch_employee_data(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name, role FROM employees WHERE emp_id = %s", (self.emp_id,))
        result = cursor.fetchone()
        if result:
            self.name = result['name']
            self.role = result['role']
        cursor.close()
        connection.close()
    
    @abstractmethod
    def display_info(self):
        pass

# Doctor class inheriting Employee
class Doctor(Employee):
    def __init__(self, emp_id: int):
        super().__init__(emp_id)
        self.specialty = None
        self.patients = []
        self.fetch_doctor_data()

    def fetch_doctor_data(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT specialty FROM doctors WHERE emp_id = %s", (self.emp_id,))
        result = cursor.fetchone()
        if result:
            self.specialty = result['specialty']
        cursor.close()
        connection.close()

    def display_info(self):
        return f"Doctor {self.name}, Specialty: {self.specialty}"

# Patient class
class Patient:
    def __init__(self, patient_id: int):
        self.patient_id = patient_id
        self.name = None
        self.age = None
        self.prescriptions = []
        self.fetch_patient_data()

    def fetch_patient_data(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name, age FROM patients WHERE patient_id = %s", (self.patient_id,))
        result = cursor.fetchone()
        if result:
            self.name = result['name']
            self.age = result['age']
        cursor.close()
        connection.close()

# DataEntry class inheriting Employee
class DataEntry(Employee):
    def __init__(self, emp_id: int):
        super().__init__(emp_id)
    
    def add_record(self, table: str, record: dict):
        connection = get_db_connection()
        cursor = connection.cursor()
        columns = ', '.join(record.keys())
        values = ', '.join(['%s'] * len(record))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        cursor.execute(sql, tuple(record.values()))
        connection.commit()
        cursor.close()
        connection.close()
        return f"Record added to {table}: {record}"
    
    def delete_record(self, table: str, record_id: int):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (record_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return f"Record {record_id} deleted from {table}"
    
    def print_prescription(self, patient_id: int):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM prescriptions WHERE patient_id = %s", (patient_id,))
        prescription = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if prescription:
            print(f"Prescription ID: {prescription['prescription_id']}\n"
                  f"Patient ID: {prescription['patient_id']}\n"
                  f"Doctor ID: {prescription['doctor_id']}\n"
                  f"Medication: {prescription['medication']}\n"
                  f"Dosage: {prescription['dosage']}")
        else:
            raise ValueError(f"No prescription found for Patient ID: {patient_id}")
    
    def display_info(self):
        return f"Data Entry Staff: {self.name}"

# Manager class inheriting Employee
class Manager(Employee):
    def __init__(self, emp_id: int):
        super().__init__(emp_id)

    def display_info(self):
        return f"Manager: {self.name}"

# Prescription Factory
class Prescription:
    def __init__(self, patient_id: int, doctor_id: int, medication: str, dosage: str):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.medication = medication
        self.dosage = dosage
        self.save_to_db()
    
    def save_to_db(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO prescriptions (patient_id, doctor_id, medication, dosage) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (self.patient_id, self.doctor_id, self.medication, self.dosage))
        connection.commit()
        cursor.close()
        connection.close()
    
    def display_info(self):
        return f"Prescription for Patient {self.patient_id} by Doctor {self.doctor_id}: {self.medication} - {self.dosage}"

# Factory Method
class PrescriptionFactory:
    @staticmethod
    def create_prescription(patient_id: int, doctor_id: int, medication: str, dosage: str):
        return Prescription(patient_id, doctor_id, medication, dosage)

# Example Usage
doctor = Doctor(1)
patient = Patient(101)
data_entry = DataEntry(201)

prescription = PrescriptionFactory.create_prescription(patient.patient_id, doctor.emp_id, "Aspirin", "1 tablet daily")
print(data_entry.display_info())
print(doctor.display_info())
