import pytest
from src.hospitality_system import *

def test_data_entry_invalid_role():
    connection = get_db_connection()
    cursor = connection.cursor()
    with pytest.raises(pymysql.err.DataError):
        cursor.execute("INSERT INTO employees (emp_id, name, role) VALUES (%s, %s, %s)", (999, "John Doe", "Receptionist"))
        connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    pytest.main()