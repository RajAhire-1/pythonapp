from flask import Flask, render_template_string, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_12345'

# HTML Template with Modern Glass Morphism Design
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glassmorphism Auth</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }

        /* Floating Background Elements */
        .floating-elements {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
        }

        .float {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }

        .float:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }

        .float:nth-child(2) {
            width: 120px;
            height: 120px;
            top: 60%;
            left: 80%;
            animation-delay: 1s;
        }

        .float:nth-child(3) {
            width: 60px;
            height: 60px;
            top: 80%;
            left: 20%;
            animation-delay: 2s;
        }

        .float:nth-child(4) {
            width: 100px;
            height: 100px;
            top: 10%;
            left: 70%;
            animation-delay: 3s;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
            }
            50% {
                transform: translateY(-20px) rotate(180deg);
            }
        }

        .container {
            position: relative;
            width: 1000px;
            max-width: 100%;
            min-height: 600px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .forms-container {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
        }

        .form-control {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 0 10%;
            text-align: center;
            transition: all 0.7s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        .login-form {
            opacity: 1;
            z-index: 2;
            transform: translateX(0);
        }

        .register-form {
            opacity: 0;
            z-index: 1;
            transform: translateX(100px);
        }

        .container.active .login-form {
            opacity: 0;
            z-index: 1;
            transform: translateX(-100px);
        }

        .container.active .register-form {
            opacity: 1;
            z-index: 2;
            transform: translateX(0);
        }

        .form-title {
            font-size: 2.8rem;
            color: white;
            margin-bottom: 15px;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .form-subtitle {
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 40px;
            font-size: 1.1rem;
            font-weight: 300;
        }

        .input-group {
            position: relative;
            margin-bottom: 25px;
            width: 100%;
            max-width: 400px;
        }

        .input-field {
            width: 100%;
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
            outline: none;
            padding: 18px 25px;
            border-radius: 15px;
            color: white;
            font-size: 1rem;
            font-weight: 400;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }

        .input-field:focus {
            background: rgba(255, 255, 255, 0.25);
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }

        .input-field::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }

        .input-icon {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: rgba(255, 255, 255, 0.7);
            transition: all 0.3s ease;
        }

        .input-field:focus + .input-icon {
            color: white;
            transform: translateY(-50%) scale(1.2);
        }

        .submit-btn {
            width: 100%;
            max-width: 400px;
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            border: none;
            padding: 18px;
            border-radius: 15px;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            position: relative;
            overflow: hidden;
        }

        .submit-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s ease;
        }

        .submit-btn:hover::before {
            left: 100%;
        }

        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(255, 107, 107, 0.4);
        }

        .submit-btn:active {
            transform: translateY(-1px);
        }

        .switch-form {
            margin-top: 30px;
            color: white;
            font-weight: 300;
        }

        .switch-form a {
            color: #ff6b6b;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }

        .switch-form a::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0;
            height: 2px;
            background: #ff6b6b;
            transition: width 0.3s ease;
        }

        .switch-form a:hover::after {
            width: 100%;
        }

        .panels-container {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            pointer-events: none;
        }

        .panel {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 45%;
            padding: 0 5%;
            text-align: center;
            z-index: 6;
            transition: all 0.7s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            pointer-events: all;
        }

        .left-panel {
            transform: translateX(0);
            opacity: 1;
        }

        .right-panel {
            transform: translateX(100px);
            opacity: 0;
        }

        .container.active .left-panel {
            transform: translateX(-100px);
            opacity: 0;
        }

        .container.active .right-panel {
            transform: translateX(0);
            opacity: 1;
        }

        .panel-content {
            color: white;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
        }

        .panel h3 {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 20px;
        }

        .panel p {
            font-size: 1.1rem;
            margin-bottom: 30px;
            opacity: 0.9;
            font-weight: 300;
        }

        .panel-btn {
            background: transparent;
            border: 2px solid white;
            color: white;
            padding: 12px 35px;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }

        .panel-btn:hover {
            background: white;
            color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }

        /* Social Icons */
        .social-container {
            margin: 25px 0;
        }

        .social-icons {
            display: flex;
            gap: 15px;
            justify-content: center;
        }

        .social-icon {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }

        .social-icon:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-3px) rotate(10deg);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }

        /* Notification Styles */
        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 20px 30px;
            border-radius: 15px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            transform: translateX(400px) scale(0.8);
            transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }

        .notification.show {
            transform: translateX(0) scale(1);
        }

        .notification.success {
            background: linear-gradient(135deg, #00b894, #55efc4);
        }

        .notification.error {
            background: linear-gradient(135deg, #ff7675, #fd79a8);
        }

        /* Loading animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Responsive Design */
        @media (max-width: 900px) {
            .container {
                min-height: 800px;
                height: auto;
                margin: 20px;
            }

            .panels-container {
                flex-direction: column;
                justify-content: space-between;
            }

            .panel {
                width: 100%;
                padding: 2rem 8%;
            }

            .left-panel {
                order: 2;
            }

            .right-panel {
                order: 1;
            }

            .form-title {
                font-size: 2.2rem;
            }
        }

        @media (max-width: 570px) {
            .form-control {
                padding: 0 1.5rem;
            }

            .panel {
                padding: 1rem;
            }

            .form-title {
                font-size: 1.8rem;
            }

            .panel h3 {
                font-size: 1.6rem;
            }
        }
    </style>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <!-- Floating Background Elements -->
    <div class="floating-elements">
        <div class="float"></div>
        <div class="float"></div>
        <div class="float"></div>
        <div class="float"></div>
    </div>

    <!-- Notification Container -->
    <div id="notification" class="notification"></div>

    <div class="container" id="container">
        <div class="forms-container">
            <!-- Login Form -->
            <div class="form-control login-form">
                <h2 class="form-title">Welcome Back!</h2>
                <p class="form-subtitle">Sign in to your account</p>
                
                <div class="social-container">
                    <div class="social-icons">
                        <a href="#" class="social-icon">
                            <i class="fab fa-google"></i>
                        </a>
                        <a href="#" class="social-icon">
                            <i class="fab fa-facebook-f"></i>
                        </a>
                        <a href="#" class="social-icon">
                            <i class="fab fa-twitter"></i>
                        </a>
                    </div>
                </div>
                
                <span style="color: rgba(255,255,255,0.7); margin: 15px 0;">or use your email</span>
                
                <form id="loginForm">
                    <div class="input-group">
                        <input type="text" class="input-field" placeholder="Username or Email" required>
                        <i class="fas fa-user input-icon"></i>
                    </div>
                    <div class="input-group">
                        <input type="password" class="input-field" placeholder="Password" required>
                        <i class="fas fa-lock input-icon"></i>
                    </div>
                    <button type="submit" class="submit-btn">Sign In</button>
                </form>
                
                <div class="switch-form">
                    Don't have an account? <a id="show-register">Sign Up</a>
                </div>
            </div>

            <!-- Registration Form -->
            <div class="form-control register-form">
                <h2 class="form-title">Create Account</h2>
                <p class="form-subtitle">Join our community today</p>
                
                <div class="social-container">
                    <div class="social-icons">
                        <a href="#" class="social-icon">
                            <i class="fab fa-google"></i>
                        </a>
                        <a href="#" class="social-icon">
                            <i class="fab fa-facebook-f"></i>
                        </a>
                        <a href="#" class="social-icon">
                            <i class="fab fa-twitter"></i>
                        </a>
                    </div>
                </div>
                
                <span style="color: rgba(255,255,255,0.7); margin: 15px 0;">or use your email</span>
                
                <form id="registerForm">
                    <div class="input-group">
                        <input type="text" class="input-field" placeholder="Full Name" required>
                        <i class="fas fa-user input-icon"></i>
                    </div>
                    <div class="input-group">
                        <input type="email" class="input-field" placeholder="Email" required>
                        <i class="fas fa-envelope input-icon"></i>
                    </div>
                    <div class="input-group">
                        <input type="text" class="input-field" placeholder="Username" required>
                        <i class="fas fa-at input-icon"></i>
                    </div>
                    <div class="input-group">
                        <input type="password" class="input-field" placeholder="Password" required>
                        <i class="fas fa-lock input-icon"></i>
                    </div>
                    <div class="input-group">
                        <input type="password" class="input-field" placeholder="Confirm Password" required>
                        <i class="fas fa-lock input-icon"></i>
                    </div>
                    <button type="submit" class="submit-btn">Create Account</button>
                </form>
                
                <div class="switch-form">
                    Already have an account? <a id="show-login">Sign In</a>
                </div>
            </div>
        </div>

        <div class="panels-container">
            <!-- Left Panel (Login) -->
            <div class="panel left-panel">
                <div class="panel-content">
                    <h3>New Here?</h3>
                    <p>Create an account and discover amazing features!</p>
                    <button class="panel-btn" id="register-btn">Sign Up</button>
                </div>
            </div>

            <!-- Right Panel (Register) -->
            <div class="panel right-panel">
                <div class="panel-content">
                    <h3>One of Us?</h3>
                    <p>If you already have an account, just sign in.</p>
                    <button class="panel-btn" id="login-btn">Sign In</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const container = document.getElementById('container');
            const showRegister = document.getElementById('show-register');
            const showLogin = document.getElementById('show-login');
            const registerBtn = document.getElementById('register-btn');
            const loginBtn = document.getElementById('login-btn');
            const loginForm = document.getElementById('loginForm');
            const registerForm = document.getElementById('registerForm');
            const successMessage = document.getElementById('notification');

            // Switch to Register Form
            showRegister.addEventListener('click', () => {
                container.classList.add('active');
            });

            registerBtn.addEventListener('click', () => {
                container.classList.add('active');
            });

            // Switch to Login Form
            showLogin.addEventListener('click', () => {
                container.classList.remove('active');
            });

            loginBtn.addEventListener('click', () => {
                container.classList.remove('active');
            });

            // Form Submission
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
                    showNotification('An error occurred. Please try again.', 'error');
                } finally {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }
            });

            // Handle signup form submission
            registerForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
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
                            container.classList.remove('active');
                            registerForm.reset();
                        }, 2000);
                    } else {
                        showNotification(data.message, 'error');
                    }
                } catch (error) {
                    showNotification('An error occurred. Please try again.', 'error');
                } finally {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }
            });

            // Show notification
            function showNotification(message, type = 'success') {
                const notification = document.getElementById('notification');
                notification.textContent = message;
                notification.className = `notification ${type} show`;
                
                setTimeout(() => {
                    notification.classList.remove('show');
                }, 4000);
            }

            // Add input animations
            const inputs = document.querySelectorAll('.input-field');
            
            inputs.forEach(input => {
                input.addEventListener('focus', () => {
                    input.parentElement.style.transform = 'translateY(-5px)';
                });
                
                input.addEventListener('blur', () => {
                    input.parentElement.style.transform = 'translateY(0)';
                });
            });

            // Add hover effect to buttons
            const buttons = document.querySelectorAll('button');
            buttons.forEach(button => {
                button.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-3px)';
                });
                
                button.addEventListener('mouseleave', function() {
                    if (!this.disabled) {
                        this.style.transform = 'translateY(0)';
                    }
                });
            });
        });
    </script>
