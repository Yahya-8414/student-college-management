# Student College Management System

A web-based **Student College Management System** built with Python and Flask. The application provides separate dashboards and functionality for **students, faculty, and administrators**, making it easier to manage academic information, attendance, grades, batches, timetables, syllabi, and performance reports.

## 📌 Features

### 👨‍🎓 Student

* Student dashboard
* View attendance
* View grades and results
* View academic performance
* View timetable
* View syllabus
* Access performance reports

### 👨‍🏫 Faculty

* Faculty dashboard
* Mark and manage student attendance
* Enter and manage grades
* View student academic information
* Access performance-related information

### 🛠️ Administrator

* Admin dashboard
* Manage users
* Create and manage batches
* View students
* Manage faculty/student accounts
* Upload and manage syllabi
* Upload and manage timetables
* View academic and performance reports

### 🔐 Authentication

* User registration
* User login
* Role-based dashboards
* User profile management

---

## 🗂️ Project Structure

```text
student-college-management/
│
├── app.py                         # Main Flask application
├── collegelogo.emf                # College logo (EMF format)
├── collegelogo.png                # College logo (PNG format)
├── example.png                    # Example/reference image
├── logo.webp                      # Logo image
│
├── static/
│   ├── css/
│   │   └── styles.css             # Application styles
│   │
│   ├── js/
│   │   └── scripts.js             # Client-side JavaScript
│   │
│   └── logo.jpg                   # Static logo
│
└── templates/
    ├── admin_dashboard.html       # Admin dashboard
    ├── attendance.html            # Attendance page
    ├── base.html                  # Base template
    ├── batch.html                 # Batch management
    ├── create_batch.html          # Create batch
    ├── dashboard.html             # General dashboard
    ├── edit_user.html             # Edit user
    ├── faculty_attendance.html    # Faculty attendance management
    ├── faculty_dashboard.html     # Faculty dashboard
    ├── faculty_grades.html        # Faculty grade management
    ├── login.html                 # Login page
    ├── manage_users.html          # User management
    ├── performance.html            # Student performance
    ├── performance_report.html    # Performance report
    ├── register.html              # Registration page
    ├── results.html               # Results page
    ├── student_dashboard.html     # Student dashboard
    ├── syllabus.html              # Syllabus page
    ├── timetable.html             # Timetable page
    ├── upload_syllabus.html       # Upload syllabus
    ├── upload_timetable.html      # Upload timetable
    ├── view_attendance.html       # View attendance
    ├── view_batches.html           # View batches
    ├── view_grades.html            # View grades
    ├── view_reports.html           # View reports
    ├── view_students.html          # View students
    ├── view_syllabus.html          # View syllabus
    └── view_timetable.html         # View timetable
```

---

## ⚙️ Technologies Used

* **Python**
* **Flask**
* **HTML5**
* **CSS3**
* **JavaScript**
* **Jinja2 Templates**

The project uses Flask's template system to dynamically render pages and separates static resources such as CSS, JavaScript, and images into the `static` directory.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd student-college-management
```

Replace `<repository-url>` with the URL of your Git repository.

### 2. Create a virtual environment

It is recommended to use a virtual environment to keep project dependencies isolated.

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

If the project contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If a requirements file has not been created yet, install Flask:

```bash
pip install flask
```

> Additional dependencies should be installed according to the imports used in `app.py`.

---

## ▶️ Running the Application

Run the Flask application with:

```bash
python app.py
```

Or, depending on your Python installation:

```bash
python3 app.py
```

After starting the application, open your browser and visit:

```text
http://127.0.0.1:5000/
```

If `app.py` uses a different port, use the port configured in the application.

---

## 🔑 User Roles

The system is designed around three primary roles:

| Role        | Main Responsibilities                                                  |
| ----------- | ---------------------------------------------------------------------- |
| **Admin**   | Manage users, batches, syllabus, timetable, and reports                |
| **Faculty** | Manage attendance and grades                                           |
| **Student** | View attendance, grades, results, timetable, syllabus, and performance |

Role-based access helps ensure that users see the functionality relevant to their responsibilities.

---

## 📚 Main Modules

### Authentication Module

Handles:

* User registration
* User login
* User authentication
* Role-based access

### Student Management

Allows administrators and faculty to access student-related information.

### Batch Management

Administrators can create and view academic batches.

### Attendance Management

Faculty can manage attendance, while students can view their attendance records.

### Grade & Result Management

Faculty can enter grades, while students can view grades and academic results.

### Performance Management

The system provides performance pages and reports to help monitor student academic progress.

### Syllabus Management

Administrators can upload and manage syllabus information for students and faculty.

### Timetable Management

Administrators can upload timetables, which can then be accessed through the application.

### Reporting

Performance and academic information can be presented through dedicated report pages.

---

## 📁 Static Files

Static resources are stored in the `static` directory:

```text
static/
├── css/
│   └── styles.css
├── js/
│   └── scripts.js
└── logo.jpg
```

* `styles.css` — Controls the visual appearance of the application.
* `scripts.js` — Contains client-side JavaScript functionality.
* `logo.jpg` — Static logo used by the application.

---

## 🖼️ Templates

The application uses Flask/Jinja2 templates stored in the `templates` directory.

`base.html` serves as the common base template, while other HTML files provide pages for individual modules and user roles.

---

## 🔒 Security Recommendations

Before deploying this application to a production environment:

* Use a strong Flask `SECRET_KEY`.
* Never store passwords as plain text.
* Use secure password hashing.
* Validate and sanitize user input.
* Restrict file upload types and sizes.
* Protect administrative routes with authentication and authorization.
* Use HTTPS in production.
* Store sensitive configuration values in environment variables.
* Disable Flask debug mode in production.

For example:

```python
app.run(debug=False)
```

---

## 🛠️ Development

During development, Flask's debug mode can be enabled if it is already supported by the application:

```python
app.run(debug=True)
```

**Do not use debug mode in production.**

When making changes:

1. Update the Flask routes or backend logic in `app.py`.
2. Update the corresponding HTML template in `templates/`.
3. Update styling in `static/css/styles.css`.
4. Update client-side behavior in `static/js/scripts.js`.
5. Run the application and test the affected functionality.

---

## 🧪 Testing

Before deploying, test the major workflows:

* [ ] User registration
* [ ] User login/logout
* [ ] Role-based access
* [ ] Admin dashboard
* [ ] User management
* [ ] Batch creation and viewing
* [ ] Student information
* [ ] Attendance management
* [ ] Grade management
* [ ] Results
* [ ] Performance reports
* [ ] Syllabus upload/viewing
* [ ] Timetable upload/viewing
* [ ] File upload validation
* [ ] Unauthorized route access

---

## 📦 Recommended `requirements.txt`

If Flask is the only external dependency currently used by the application, a basic `requirements.txt` can contain:

```text
Flask
```

Generate an environment-specific dependency list with:

```bash
pip freeze > requirements.txt
```

---

## 🌐 Deployment

For production deployment, the Flask development server should not be used as the primary production server.

A production setup can use:

```text
Browser
   │
   ▼
