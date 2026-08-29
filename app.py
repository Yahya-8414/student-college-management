from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import datetime
from functools import wraps
import logging
import os

logging.basicConfig(level=logging.INFO)

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session:
                abort(403)
                
            # Convert a single string role into a list automatically so the 'in' check works flawlessly
            roles_list = [allowed_roles] if isinstance(allowed_roles, str) else allowed_roles
            
            if session['role'] not in roles_list:
                abort(403)  # Forbidden if user's role is not in the allowed list
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secure string
app.config["MONGO_URI"] = "mongodb://localhost:27017/college_management"
mongo = PyMongo(app)

# Ensure upload directories exist safely inside static folder
UPLOAD_SYLLABUS_DIR = os.path.join('static', 'syllabi')
UPLOAD_TIMETABLE_DIR = os.path.join('static', 'timetables')
os.makedirs(UPLOAD_SYLLABUS_DIR, exist_ok=True)
os.makedirs(UPLOAD_TIMETABLE_DIR, exist_ok=True)

# Fixed Home route routing
@app.route('/')
def home():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session['role'] == 'faculty':
            return redirect(url_for('faculty_dashboard'))
        elif session['role'] == 'student':
            return redirect(url_for('student_dashboard'))
    return render_template('login.html') # Render login directly to prevent loops

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'role' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = mongo.db.users.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
            'role': role,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        })
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Dashboards
@app.route('/admin_dashboard')
@role_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/faculty_dashboard')
@role_required('faculty')
def faculty_dashboard():
    return render_template('faculty_dashboard.html')

@app.route('/student_dashboard')
@role_required('student')
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/upload_syllabus', methods=['GET', 'POST'])
@role_required('faculty')
def upload_syllabus():
    if request.method == 'POST':
        subject = request.form['subject']
        syllabus_file = request.files['syllabus_file']
        if syllabus_file:
            syllabus_path = os.path.join(UPLOAD_SYLLABUS_DIR, syllabus_file.filename)
            syllabus_file.save(syllabus_path)
            
            mongo.db.syllabi.insert_one({
                'subject': subject,
                'file_path': syllabus_path.replace('\\', '/'),
                'uploaded_at': datetime.datetime.now(),
                'faculty_id': ObjectId(session['user_id'])
            })
            flash('Syllabus uploaded successfully!', 'success')
        return redirect(url_for('upload_syllabus'))
    
    return render_template('upload_syllabus.html')

@app.route('/view_syllabus')
@role_required('student')
def view_syllabus():
    syllabi = mongo.db.syllabi.find()
    return render_template('view_syllabus.html', syllabi=syllabi)

@app.route('/upload_timetable', methods=['GET', 'POST'])
@role_required('faculty')
def upload_timetable():
    if request.method == 'POST':
        timetable_file = request.files['timetable_file']
        if timetable_file:
            timetable_path = os.path.join(UPLOAD_TIMETABLE_DIR, timetable_file.filename)
            timetable_file.save(timetable_path)
            
            mongo.db.timetables.insert_one({
                'file_path': timetable_path.replace('\\', '/'),
                'uploaded_at': datetime.datetime.now(),
                'faculty_id': ObjectId(session['user_id'])
            })
            flash('Timetable uploaded successfully!', 'success')
        return redirect(url_for('upload_timetable'))
    
    return render_template('upload_timetable.html')

@app.route('/view_timetable')
@role_required('student')
def view_timetable():
    timetables = mongo.db.timetables.find()
    return render_template('view_timetable.html', timetables=timetables)

@app.route('/create_batch', methods=['GET', 'POST'])
@role_required('faculty')
def create_batch():
    if request.method == 'POST':
        batch_name = request.form['batch_name']
        course_id = request.form['course_id']
        
        mongo.db.batches.insert_one({
            'batch_name': batch_name,
            'course_id': ObjectId(course_id),
            'created_at': datetime.datetime.now()
        })
        flash('Batch created successfully!', 'success')
        return redirect(url_for('create_batch'))
    
    return render_template('create_batch.html')

@app.route('/view_batches')
@role_required('student')
def view_batches():
    batches = mongo.db.batches.find()
    return render_template('view_batches.html', batches=batches)

# Fixed collection name mismatch (Changed 'performance' to read from 'results')
@app.route('/compute_performance')
@role_required('faculty')
def compute_performance():
    students = mongo.db.users.find({'role': 'student'})
    performance_data = []

    for student in students:
        total_grades = 0
        count = 0
        
        # Read from 'results' using 'user_id' to match faculty insertions
        grades = mongo.db.results.find({'user_id': ObjectId(student['_id'])})
        for record in grades:
            try:
                total_grades += float(record['grade'])
                count += 1
            except (ValueError, TypeError):
                logging.error(f"Error processing grade for student {student['username']}")

        average_grade = total_grades / count if count > 0 else 0
        
        # Attendance calculation
        total_classes = mongo.db.attendance.count_documents({'user_id': ObjectId(student['_id'])})
        attendance_records = mongo.db.attendance.find({'user_id': ObjectId(student['_id'])})
        attended_classes = sum(1 for record in attendance_records if record.get('status') == 'present')
        attendance_rate = (attended_classes / total_classes) * 100 if total_classes > 0 else 0
        
        performance_data.append({
            'student_id': student['_id'],
            'username': student['username'],
            'average_grade': round(average_grade, 2),
            'attendance_rate': round(attendance_rate, 2)
        })
    
    return render_template('performance_report.html', performance_data=performance_data)

