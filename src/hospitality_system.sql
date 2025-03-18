SET SQL_SAFE_UPDATES = 0;
 
CREATE DATABASE IF NOT EXISTS hospitality_system;
USE hospitality_system;

CREATE TABLE IF NOT EXISTS employees (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    role ENUM('Doctor', 'DataEntry', 'Manager') NOT NULL
);

CREATE TABLE IF NOT EXISTS doctors (
    emp_id INT PRIMARY KEY,
    specialty VARCHAR(255) NOT NULL,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL
);

CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    medication VARCHAR(255) NOT NULL,
    dosage VARCHAR(255) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(emp_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS data_entries (
    emp_id INT PRIMARY KEY,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS managers (
    emp_id INT PRIMARY KEY,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE
);

show tables;

INSERT INTO employees (emp_id, name, role) VALUES (1, 'Amr Metwally', 'Doctor');
INSERT INTO doctors (emp_id, specialty) VALUES (1, 'Cardiology');

INSERT INTO patients (patient_id, name, age) VALUES (101, 'Hania Mohamed', 17);
INSERT INTO employees (emp_id, name,role) VALUES (201, 'Youssef Ahmed', 'DataEntry');
INSERT INTO employees (emp_id, name,role) VALUES (301, 'Toka Hossam', 'Manager');

SELECT * FROM employees WHERE role = 'Doctor';

SELECT * FROM patients;