Web Server / Reverse Proxy
   │
   ▼
WSGI Server
   │
   ▼
Flask Application
```

Possible deployment options include platforms or services that support Python/Flask applications.

Before deployment, configure:

* Production secret key
* Database/storage configuration
* Environment variables
* File upload storage
* HTTPS
* Production WSGI server
* Proper logging
* Access controls

---

## 🔮 Future Enhancements

Possible improvements include:

* Database integration with MySQL/PostgreSQL
* REST API
* Email notifications
* Student/faculty profile pages
* Password reset functionality
* Attendance percentage calculations
* Interactive performance charts
* Export reports to PDF/Excel
* Search and filtering
* Notifications and announcements
* Responsive mobile interface
* Improved authentication and session management
* Automated testing
* Production deployment configuration

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/your-feature
```

3. Make your changes.
4. Test the application.
5. Commit your changes:

```bash
git commit -m "Add your feature"
```

6. Push the branch:

```bash
git push origin feature/your-feature
```

7. Open a Pull Request.


## 📜 Copyright & Registration

This software is registered with the **Copyright Office, Government of India** under the Copyright Act, 1957.

* **Certificate No.:** SW-2025021327  
* **Application No.:** 14253/2025-CO/SW  
* **Date of ROC:** 13/08/2025  
* **Registered Title:** COLLEGE-STUDENT MANAGEMENT SYSTEM  

### Copyright Owners & Authors
1. **Ruzda Jamir Shaikh**
2. **Yahya Irfan Shaikh**
3. **Affan Irfan Shaikh**
4. **Shifa Samreen**
5. **Ayesha Ayajmustak Sayyad**
6. **Prof. Barkha Shahani**
7. **Dr. Sneha Tirth**
8. **Prof. Rupali Maske**
9. **Prof. Sai Takawale**
10. **Dr. Sujeet More**

---

## 📜 Copyright & Registration

This software is registered with the **Copyright Office, Government of India** under the Copyright Act, 1957.

* **Certificate No.:** SW-2025021327  
* **Application No.:** 14253/2025-CO/SW  
* **Date of ROC:** 13/08/2025  
* **Registered Title:** COLLEGE-STUDENT MANAGEMENT SYSTEM  

### Copyright Owners & Authors
1. **Ruzda Jamir Shaikh**
2. **Yahya Irfan Shaikh**
3. **Affan Irfan Shaikh**
4. **Shifa Samreen**
5. **Ayesha Ayajmustak Sayyad**
6. **Prof. Barkha Shahani**
7. **Dr. Sneha Tirth**
8. **Prof. Rupali Maske**
9. **Prof. Sai Takawale**
10. **Dr. Sujeet More**

---

## 📄 License & Terms

All rights reserved © 2025. Unauthorized copying, distribution, modification, or commercial exploitation of this software and its source code is strictly prohibited without explicit written permission from the copyright owners listed above.

---


## 👨‍💻 Author

**Student College Management System**

Developed as a college/academic management web application using Flask, HTML, CSS, and JavaScript.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

For issues or feature requests, open an issue in the project repository.
