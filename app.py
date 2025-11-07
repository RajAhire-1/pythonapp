from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import secrets
from datetime import timedelta
import re

app = Flask(__name__)
# Generate a secure secret key (change this in production!)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# HTML Template with improved styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login & Signup</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
            width: 850px;
            max-width: 100%;
            min-height: 550px;
        }

        .form-container {
            position: absolute;
            top: 0;
            height: 100%;
            transition: all 0.6s ease-in-out;
        }

        .sign-in-container {
            left: 0;
            width: 50%;
            z-index: 2;
        }

        .container.right-panel-active .sign-in-container {
            transform: translateX(100%);
        }

        .sign-up-container {
            left: 0;
            width: 50%;
            opacity: 0;
            z-index: 1;
        }

        .container.right-panel-active .sign-up-container {
            transform: translateX(100%);
            opacity: 1;
            z-index: 5;
            animation: show 0.6s;
        }

        @keyframes show {
            0%, 49.99% {
                opacity: 0;
                z-index: 1;
            }
            50%, 100% {
                opacity: 1;
                z-index: 5;
            }
        }

        form {
            background-color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 0 50px;
            height: 100%;
            text-align: center;
        }

        h1 {
            font-weight: 700;
            margin-bottom: 10px;
            color: #333;
            font-size: 2em;
        }

        .subtitle {
            font-size: 14px;
            color: #666;
            margin-bottom: 20px;
        }

        .input-group {
            position: relative;
            width: 100%;
            margin: 10px 0;
        }

        input {
            background-color: #f0f0f0;
            border: 2px solid transparent;
            padding: 14px 15px;
            width: 100%;
            border-radius: 10px;
            font-family: 'Poppins', sans-serif;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: #667eea;
            background-color: #fff;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }

        .password-toggle {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            color: #999;
            transition: color 0.3s;
        }

        .password-toggle:hover {
            color: #667eea;
        }

        button {
            border-radius: 25px;
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #FFFFFF;
            font-size: 13px;
            font-weight: 600;
            padding: 14px 50px;
            letter-spacing: 1px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            cursor: pointer;
            margin-top: 15px;
        }

        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        button:active {
            transform: translateY(-1px);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        button.ghost {
            background: transparent;
            border: 2px solid #FFFFFF;
        }

        button.ghost:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        a {
            color: #667eea;
            font-size: 13px;
            text-decoration: none;
            margin: 15px 0;
            transition: color 0.3s;
        }

        a:hover {
            color: #764ba2;
            text-decoration: underline;
        }

        .overlay-container {
            position: absolute;
            top: 0;
            left: 50%;
            width: 50%;
            height: 100%;
            overflow: hidden;
            transition: transform 0.6s ease-in-out;
            z-index: 100;
        }

        .container.right-panel-active .overlay-container {
            transform: translateX(-100%);
        }

        .overlay {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #FFFFFF;
            position: relative;
            left: -100%;
            height: 100%;
            width: 200%;
            transform: translateX(0);
            transition: transform 0.6s ease-in-out;
        }

        .container.right-panel-active .overlay {
            transform: translateX(50%);
        }

        .overlay-panel {
            position: absolute;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 0 40px;
            text-align: center;
            top: 0;
            height: 100%;
            width: 50%;
            transform: translateX(0);
            transition: transform 0.6s ease-in-out;
        }

        .overlay-panel h1 {
            color: white;
        }

        .overlay-panel p {
            font-size: 15px;
            font-weight: 300;
            line-height: 24px;
            margin: 20px 0 30px;
        }

        .overlay-left {
            transform: translateX(-20%);
        }

        .container.right-panel-active .overlay-left {
            transform: translateX(0);
        }

        .overlay-right {
            right: 0;
            transform: translateX(0);
        }

        .container.right-panel-active .overlay-right {
            transform: translateX(20%);
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            transform: translateX(400px);
            transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .notification.show {
            transform: translateX(0);
        }

        .notification.success {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }

        .notification.error {
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        }

        .loading {
            display: inline-block;
            width: 18px;
            height: 18px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #ffffff;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .strength-meter {
            width: 100%;
            height: 4px;
            background: #e0e0e0;
            border-radius: 2px;
            margin-top: 5px;
            overflow: hidden;
        }

        .strength-meter-fill {
            height: 100%;
            width: 0%;
            transition: all 0.3s ease;
            border-radius: 2px;
        }

        .strength-weak { background: #f44336; width: 33%; }
        .strength-medium { background: #ff9800; width: 66%; }
        .strength-strong { background: #4caf50; width: 100%; }

        @media (max-width: 768px) {
            .container {
                width: 100%;
                min-height: 600px;
            }
            
            .form-container {
                width: 100% !important;
            }
            
            .overlay-container {
                display: none;
            }
            
            .sign-in-container,
            .sign-up-container {
                width: 100%;
            }
            
            .container.right-panel-active .sign-in-container {
                transform: translateX(-100%);
                opacity: 0;
            }
            
            .container.right-panel-active .sign-up-container {
                transform: translateX(0);
            }

            form {
                padding: 0 30px;
            }

            .mobile-toggle {
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #667eea;
                font-size: 14px;
            }
        }

        .mobile-toggle {
            display: none;
        }
    </style>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="container" id="container">
        <div class="form-container sign-up-container">
            <form id="signupForm">
                <h1>Create Account</h1>
                <p class="subtitle">Sign up to get started</p>
                
                <div class="input-group">
                    <input type="text" name="username" placeholder="Username" required minlength="3" />
                </div>
                
                <div class="input-group">
                    <input type="email" name="email" placeholder="Email" required />
                </div>
                
                <div class="input-group">
                    <input type="password" id="signupPassword" name="password" placeholder="Password" required minlength="6" />
                    <i class="fas fa-eye password-toggle" onclick="togglePassword('signupPassword')"></i>
                    <div class="strength-meter">
                        <div class="strength-meter-fill" id="strengthMeter"></div>
                    </div>
                </div>
                
                <div class="input-group">
                    <input type="password" id="confirmPassword" name="confirm_password" placeholder="Confirm Password" required />
                    <i class="fas fa-eye password-toggle" onclick="togglePassword('confirmPassword')"></i>
                </div>
                
                <button type="submit">Sign Up</button>
                <div class="mobile-toggle">
                    Already have an account? <a href="#" onclick="toggleForms(); return false;">Sign In</a>
                </div>
            </form>
        </div>
        
        <div class="form-container sign-in-container">
            <form id="loginForm">
                <h1>Welcome Back</h1>
                <p class="subtitle">Sign in to your account</p>
                
                <div class="input-group">
                    <input type="text" name="username" placeholder="Username" required />
                </div>
                
                <div class="input-group">
                    <input type="password" id="loginPassword" name="password" placeholder="Password" required />
                    <i class="fas fa-eye password-toggle" onclick="togglePassword('loginPassword')"></i>
                </div>
                
                <a href="#">Forgot your password?</a>
                <button type="submit">Sign In</button>
                <div class="mobile-toggle">
                    Don't have an account? <a href="#" onclick="toggleForms(); return false;">Sign Up</a>
                </div>
            </form>
        </div>
        
        <div class="overlay-container">
            <div class="overlay">
                <div class="overlay-panel overlay-left">
                    <h1>Welcome Back!</h1>
                    <p>To keep connected with us please login with your personal info</p>
                    <button class="ghost" id="signIn">Sign In</button>
                </div>
                <div class="overlay-panel overlay-right">
                    <h1>Hello, Friend!</h1>
                    <p>Enter your personal details and start your journey with us</p>
                    <button class="ghost" id="signUp">Sign Up</button>
                </div>
            </div>
        </div>
    </div>

    <div id="notification" class="notification"></div>

    <script>
        const container = document.getElementById('container');
        const signUpButton = document.getElementById('signUp');
        const signInButton = document.getElementById('signIn');
        const loginForm = document.getElementById('loginForm');
        const signupForm = document.getElementById('signupForm');
        const signupPassword = document.getElementById('signupPassword');
        const strengthMeter = document.getElementById('strengthMeter');

        if (signUpButton) {
            signUpButton.addEventListener('click', () => {
                container.classList.add('right-panel-active');
            });
        }

        if (signInButton) {
            signInButton.addEventListener('click', () => {
                container.classList.remove('right-panel-active');
            });
        }

        function toggleForms() {
            container.classList.toggle('right-panel-active');
        }

        function togglePassword(inputId) {
            const input = document.getElementById(inputId);
            const icon = input.nextElementSibling;
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        }

        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${type} show`;
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 4000);
        }

        // Password strength meter
        if (signupPassword) {
            signupPassword.addEventListener('input', function() {
                const password = this.value;
                let strength = 0;
                
                if (password.length >= 6) strength++;
                if (password.length >= 10) strength++;
                if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
                if (/\d/.test(password)) strength++;
                if (/[^a-zA-Z0-9]/.test(password)) strength++;
                
                strengthMeter.className = 'strength-meter-fill';
                
                if (strength <= 2) {
                    strengthMeter.classList.add('strength-weak');
                } else if (strength <= 4) {
                    strengthMeter.classList.add('strength-medium');
                } else {
                    strengthMeter.classList.add('strength-strong');
                }
            });
        }

        // Login form submission
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<div class="loading"></div>';
            submitButton.disabled = true;

            const formData = new FormData(this);
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showNotification(data.message, 'success');
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1500);
                } else {
                    showNotification(data.message, 'error');
                }
            } catch (error) {
                showNotification('Connection error. Please try again.', 'error');
            } finally {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }
        });

        // Signup form submission
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const password = this.querySelector('[name="password"]').value;
            const confirmPassword = this.querySelector('[name="confirm_password"]').value;
            
            if (password !== confirmPassword) {
                showNotification('Passwords do not match!', 'error');
                return;
            }
            
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<div class="loading"></div>';
            submitButton.disabled = true;

            const formData = new FormData(this);
            
            try {
                const response = await fetch('/signup', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showNotification(data.message, 'success');
                    setTimeout(() => {
                        container.classList.remove('right-panel-active');
                        signupForm.reset();
                        strengthMeter.className = 'strength-meter-fill';
                    }, 2000);
                } else {
                    showNotification(data.message, 'error');
                }
            } catch (error) {
                showNotification('Connection error. Please try again.', 'error');
            } finally {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }
        });

        // Input animations
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.01)';
                this.parentElement.style.transition = 'transform 0.2s ease';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
    </script>
</body>
</html>
'''

# Dashboard HTML with improved design
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Welcome</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .dashboard-container {
            background: white;
            padding: 50px;
            border-radius: 25px;
            box-shadow: 0 25px 70px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 600px;
            width: 100%;
            animation: fadeInUp 0.6s ease;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 3em;
            color: white;
            font-weight: bold;
        }

        .welcome-message {
            color: #333;
            font-size: 2.2em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .subtitle {
            color: #666;
            font-size: 1.1em;
            margin-bottom: 30px;
            font-weight: 300;
        }

        .user-info {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 30px 0;
            text-align: left;
        }

        .user-info-item {
            display: flex;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }

        .user-info-item:last-child {
            border-bottom: none;
        }

        .user-info-item i {
            font-size: 1.2em;
            color: #667eea;
            margin-right: 15px;
            width: 25px;
        }

        .user-info-label {
            font-weight: 600;
            color: #555;
            margin-right: 10px;
        }

        .user-info-value {
            color: #888;
        }

        .logout-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .logout-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        }

        @media (max-width: 600px) {
            .dashboard-container {
                padding: 30px 20px;
            }

            .welcome-message {
                font-size: 1.8em;
            }

            .subtitle {
                font-size: 1em;
            }
        }
    </style>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="dashboard-container">
        <div class="avatar">{{ username[0].upper() }}</div>
        <h1 class="welcome-message">Welcome, {{ username }}!</h1>
        <p class="subtitle">You're successfully logged in</p>
        
        <div class="user-info">
            <div class="user-info-item">
                <i class="fas fa-user"></i>
                <span class="user-info-label">Username:</span>
                <span class="user-info-value">{{ username }}</span>
            </div>
            <div class="user-info-item">
                <i class="fas fa-envelope"></i>
                <span class="user-info-label">Email:</span>
                <span class="user-info-value">{{ email }}</span>
            </div>
            <div class="user-info-item">
                <i class="fas fa-calendar"></i>
                <span class="user-info-label">Member since:</span>
                <span class="user-info-value">{{ created_at }}</span>
            </div>
        </div>
        
        <a href="/logout" class="logout-btn">
            <i class="fas fa-sign-out-alt"></i> Logout
        </a>
    </div>
</body>
</html>
'''

# Database initialization
def init_db():
    """Initialize the database with users table"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username (alphanumeric and underscores only)"""
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

@app.route('/')
def index():
    """Main page - redirect to dashboard if logged in"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Please fill in all fields!'})
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session.permanent = True
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['email'] = user['email']
        return jsonify({'success': True, 'message': 'Login successful!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password!'})

@app.route('/signup', methods=['POST'])
def signup():
    """Handle user registration"""
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Validation
    if not all([username, email, password, confirm_password]):
        return jsonify({'success': False, 'message': 'Please fill in all fields!'})
    
    if not validate_username(username):
        return jsonify({'success': False, 'message': 'Username must be 3-20 characters (letters, numbers, underscores only)!'})
    
    if not validate_email(email):
        return jsonify({'success': False, 'message': 'Please enter a valid email address!'})
    
    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters long!'})
    
    if password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match!'})
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Registration successful! Please login.'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Username or email already exists!'})

@app.route('/dashboard')
def dashboard():
    """User dashboard - protected route"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    if user:
        return render_template_string(
            DASHBOARD_HTML, 
            username=user['username'],
            email=user['email'],
            created_at=user['created_at'].split()[0] if user['created_at'] else 'N/A'
        )
    
    session.clear()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/users')
def list_users():
    """API endpoint to list all users (for debugging - remove in production)"""
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, email, created_at FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    
    users_list =