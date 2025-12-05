from flask import Flask, jsonify, request
from db_utils import get_db_connection

app = Flask(__name__)

#Get departments
@app.route('/departments', methods=['GET'])
def get_departments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(departments)

#Get employees
@app.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(employees)

#Get employees by query parameters
@app.route('/employees/query', methods=['GET'])
def query_employees():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    position = request.args.get('position')
    department_name = request.args.get('department_name')
    location = request.args.get('location')

    query = "SELECT e.* FROM employees e LEFT JOIN departments d ON e.department_id = d.id WHERE 1=1"
    params = []

    if first_name:
        query += " AND e.first_name = %s"
        params.append(first_name)
    if last_name:
        query += " AND e.last_name = %s"
        params.append(last_name)
    if position:
        query += " AND e.position = %s"
        params.append(position)
    if department_name:
        query += " AND d.name = %s"
        params.append(department_name)
    if location:
        query += " AND d.location = %s"
        params.append(location)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(employees)

#add employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json(force=True)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    position = data.get('position')
    hire_date = data.get('hire_date')
    department_id = data.get('department_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (first_name, last_name, position, hire_date, department_id) VALUES (%s, %s, %s, %s, %s)",
        (first_name, last_name, position, hire_date, department_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Employee added successfully"}), 201



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5005)