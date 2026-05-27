from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__, template_folder='homework-club-prototype', static_folder='homework-club-prototype')
app.secret_key = 'indigenomics_secret_key_123' # In production, use an environment variable

DB_PATH = 'homework_club_hub.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==================== PAGE ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/join')
def join_page():
    return render_template('join.html')

@app.route('/profile')
def profile_page():
    name = request.args.get('name')
    if not name:
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        user_id = session['user_id']
    else:
        conn = get_db_connection()
        user = conn.execute('SELECT user_id FROM users WHERE full_name = ?', (name,)).fetchone()
        conn.close()
        if not user:
            return "User not found", 404
        user_id = user['user_id']
    
    return render_template('profile.html', user_id=user_id)

@app.route('/my-profile')
def my_profile_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('my-profile.html')

@app.route('/my-sessions')
def my_sessions_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('my-sessions.html')

@app.route('/admin')
def admin_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    conn = get_db_connection()
    user = conn.execute('SELECT role FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()
    conn.close()
    if not user or user['role'] != 'admin':
        return redirect(url_for('index'))
    return render_template('admin.html')

@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/booking')
def booking_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('booking.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ==================== API ROUTES ====================

@app.route('/api/join', methods=['POST'])
def join_club():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student_parent')
    subject = data.get('subject', 'None')
    language = data.get('language', 'None')

    if not full_name or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    password_hash = generate_password_hash(password)
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (full_name, email, password_hash, role, subject, language, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (full_name, email, password_hash, role, subject, language, created_at)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Welcome to the club!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['user_id']
        session['full_name'] = user['full_name']
        return jsonify({'message': 'Login successful'}), 200
    
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/me')
def get_me():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    user = conn.execute('SELECT full_name, email, role, created_at, subject, language FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/profile')
def get_profile():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'No name provided'}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT full_name, email, role, created_at, subject, language FROM users WHERE full_name = ?', (name,)).fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/tutors')
def get_tutors():
    subject = request.args.get('subject', 'All Subjects')
    language = request.args.get('language', 'All Backgrounds')
    
    conn = get_db_connection()
    query = 'SELECT * FROM users WHERE role = "volunteer"'
    params = []
    
    if subject != 'All Subjects':
        query += ' AND subject LIKE ?'
        params.append(f'%{subject}%')
    if language != 'All Backgrounds':
        query += ' AND language LIKE ?'
        params.append(f'%{language}%')
        
    tutors = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(t) for t in tutors])

@app.route('/api/ai-match')
def ai_match():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    user = conn.execute('SELECT subject, language FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User profile not found'}), 404

    user_subject = user['subject']
    user_language = user['language']

    # Find best match volunteer based on subject and language
    query = 'SELECT * FROM users WHERE role = "volunteer"'
    volunteers = conn.execute(query).fetchall()
    conn.close()

    if not volunteers:
        return jsonify({'error': 'No volunteers available'}), 404

    best_match = None
    highest_score = -1

    for v in volunteers:
        score = 0
        if v['subject'] == user_subject:
            score += 2
        if v['language'] == user_language:
            score += 1
        
        if score > highest_score:
            highest_score = score
            best_match = v

    if not best_match or highest_score == 0:
        best_match = volunteers[0]
        reasoning = f"Suggested based on general availability in {best_match.get('subject', 'General')}."
        compatibility = "General Match"
    else:
        reasoning = f"Perfect match! {best_match['full_name']} shares your interest in {user_subject} and speaks {user_language}."
        compatibility = "High" if highest_score == 3 else "Good"

    return jsonify({
        'match': dict(best_match),
        'compatibility': compatibility,
        'reasoning': reasoning
    })

# ==================== ADMIN API ====================

@app.route('/api/admin/users')
def admin_users():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    user = conn.execute('SELECT role FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Forbidden'}), 403
    
    all_users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(u) for u in all_users])

@app.route('/api/admin/users/<int:user_id>/verify', methods=['POST'])
def verify_volunteer(user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    user = conn.execute('SELECT role FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Forbidden'}), 403
    
    conn.execute('UPDATE users SET is_verified = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Volunteer verified successfully'})

# ==================== SESSION & FEEDBACK API ====================

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    user = conn.execute('SELECT role FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    if user and user['role'] == 'admin':
        # Admin sees all sessions
        sessions = conn.execute('SELECT * FROM sessions ORDER BY scheduled_time DESC').fetchall()
    else:
        # Users see their own sessions
        # For prototype, return mock data since sessions table may be empty
        sessions = []
    
    conn.close()
    return jsonify([dict(s) for s in sessions])

@app.route('/api/sessions', methods=['POST'])
def create_session():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    tutor_name = data.get('tutor')
    student_name = data.get('student_name')
    parent_name = data.get('parent_name')
    needs = data.get('needs')
    preferred_date = data.get('preferred_date')
    preferred_time = data.get('preferred_time')
    session_type = data.get('session_type', 'online')
    
    if not tutor_name or not student_name or not preferred_date or not preferred_time:
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    tutor = conn.execute('SELECT user_id FROM users WHERE full_name = ?', (tutor_name,)).fetchone()
    
    if not tutor:
        conn.close()
        return jsonify({'error': 'Tutor not found'}), 404
    
    scheduled_time = f"{preferred_date} {preferred_time}"
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO sessions (student_name, parent_name, tutor_id, tutor_name, needs, scheduled_time, session_type, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (student_name, parent_name, tutor['user_id'], tutor_name, needs, scheduled_time, session_type, 'pending', created_at)
        )
        conn.commit()
        session_id = cursor.lastrowid
        conn.close()
        return jsonify({'message': 'Session created', 'session_id': session_id}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<int:session_id>/rate', methods=['POST'])
def rate_session(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    rating = data.get('rating')
    feedback = data.get('feedback')
    
    if not rating or rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    conn = get_db_connection()
    try:
        conn.execute(
            'UPDATE sessions SET rating = ?, feedback = ? WHERE session_id = ?',
            (rating, feedback, session_id)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Rating submitted'}), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<int:session_id>/cancel', methods=['POST'])
def cancel_session(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    try:
        conn.execute(
            'UPDATE sessions SET status = ? WHERE session_id = ?',
            ('cancelled', session_id)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Session cancelled'}), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/stats')
def admin_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    user = conn.execute('SELECT role FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Forbidden'}), 403
    
    total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    volunteers = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'volunteer'").fetchone()[0]
    students = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'student_parent'").fetchone()[0]
    
    # Get subject and language distributions
    subjects = conn.execute('SELECT subject, COUNT(*) as count FROM users WHERE subject IS NOT NULL AND subject != "None" GROUP BY subject').fetchall()
    languages = conn.execute('SELECT language, COUNT(*) as count FROM users WHERE language IS NOT NULL AND language != "None" GROUP BY language').fetchall()
    
    conn.close()
    
    return jsonify({
        'total_users': total_users,
        'volunteers': volunteers,
        'students': students,
        'subjects': [dict(s) for s in subjects],
        'languages': [dict(l) for l in languages]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
