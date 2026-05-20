from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, static_folder='public')
CORS(app)

DB_PATH = 'tasks.db'

# ── Database helpers ──────────────────────────────────

def get_db():
    """Open a new database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn

def init_db():
    """Create the tasks table if it doesn't already exist."""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id         INTEGER  PRIMARY KEY AUTOINCREMENT,
            title      TEXT     NOT NULL,
            status     TEXT     DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ── Serve frontend ────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# ── READ — GET all tasks ──────────────────────────────

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM tasks ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# ── CREATE — POST a new task ──────────────────────────

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO tasks (title) VALUES (?)', (title,)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': task_id, 'title': title, 'status': 'pending'}), 201

# ── UPDATE — PUT update task status ──────────────────

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    status = data.get('status')
    conn = get_db()
    conn.execute(
        'UPDATE tasks SET status = ? WHERE id = ?', (status, task_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ── DELETE — remove a task ────────────────────────────

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ── Health check ──────────────────────────────────────

@app.route('/health')
def health():
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.utcnow().isoformat()
    })

# ── Entry point ───────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=3000, debug=False)