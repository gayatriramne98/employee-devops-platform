from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "employee_db"),
        user=os.getenv("DB_USER", "employee_user"),
        password=os.getenv("DB_PASSWORD", "employeepassword")
    )


@app.route("/")
def home():
    return jsonify({
        "message": "Employee DevOps Platform API is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/ready")
def ready():
    return jsonify({
        "status": "ready"
    })


# =========================
# GET - Get all employees
# =========================

@app.route("/employees", methods=["GET"])
def get_employees():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(employees)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================
# POST - Add employee
# =========================

@app.route("/employees", methods=["POST"])
def add_employee():
    try:
        data = request.get_json()

        name = data["name"]
        email = data["email"]
        department = data.get("department")
        role = data.get("role")

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO employees
            (name, email, department, role)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (name, email, department, role)
        )

        connection.commit()

        employee_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Employee added successfully",
            "id": employee_id
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================
# PUT - Update employee
# =========================

@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        department = data.get("department")
        role = data.get("role")

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            UPDATE employees
            SET name = %s,
                email = %s,
                department = %s,
                role = %s
            WHERE id = %s
        """

        cursor.execute(
            query,
            (name, email, department, role, employee_id)
        )

        connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            connection.close()

            return jsonify({
                "error": "Employee not found"
            }), 404

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Employee updated successfully",
            "id": employee_id
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================
# DELETE - Delete employee
# =========================

@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "DELETE FROM employees WHERE id = %s"

        cursor.execute(query, (employee_id,))
        connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            connection.close()

            return jsonify({
                "error": "Employee not found"
            }), 404

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Employee deleted successfully",
            "id": employee_id
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================
# Start Flask application
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )