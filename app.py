from flask import Flask, render_template_string, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_12345'

# HTML Template with New Animations and Colors
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Glow Login & Signup</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            font-family: 'Rajdhani', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
            position: relative;
        }

        /* Cyber Grid Background */
        .cyber-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(90deg, transparent 95%, rgba(0, 255, 255, 0.1) 95%),
                linear-gradient(transparent 95%, rgba(0, 255, 255, 0.1) 95%);
            background-size: 50px 50px;
            animation: gridMove 20s linear infinite;
            z-index: -2;
        }

        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }

        /* Floating Particles */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00ff88;
            border-radius: 50%;
            animation: float 6s infinite ease-in-out;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0) translateX(0);
                opacity: 0;
            }
            10%, 90% {
                opacity: 1;
            }
            50% {
                transform: translateY(-100px) translateX(100px);
            }
        }

        h1 {
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            margin: 0 0 20px 0;
            background: linear-gradient(45deg, #00ff88, #00ccff, #ff00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        p {
            font-size: 14px;
            font-weight: 400;
            line-height: 20px;
            letter-spacing: 0.5px;
            margin: 20px 0 30px;
            color: #b8b8b8;
        }

        span {
            font-size: 12px;
            color: #888;
        }

        a {
            color: #00ff88;
            font-size: 14px;
            text-decoration: none;
            margin: 15px 0;
            transition: all 0.3s ease;
            position: relative;
        }

        a::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0;
            height: 1px;
            background: #00ff88;
            transition: width 0.3s ease;
        }

        a:hover::after {
            width: 100%;
        }

        button {
            border-radius: 25px;
            border: none;
            background: linear-gradient(45deg, #00ff88, #00ccff);
            color: #000;
            font-size: 12px;
            font-weight: bold;
            padding: 12px 45px;
            letter-spacing: 2px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            font-family: 'Orbitron', sans-serif;
        }

        button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: left 0.5s ease;
        }

        button:hover::before {
            left: 100%;
        }

        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 255, 136, 0.3);
        }

        button:active {
            transform: translateY(-1px);
        }

        button.ghost {
            background: transparent;
            border: 2px solid #00ff88;
            color: #00ff88;
        }

        button.ghost:hover {
            background: #00ff88;
            color: #000;
        }

        form {
            background: rgba(15, 12, 41, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 136, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 0 50px;
            height: 100%;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        form::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #00ff88, #00ccff, #ff00ff, #00ff88);
            z-index: -1;
            animation: borderGlow 3s linear infinite;
            background-size: 400%;
            border-radius: 10px;
        }

        @keyframes borderGlow {
            0% { background-position: 0 0; }
            50% { background-position: 400% 0; }
            100% { background-position: 0 0; }
        }

        input {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            padding: 15px 20px;
            margin: 10px 0;
            width: 100%;
            border-radius: 25px;
            font-family: 'Rajdhani', sans-serif;
            color: #fff;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: #00ff88;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
            transform: scale(1.02);
        }

        input::placeholder {
            color: #888;
        }

        .container {
            background: rgba(15, 12, 41, 0.6);
            border-radius: 15px;
            box-shadow: 0 25px 45px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
            width: 900px;
            max-width: 100%;
            min-height: 580px;
            border: 1px solid rgba(0, 255, 136, 0.1);
        }

        .form-container {
            position: absolute;
            top: 0;
            height: 100%;
            transition: all 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        .sign-in-container {
            left: 0;
            width: 50%;
            z-index: 2;
        }

        .container.right-panel-active .sign-in-container {
            transform: translateX(100%) rotateY(10deg);
            opacity: 0;
        }

        .sign-up-container {
            left: 0;
            width: 50%;
            opacity: 0;
            z-index: 1;
            transform: rotateY(-10deg);
        }

        .container.right-panel-active .sign-up-container {
            transform: translateX(100%) rotateY(0deg);
            opacity: 1;
            z-index: 5;
        }

        .overlay-container {
            position: absolute;
            top: 0;
            left: 50%;
            width: 50%;
            height: 100%;
            overflow: hidden;
            transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            z-index: 100;
        }

        .container.right-panel-active .overlay-container{
            transform: translateX(-100%);
        }

        .overlay {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-repeat: no-repeat;
            background-size: cover;
            background-position: 0 0;
            color: #FFFFFF;
            position: relative;
            left: -100%;
            height: 100%;
            width: 200%;
            transform: translateX(0);
            transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
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
            transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
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

        .social-container {
            margin: 25px 0;
        }

        .social-container a {
            border: 1px solid rgba(0, 255, 136, 0.5);
            border-radius: 50%;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            margin: 0 8px;
            height: 45px;
            width: 45px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.1);
        }

        .social-container a:hover {
            background: #00ff88;
            color: #000;
            transform: scale(1.1) rotate(10deg);
            box-shadow: 0 5px 15px rgba(0, 255, 136, 0.4);
        }

        /* Notification Styles */
        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 20px 30px;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            transform: translateX(400px) rotate(10deg);
            transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            font-family: 'Rajdhani', sans-serif;
        }

        .notification.show {
            transform: translateX(0) rotate(0deg);
        }

        .notification.success {
            background: linear-gradient(45deg, #00b09b, #96c93d);
            box-shadow: 0 10px 30px rgba(0, 176, 155, 0.3);
        }

        .notification.error {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            box-shadow: 0 10px 30px rgba(255, 65, 108, 0.3);
        }

        /* Loading animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #00ff88;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Cyber Lines */
        .cyber-line {
            position: absolute;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00ff88, transparent);
            animation: lineScan 2s linear infinite;
        }

        @keyframes lineScan {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        /* Responsive Design */
        @media (max-width: 900px) {
            .container {
                width: 100%;
                height: 100vh;
                border-radius: 0;
            }
            
            .form-container {
                width: 100%;
            }
            
            .overlay-container {
                display: none;
            }
            
            .container.right-panel-active .sign-in-container {
                transform: translateX(100%);
            }
            
            .container.right-panel-active .sign-up-container {
                transform: translateX(0);
                opacity: 1;
            }

            h1 {
                font-size: 1.8em;
            }
        }
    </style>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <!-- Background Elements -->
    <div class="cyber-grid"></div>
    <div class="particles" id="particles"></div>

    <div class="container" id="container">
        <!-- Cyber Lines -->
        <div class="cyber-line" style="top: 20%; width: 80%;"></div>
        <div class="cyber-line" style="top: 50%; width: 60%; animation-delay: 1s;"></div>
        <div class="cyber-line" style="top: 80%; width: 70%; animation-delay: 0.5s;"></div>

        <div class="form-container sign-up-container">
            <form id="signupForm">
                <h1>CREATE ACCOUNT</h1>
                <div class="social-container">
                    <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
                    <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
                </div>
                <span>or use your email for registration</span>
                <input type="text" name="username" placeholder="Username" required />
                <input type="email" name="email" placeholder="Email" required />
                <input type="password" name="password" placeholder="Password" required />
                <input type="password" name="confirm_password" placeholder="Confirm Password" required />
                <button type="submit">SIGN UP</button>
            </form>
        </div>
        <div class="form-container sign-in-container">
            <form id="loginForm">
                <h1>SIGN IN</h1>
                <div class="social-container">
                    <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
                    <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
                </div>
                <span>or use your account</span>
                <input type="text" name="username" placeholder="Username" required />
                <input type="password" name="password" placeholder="Password" required />
                <a href="#">Forgot your password?</a>
                <button type="submit">SIGN IN</button>
            </form>
        </div>
        <div class="overlay-container">
            <div class="overlay">
                <div class="overlay-panel overlay-left">
                    <h1>WELCOME BACK!</h1>
                    <p>To keep connected with us please login with your personal info</p>
                    <button class="ghost" id="signIn">SIGN IN</button>
                </div>
                <div class="overlay-panel overlay-right">
                    <h1>HELLO, FRIEND!</h1>
                    <p>Enter your personal details and start journey with us</p>
                    <button class="ghost" id="signUp">SIGN UP</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Notification Container -->
    <div id="notification" class="notification"></div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const signUpButton = document.getElementById('signUp');
            const signInButton = document.getElementById('signIn');
            const container = document.getElementById('container');
            const loginForm = document.getElementById('loginForm');
            const signupForm = document.getElementById('signupForm');
            const particlesContainer = document.getElementById('particles');

            // Create floating particles
            function createParticles() {
                for (let i = 0; i < 30; i++) {
                    const particle = document.createElement('div');
                    particle.classList.add('particle');
                    particle.style.left = `${Math.random() * 100}%`;
                    particle.style.top = `${Math.random() * 100}%`;
                    particle.style.animationDelay = `${Math.random() * 6}s`;
                    particle.style.animationDuration = `${4 + Math.random() * 4}s`;
                    particlesContainer.appendChild(particle);
                }
            }

            createParticles();

            // Toggle between login and signup forms
            signUpButton.addEventListener('click', () => {
                container.classList.add('right-panel-active');
            });

            signInButton.addEventListener('click', () => {
                container.classList.remove('right-panel-active');
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

            // Handle login form submission
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
            signupForm.addEventListener('submit', async function(e) {
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
                            container.classList.remove('right-panel-active');
                            signupForm.reset();
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

            // Add input animations
            const inputs = document.querySelectorAll('input');
            inputs.forEach(input => {
                input.addEventListener('focus', function() {
                    this.style.transform = 'scale(1.02)';
                    this.style.boxShadow = '0 0 20px rgba(0, 255, 136, 0.4)';
                });
                
                input.addEventListener('blur', function() {
                    this.style.transform = 'scale(1)';
                    this.style.boxShadow = 'none';
                });
            });

            // Add hover effect to buttons
            const buttons = document.querySelectorAll('button');
            buttons.forEach(button => {
                button.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-3px)';
                });
                
                button.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                });
            });
        });
    </script>
