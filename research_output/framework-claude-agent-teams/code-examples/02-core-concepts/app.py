"""
Sample application for code review team to analyze.
Contains intentional security, performance, and testing issues.
"""

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get users matching search criteria."""
    # ISSUE: SQL injection vulnerability
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    search = request.args.get('search', '')
    query = f"SELECT * FROM users WHERE name LIKE '%{search}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    # ISSUE: Connection not closed (resource leak)
    return jsonify(results)


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.json
    # ISSUE: No input validation
    # ISSUE: SQL injection vulnerability
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO users (name, email) VALUES ('{data['name']}', '{data['email']}')"
    )
    conn.commit()
    # ISSUE: Connection not closed
    return jsonify({"status": "created"}), 201


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user."""
    # ISSUE: No connection pooling (creates new connection each request)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # ISSUE: Should use parameterized query
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    result = cursor.fetchone()
    conn.close()

    if not result:
        # ISSUE: No test for 404 case
        return jsonify({"error": "User not found"}), 404

    return jsonify(result)


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    # ISSUE: No authentication check
    # ISSUE: No authorization check
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})


if __name__ == '__main__':
    # ISSUE: Debug mode in production is a security risk
    app.run(debug=True, host='0.0.0.0')