</body>
</html>
'''

# Dashboard HTML with Glass Morphism
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }

        .floating-elements {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
        }

        .float {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }

        .float:nth-child(1) {
            width: 100px;
            height: 100px;
            top: 10%;
            left: 20%;
            animation-delay: 0s;
        }

        .float:nth-child(2) {
            width: 150px;
            height: 150px;
            top: 60%;
            left: 70%;
            animation-delay: 2s;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
            }
            50% {
                transform: translateY(-20px) rotate(180deg);
            }
        }

        .dashboard-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            padding: 50px;
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 600px;
            width: 90%;
            position: relative;
            overflow: hidden;
        }

        .dashboard-container::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #ff6b6b, #667eea, #764ba2);
            z-index: -1;
            animation: borderGlow 3s linear infinite;
            background-size: 400%;
            border-radius: 27px;
            opacity: 0.7;
        }

        @keyframes borderGlow {
            0% { background-position: 0 0; }
            50% { background-position: 400% 0; }
            100% { background-position: 0 0; }
        }

        .welcome-message {
            font-size: 2.8rem;
            color: white;
            margin-bottom: 20px;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .dashboard-container p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2rem;
            margin-bottom: 30px;
            font-weight: 300;
        }

        .logout-btn {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 25px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .logout-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s ease;
        }

        .logout-btn:hover::before {
            left: 100%;
        }

        .logout-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(255, 107, 107, 0.4);
        }
    </style>
</head>
<body>
    <!-- Floating Background Elements -->
    <div class="floating-elements">
        <div class="float"></div>
        <div class="float"></div>
    </div>
    
    <div class="dashboard-container">
        <h1 class="welcome-message">Welcome, {{ username }}! 🎉</h1>
        <p>You have successfully logged into your account.</p>
        <a href="/logout" class="logout-btn">Logout</a>
    </div>
</body>
</html>
'''

# Database setup
def init_db():
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

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password!'})

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters long!'})
        
        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match!'})
        
        hashed_password = generate_password_hash(password)
        
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
    if 'user_id' in session:
        return render_template_string(DASHBOARD_HTML, username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/check_db')
def check_db():
    """Route to check database contents (for debugging)"""
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, email, created_at FROM users').fetchall()
    conn.close()
    
    users_list = []
    for user in users:
        users_list.append(dict(user))
    
    return jsonify({'users': users_list})

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
    print("Starting Flask application...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)