</body>
</html>
'''

# Dashboard HTML with New Theme
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Dashboard</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        body {
            font-family: 'Rajdhani', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
            position: relative;
        }

        .cyber-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(90deg, transparent 95%, rgba(0, 255, 255, 0.1) 95%),
                linear-gradient(transparent 95%, rgba(0, 255, 255, 0.1) 95%);
            background-size: 50px 50px;
            animation: gridMove 20s linear infinite;
            z-index: -1;
        }

        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }

        .dashboard-container {
            background: rgba(15, 12, 41, 0.8);
            backdrop-filter: blur(10px);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
            text-align: center;
            max-width: 600px;
            width: 90%;
            border: 1px solid rgba(0, 255, 136, 0.2);
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
            background: linear-gradient(45deg, #00ff88, #00ccff, #ff00ff, #00ff88);
            z-index: -1;
            animation: borderGlow 3s linear infinite;
            background-size: 400%;
            border-radius: 22px;
        }

        @keyframes borderGlow {
            0% { background-position: 0 0; }
            50% { background-position: 400% 0; }
            100% { background-position: 0 0; }
        }

        .welcome-message {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5em;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #00ff88, #00ccff, #ff00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .dashboard-container p {
            color: #b8b8b8;
            font-size: 1.2em;
            margin-bottom: 30px;
        }

        .logout-btn {
            background: linear-gradient(45deg, #00ff88, #00ccff);
            color: #000;
            border: none;
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
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
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: left 0.5s ease;
        }

        .logout-btn:hover::before {
            left: 100%;
        }

        .logout-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(0, 255, 136, 0.4);
        }

        .cyber-line {
            position: absolute;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00ff88, transparent);
            animation: lineScan 2s linear infinite;
        }

        @keyframes lineScan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
    </style>
</head>
<body>
    <div class="cyber-grid"></div>
    <!-- Cyber Lines -->
    <div class="cyber-line" style="top: 30%; width: 80%;"></div>
    <div class="cyber-line" style="top: 70%; width: 60%; animation-delay: 1s;"></div>
    
    <div class="dashboard-container">
        <h1 class="welcome-message">ACCESS GRANTED, {{ username }}! 🚀</h1>
        <p>Welcome to your cyber dashboard. Your journey begins now.</p>
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
            return jsonify({'success': True, 'message': 'Access granted! Welcome back!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials. Access denied!'})

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
            return jsonify({'success': True, 'message': 'Registration successful! System initialized.'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': 'Username or email already exists in the system!'})

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