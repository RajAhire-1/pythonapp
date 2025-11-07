<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Animated Login & Registration</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }

        .container {
            position: relative;
            width: 100%;
            max-width: 1000px;
            min-height: 600px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            animation: containerSlideIn 1s ease-out;
        }

        @keyframes containerSlideIn {
            0% {
                opacity: 0;
                transform: translateY(50px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
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
            transition: all 0.6s ease-in-out;
        }

        .login-form {
            opacity: 1;
            z-index: 2;
        }

        .register-form {
            opacity: 0;
            z-index: 1;
        }

        .container.active .login-form {
            opacity: 0;
            z-index: 1;
            animation: formSlideOut 0.6s ease-in-out;
        }

        .container.active .register-form {
            opacity: 1;
            z-index: 2;
            animation: formSlideIn 0.6s ease-in-out;
        }

        @keyframes formSlideIn {
            0% {
                transform: translateX(100px);
                opacity: 0;
            }
            100% {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes formSlideOut {
            0% {
                transform: translateX(0);
                opacity: 1;
            }
            100% {
                transform: translateX(-100px);
                opacity: 0;
            }
        }

        .form-title {
            font-size: 2.5rem;
            color: white;
            margin-bottom: 20px;
            font-weight: 700;
            position: relative;
            display: inline-block;
        }

        .form-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 4px;
            background: white;
            border-radius: 2px;
            animation: titleUnderline 2s infinite;
        }

        @keyframes titleUnderline {
            0%, 100% {
                width: 60px;
            }
            50% {
                width: 100px;
            }
        }

        .form-subtitle {
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 40px;
            font-size: 1rem;
            animation: subtitleFadeIn 1.5s ease-out;
        }

        @keyframes subtitleFadeIn {
            0% {
                opacity: 0;
                transform: translateY(10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .input-group {
            position: relative;
            margin-bottom: 30px;
            width: 100%;
            max-width: 380px;
            transition: all 0.3s ease;
        }

        .input-field {
            width: 100%;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            outline: none;
            padding: 15px 20px 15px 45px;
            border-radius: 50px;
            color: white;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .input-field:focus {
            background: rgba(255, 255, 255, 0.3);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.4);
            transform: scale(1.02);
        }

        .input-field::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }

        .input-icon {
            position: absolute;
            left: 15px;
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
            max-width: 380px;
            background: white;
            border: none;
            padding: 15px;
            border-radius: 50px;
            color: #6a11cb;
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
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: all 0.5s ease;
        }

        .submit-btn:hover::before {
            left: 100%;
        }

        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 7px 15px rgba(0, 0, 0, 0.3);
        }

        .submit-btn:active {
            transform: translateY(-1px);
        }

        .switch-form {
            margin-top: 30px;
            color: white;
            animation: fadeIn 1s ease-out;
        }

        @keyframes fadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }

        .switch-form a {
            color: white;
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
            background: white;
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
            justify-content: space-around;
        }

        .panel {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 40%;
            padding: 0 5%;
            text-align: center;
            z-index: 6;
            transition: all 0.6s ease-in-out;
        }

        .left-panel {
            pointer-events: none;
            opacity: 1;
        }

        .right-panel {
            pointer-events: none;
            opacity: 0;
        }

        .container.active .left-panel {
            opacity: 0;
            animation: panelSlideOut 0.6s ease-in-out;
        }

        .container.active .right-panel {
            opacity: 1;
            animation: panelSlideIn 0.6s ease-in-out;
        }

        @keyframes panelSlideIn {
            0% {
                transform: translateX(100px);
                opacity: 0;
            }
            100% {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes panelSlideOut {
            0% {
                transform: translateX(0);
                opacity: 1;
            }
            100% {
                transform: translateX(-100px);
                opacity: 0;
            }
        }

        .panel-content {
            color: white;
            transition: all 0.6s ease-in-out;
        }

        .panel h3 {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 15px;
        }

        .panel p {
            font-size: 1rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }

        .panel-btn {
            border: 2px solid white;
            background: transparent;
            color: white;
            padding: 10px 30px;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .panel-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: white;
            transition: all 0.3s ease;
            z-index: -1;
        }

        .panel-btn:hover::before {
            left: 0;
        }

        .panel-btn:hover {
            color: #6a11cb;
        }

        /* Enhanced Animation Elements */
        .animation-circle {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: float 15s infinite ease-in-out;
        }

        .circle-1 {
            width: 200px;
            height: 200px;
            top: 10%;
            left: 5%;
            animation-delay: 0s;
        }

        .circle-2 {
            width: 150px;
            height: 150px;
            top: 60%;
            left: 10%;
            animation-delay: 2s;
        }

        .circle-3 {
            width: 100px;
            height: 100px;
            top: 20%;
            right: 10%;
            animation-delay: 4s;
        }

        .circle-4 {
            width: 120px;
            height: 120px;
            bottom: 10%;
            right: 5%;
            animation-delay: 6s;
        }

        .circle-5 {
            width: 80px;
            height: 80px;
            top: 80%;
            left: 80%;
            animation-delay: 1s;
        }

        .circle-6 {
            width: 180px;
            height: 180px;
            top: 5%;
            right: 15%;
            animation-delay: 3s;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0) translateX(0) rotate(0deg);
            }
            25% {
                transform: translateY(-20px) translateX(10px) rotate(5deg);
            }
            50% {
                transform: translateY(-10px) translateX(-10px) rotate(-5deg);
            }
            75% {
                transform: translateY(20px) translateX(-5px) rotate(3deg);
            }
        }

        /* Enhanced Success Message */
        .success-message {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 25px;
            border-radius: 5px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transform: translateX(150%);
            transition: transform 0.5s ease;
            z-index: 100;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .success-message.show {
            transform: translateX(0);
            animation: messagePulse 2s infinite;
        }

        @keyframes messagePulse {
            0%, 100% {
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }
            50% {
                box-shadow: 0 5px 20px rgba(76, 175, 80, 0.5);
            }
        }

        /* Particle Animation */
        .particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            animation: particleFloat 20s infinite linear;
        }

        @keyframes particleFloat {
            0% {
                transform: translateY(100vh) translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) translateX(100px);
                opacity: 0;
            }
        }

        /* Glow Effect */
        .glow {
            position: absolute;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
            filter: blur(20px);
            animation: glowMove 15s infinite alternate;
            z-index: -1;
        }

        @keyframes glowMove {
            0% {
                transform: translate(10%, 10%);
            }
            100% {
                transform: translate(-10%, -10%);
            }
        }

        /* Responsive Design */
        @media (max-width: 870px) {
            .container {
                min-height: 800px;
                height: auto;
            }

            .panels-container {
                flex-direction: column;
                justify-content: space-between;
            }

            .panel {
                flex-direction: row;
                justify-content: space-around;
                align-items: center;
                width: 100%;
                padding: 2.5rem 8%;
            }

            .left-panel {
                order: 2;
            }

            .right-panel {
                order: 1;
            }

            .panel-content {
                padding-right: 15px;
            }
        }

        @media (max-width: 570px) {
            .form-control {
                padding: 0 1.5rem;
            }

            .panel {
                flex-direction: column;
                padding: 1rem;
            }

            .panel-content {
                padding-right: 0;
                margin-bottom: 20px;
            }
        }
    </style>
</head>
<body>
    <!-- Enhanced Animation Elements -->
    <div class="animation-circle circle-1"></div>
    <div class="animation-circle circle-2"></div>
    <div class="animation-circle circle-3"></div>
    <div class="animation-circle circle-4"></div>
    <div class="animation-circle circle-5"></div>
    <div class="animation-circle circle-6"></div>

    <!-- Particles -->
    <div class="particles" id="particles"></div>

    <!-- Glow Effects -->
    <div class="glow" style="top: 10%; left: 10%;"></div>
    <div class="glow" style="bottom: 10%; right: 10%;"></div>

    <!-- Success Message -->
    <div class="success-message" id="successMessage">
        <i class="fas fa-check-circle"></i>
        <span>Operation completed successfully!</span>
    </div>

    <div class="container" id="container">
        <div class="forms-container">
            <!-- Login Form -->
            <div class="form-control login-form">
                <h2 class="form-title">Welcome Back!</h2>
                <p class="form-subtitle">Please login to your account</p>
                
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
                <p class="form-subtitle">Sign up for a new account</p>
                
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
                    <button type="submit" class="submit-btn">Sign Up</button>
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
                    <h3>New here?</h3>
                    <p>Create an account and discover a great community!</p>
                    <button class="panel-btn" id="register-btn">Sign Up</button>
                </div>
            </div>

            <!-- Right Panel (Register) -->
            <div class="panel right-panel">
                <div class="panel-content">
                    <h3>One of us?</h3>
                    <p>If you already have an account, just sign in.</p>
                    <button class="panel-btn" id="login-btn">Sign In</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // DOM Elements
        const container = document.getElementById('container');
        const showRegister = document.getElementById('show-register');
        const showLogin = document.getElementById('show-login');
        const registerBtn = document.getElementById('register-btn');
        const loginBtn = document.getElementById('login-btn');
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');
        const successMessage = document.getElementById('successMessage');
        const particlesContainer = document.getElementById('particles');

        // Create particles
        function createParticles() {
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.animationDelay = `${Math.random() * 20}s`;
                particle.style.animationDuration = `${15 + Math.random() * 10}s`;
                particlesContainer.appendChild(particle);
            }
        }

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
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            showSuccessMessage('Login successful!');
        });

        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            showSuccessMessage('Registration successful!');
        });

        // Show Success Message
        function showSuccessMessage(message) {
            successMessage.querySelector('span').textContent = message;
            successMessage.classList.add('show');
            
            setTimeout(() => {
                successMessage.classList.remove('show');
            }, 3000);
        }

        // Add floating animation to input fields on focus
        const inputFields = document.querySelectorAll('.input-field');
        
        inputFields.forEach(input => {
            input.addEventListener('focus', () => {
                input.parentElement.style.transform = 'translateY(-5px)';
            });
            
            input.addEventListener('blur', () => {
                input.parentElement.style.transform = 'translateY(0)';
            });
        });

        // Initialize particles
        createParticles();
    </script>
</body>
</html>