@app.route('/logout')
def logout():
    session.clear() # Clear everything cleanly
    return redirect(url_for('login'))

@app.route('/manage_users', methods=['GET', 'POST'])
@role_required('admin')
def manage_users():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
            'role': role,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        })
        flash('User added successfully!', 'success')
        return redirect(url_for('manage_users'))
    
    users = mongo.db.users.find()
    return render_template('manage_users.html', users=users)

@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
@role_required('admin')
def edit_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'username': username, 'email': email, 'role': role, 'updated_at': datetime.datetime.now()}}
        )
        flash('User updated successfully!', 'success')
        return redirect(url_for('manage_users'))
    
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<user_id>', methods=['POST'])
@role_required('admin')
def delete_user(user_id):
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    flash('User deleted successfully!', 'success')
    return redirect(url_for('manage_users'))

@app.route('/view_reports')
@role_required('admin')
def view_reports():
    return render_template('view_reports.html')

@app.route('/faculty_attendance', methods=['GET', 'POST'])
@role_required('faculty') # Or whatever your role decorator is named
def faculty_attendance():
    if request.method == 'POST':
        date = request.form.get('date')
        subject = request.form.get('subject')
        
        # Look through submitted data to capture the dynamic student radio buttons
        for key, value in request.form.items():
            if key.startswith('attendance_'):
                student_id, status = value.split(':')
                mongo.db.attendance.insert_one({
                    'user_id': ObjectId(student_id),
                    'date': datetime.datetime.strptime(date, '%Y-%m-%d'),
                    'subject': subject,
                    'status': status,
                    'created_at': datetime.datetime.now(),
                    'updated_at': datetime.datetime.now()
                })
        
        flash('Attendance recorded successfully!', 'success')
        # CRITICAL FIX 1: Explicit return after handling form submission
        return redirect(url_for('faculty_attendance'))
    
    # --- GET Request Logic ---
    # Fetch your student list to render the empty attendance sheet
    students = list(mongo.db.users.find({'role': 'student'}))
    
    # CRITICAL FIX 2: Explicit return to display the page on normal load
    return render_template('faculty_attendance.html', students=students)

@app.route('/faculty_grades', methods=['GET', 'POST'])
@role_required('faculty')
def faculty_grades():
    if request.method == 'POST':
        subject = request.form['subject']
        
        # Scrape through submitted items to process individual student marks
        for key, value in request.form.items():
            if key.startswith('grade_'):
                student_id = key.split('_')[1]
                grade = value
                
                mongo.db.results.insert_one({
                    'user_id': ObjectId(student_id),
                    'subject': subject,
                    'grade': float(grade), # Guaranteeing float storage for compute_performance calculations
                    'created_at': datetime.datetime.now(),
                    'updated_at': datetime.datetime.now()
                })
        
        flash('Class grades published successfully!', 'success')
        return redirect(url_for('faculty_grades'))
    
    students = mongo.db.users.find({'role': 'student'})
    return render_template('faculty_grades.html', students=students)

@app.route('/view_attendance')
@role_required(['student', 'faculty', 'admin']) # Allow all authenticated roles to hit this route endpoint
def view_attendance():
    user_role = session.get('role')
    
    # If the logged-in user is a student, show ONLY their personal attendance history
    if user_role == 'student':
        attendance_records = mongo.db.attendance.find({'user_id': ObjectId(session['user_id'])}).sort('date', -1)
        return render_template('view_attendance.html', records=attendance_records)
        
    # If the user is Faculty or Admin, pull all student attendance records so they can monitor them
    else:
        # Fetching a master log of all attendance documents to show the faculty member
        attendance_records = list(mongo.db.attendance.find().sort('date', -1))
        
        # We need to map student usernames to these logs so the teacher knows whose record is whose
        for record in attendance_records:
            student = mongo.db.users.find_one({'_id': record.get('user_id')})
            record['username'] = student['username'] if student else "Unknown Student"
            
        # We use a custom faculty-facing viewer template here so it renders a full roster list
        return render_template('faculty_view_attendance.html', records=attendance_records)

@app.route('/view_grades')
@role_required('student')
def view_grades():
    grades = list(mongo.db.results.find({'user_id': ObjectId(session['user_id'])}))
    return render_template('view_grades.html', grades=grades)

@app.route('/view_students')
@role_required('faculty')
def view_students():
    students = mongo.db.users.find({'role': 'student'})
    return render_template('view_students.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)