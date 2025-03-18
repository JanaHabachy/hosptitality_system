import pytest
from hospitality_system import *

def test_doctor_instantiation():
    doctor = Doctor(emp_id=1)
    assert doctor.emp_id == 1
    assert doctor.name is not None  

def test_patient_instantiation():
    patient = Patient(patient_id=101)
    assert patient.patient_id == 101
    assert patient.name is not None 

# Test Manager instantiation
def test_manager_instantiation():
    manager = Manager(emp_id=301)
    assert manager.emp_id == 301
    assert manager.name is not None 

# Test DataEntry operations
def test_data_entry_operations():
    data_entry = DataEntry(emp_id=201)
    assert data_entry.emp_id == 201

    # Add record
    record = {"name": "John Doe", "role": "Doctor"}
    result = data_entry.add_record("employees", record)
    assert "Record added" in result

    # Delete record
    with pytest.raises(Exception): 
        data_entry.delete_record("employees", 99999)  

def test_data_entry_invalid_role():
    connection = get_db_connection()
    cursor = connection.cursor()
    with pytest.raises(pymysql.err.DataError):
        cursor.execute("INSERT INTO employees (emp_id, name, role) VALUES (%s, %s, %s)", (999, "John Doe", "Receptionist"))
        connection.commit()
    cursor.close()
    connection.close()

def test_data_entry_print_prescription():
    data_entry = DataEntry(emp_id=201)
    with pytest.raises(Exception):  
        data_entry.print_prescription(99999) 

def test_prescription_factory():
    prescription = PrescriptionFactory.create_prescription(101, 1, "Aspirin", "1 tablet daily")
    assert prescription.patient_id == 101
    assert prescription.doctor_id == 1
    assert prescription.medication == "Aspirin"
    assert prescription.dosage == "1 tablet daily"

if __name__ == "__main__":
    pytest.main()