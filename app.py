import tkinter as tk
from tkinter import messagebox
import json
import os
from PIL import Image, ImageTk
import re

class AnimatedLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Login & Registration")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f2f5')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Data file for storing user information
        self.data_file = "users.json"
        self.load_users()
        
        # Colors
        self.primary_color = "#4e54c8"
        self.secondary_color = "#8f94fb"
        self.accent_color = "#ff6b6b"
        self.text_color = "#333333"
        self.light_text = "#ffffff"
        
        # Animation variables
        self.animation_running = False
        self.canvas_items = []
        
        # Create the main container
        self.main_frame = tk.Frame(self.root, bg='#f0f2f5')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show login screen by default
        self.show_login_screen()
        
        # Start background animation
        self.start_background_animation()
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def load_users(self):
        """Load user data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.users = json.load(file)
        else:
            self.users = {}
    
    def save_users(self):
        """Save user data to JSON file"""
        with open(self.data_file, 'w') as file:
            json.dump(self.users, file, indent=4)
    
    def start_background_animation(self):
        """Create animated background with floating shapes"""
        self.canvas = tk.Canvas(self.main_frame, bg='#f0f2f5', highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)
        
        # Create floating shapes
        self.shapes = []
        colors = ['#4e54c8', '#8f94fb', '#ff6b6b', '#6a11cb', '#2575fc']
        
        for _ in range(15):
            x = self.canvas.winfo_reqwidth() * 0.1 + tk._flatten(self.canvas.winfo_geometry())[2] * 0.8 * tk._default_root.random()
            y = self.canvas.winfo_reqheight() * 0.1 + tk._default_root.random() * 0.8 * self.canvas.winfo_reqheight()
            size = 20 + tk._default_root.random() * 40
            color = colors[int(tk._default_root.random() * len(colors))]
            shape_type = tk._default_root.random()
            
            if shape_type < 0.33:
                shape = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            elif shape_type < 0.66:
                shape = self.canvas.create_rectangle(x, y, x+size, y+size, fill=color, outline="")
            else:
                shape = self.canvas.create_polygon(
                    x, y+size/2,
                    x+size/2, y,
                    x+size, y+size/2,
                    x+size/2, y+size,
                    fill=color, outline=""
                )
            
            self.shapes.append({
                'id': shape,
                'dx': (tk._default_root.random() - 0.5) * 2,
                'dy': (tk._default_root.random() - 0.5) * 2,
                'size': size
            })
        
        self.animation_running = True
        self.animate_shapes()
    
    def animate_shapes(self):
        """Animate the floating shapes"""
        if not self.animation_running:
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        for shape in self.shapes:
            self.canvas.move(shape['id'], shape['dx'], shape['dy'])
            x1, y1, x2, y2 = self.canvas.coords(shape['id'])
            
            # Bounce off edges
            if x1 <= 0 or x2 >= canvas_width:
                shape['dx'] *= -1
            if y1 <= 0 or y2 >= canvas_height:
                shape['dy'] *= -1
        
        self.root.after(50, self.animate_shapes)
    
    def stop_animation(self):
        """Stop the background animation"""
        self.animation_running = False
    
    def show_login_screen(self):
        """Display the login screen"""
        self.clear_screen()
        self.stop_animation()
        
        # Create login container
        login_container = tk.Frame(self.main_frame, bg='white', relief='raised', bd=0)
        login_container.place(relx=0.5, rely=0.5, anchor='center', width=400, height=500)
        
        # Title with animation
        title_label = tk.Label(
            login_container, 
            text="Welcome Back!", 
            font=('Arial', 24, 'bold'),
            bg='white',
            fg=self.primary_color
        )
        title_label.pack(pady=(40, 20))
        
        # Subtitle
        subtitle_label = tk.Label(
            login_container,
            text="Sign in to your account",
            font=('Arial', 12),
            bg='white',
            fg=self.text_color
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Username field
        username_frame = tk.Frame(login_container, bg='white')
        username_frame.pack(pady=10, padx=40, fill='x')
        
        username_label = tk.Label(
            username_frame,
            text="Username",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg=self.text_color,
            anchor='w'
        )
        username_label.pack(fill='x')
        
        self.username_entry = tk.Entry(
            username_frame,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground='#dddddd'
        )
        self.username_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.username_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(e, self.username_entry))
        self.username_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(e, self.username_entry))
        
        # Password field
        password_frame = tk.Frame(login_container, bg='white')
        password_frame.pack(pady=10, padx=40, fill='x')
        
        password_label = tk.Label(
            password_frame,
            text="Password",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg=self.text_color,
            anchor='w'
        )
        password_label.pack(fill='x')
        
        self.password_entry = tk.Entry(
            password_frame,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            show='•',
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground='#dddddd'
        )
        self.password_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.password_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(e, self.password_entry))
        self.password_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(e, self.password_entry))
        
        # Remember me and Forgot password
        options_frame = tk.Frame(login_container, bg='white')
        options_frame.pack(pady=10, padx=40, fill='x')
        
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            options_frame,
            text="Remember me",
            variable=self.remember_var,
            bg='white',
            fg=self.text_color,
            font=('Arial', 10),
            selectcolor='white'
        )
        remember_check.pack(side='left')
        
        forgot_label = tk.Label(
            options_frame,
            text="Forgot password?",
            font=('Arial', 10, 'underline'),
            bg='white',
            fg=self.primary_color,
            cursor="hand2"
        )
        forgot_label.pack(side='right')
        forgot_label.bind('<Button-1>', lambda e: self.forgot_password())
        
        # Login button
        login_button = tk.Button(
            login_container,
            text="Sign In",
            font=('Arial', 12, 'bold'),
            bg=self.primary_color,
            fg='white',
            activebackground=self.secondary_color,
            activeforeground='white',
            relief='flat',
            bd=0,
            cursor="hand2",
            command=self.login
        )
        login_button.pack(pady=20, padx=40, fill='x', ipady=12)
        
        # Register link
        register_frame = tk.Frame(login_container, bg='white')
        register_frame.pack(pady=20)
        
        register_label1 = tk.Label(
            register_frame,
            text="Don't have an account?",
            font=('Arial', 10),
            bg='white',
            fg=self.text_color
        )
        register_label1.pack(side='left')
        
        register_label2 = tk.Label(
            register_frame,
            text="Sign Up",
            font=('Arial', 10, 'bold', 'underline'),
            bg='white',
            fg=self.primary_color,
            cursor="hand2"
        )
        register_label2.pack(side='left', padx=(5, 0))
        register_label2.bind('<Button-1>', lambda e: self.show_registration_screen())
        
        # Start animation after UI is created
        self.root.after(100, self.start_background_animation)
    
    def show_registration_screen(self):
        """Display the registration screen"""
        self.clear_screen()
        self.stop_animation()
        
        # Create registration container
        reg_container = tk.Frame(self.main_frame, bg='white', relief='raised', bd=0)
        reg_container.place(relx=0.5, rely=0.5, anchor='center', width=400, height=550)
        
        # Title with animation
        title_label = tk.Label(
            reg_container, 
            text="Create Account", 
            font=('Arial', 24, 'bold'),
            bg='white',
            fg=self.primary_color
        )
        title_label.pack(pady=(30, 20))
        
        # Subtitle
        subtitle_label = tk.Label(
            reg_container,
            text="Sign up for a new account",
            font=('Arial', 12),
            bg='white',
            fg=self.text_color
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Full Name field
        name_frame = tk.Frame(reg_container, bg='white')
        name_frame.pack(pady=8, padx=40, fill='x')
        
        name_label = tk.Label(
            name_frame,
            text="Full Name",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg=self.text_color,
            anchor='w'
        )
        name_label.pack(fill='x')
        
        self.name_entry = tk.Entry(
            name_frame,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground='#dddddd'
        )
        self.name_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.name_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(e, self.name_entry))
        self.name_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(e, self.name_entry))
        
        # Email field
        email_frame = tk.Frame(reg_container, bg='white')
        email_frame.pack(pady=8, padx=40, fill='x')
        
        email_label = tk.Label(
            email_frame,
            text="Email",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg=self.text_color,
            anchor='w'
        )
        email_label.pack(fill='x')
        
        self.email_entry = tk.Entry(
            email_frame,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground='#dddddd'
        )
        self.email_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.email_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(e, self.email_entry))
        self.email_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(e, self.email_entry))
        
        # Username field
        username_frame = tk.Frame(reg_container, bg='white')
        username_frame.pack(pady=8, padx=40, fill='x')
        
        username_label = tk.Label(
            username_frame,
            text="Username",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg=self.text_color,
            anchor='w'
        )
        username_label.pack(fill='x')
        
        self.reg_username_entry = tk.Entry(
            username_frame,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground='#dddddd'
        )
        self.reg_username_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.reg_username_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(e, self.reg_username_entry))
        self.reg_username_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(e, self.reg_username_entry))
        
        # Password field
        password_frame = tk.Frame(reg_container, bg='white')
        password_frame.pack(pady=8, padx=40, fill='x')
        
        password_label = tk.Label(
            password_frame,
            text="Password",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg=self.text_color,
            anchor='w'
        )
        password_label.pack(fill='x')
        
        self.reg_password_entry = tk.Entry(
            password_frame,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            show='•',
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground='#dddddd'
        )
        self.reg_password_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.reg_password_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(e, self.reg_password_entry))
        self.reg_password_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(e, self.reg_password_entry))
        
        # Confirm Password field
        confirm_frame = tk.Frame(reg_container, bg='white')
        confirm_frame.pack(pady=8, padx=40, fill='x')
        
        confirm_label = tk.Label(
            confirm_frame,
            text="Confirm Password",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg=self.text_color,
            anchor='w'
        )
        confirm_label.pack(fill='x')
        
        self.confirm_password_entry = tk.Entry(
            confirm_frame,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            show='•',
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground='#dddddd'
        )
        self.confirm_password_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.confirm_password_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(e, self.confirm_password_entry))
        self.confirm_password_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(e, self.confirm_password_entry))
        
        # Register button
        register_button = tk.Button(
            reg_container,
            text="Create Account",
            font=('Arial', 12, 'bold'),
            bg=self.primary_color,
            fg='white',
            activebackground=self.secondary_color,
            activeforeground='white',
            relief='flat',
            bd=0,
            cursor="hand2",
            command=self.register
        )
        register_button.pack(pady=20, padx=40, fill='x', ipady=12)
        
        # Login link
        login_frame = tk.Frame(reg_container, bg='white')
        login_frame.pack(pady=10)
        
        login_label1 = tk.Label(
            login_frame,
            text="Already have an account?",
            font=('Arial', 10),
            bg='white',
            fg=self.text_color
        )
        login_label1.pack(side='left')
        
        login_label2 = tk.Label(
            login_frame,
            text="Sign In",
            font=('Arial', 10, 'bold', 'underline'),
            bg='white',
            fg=self.primary_color,
            cursor="hand2"
        )
        login_label2.pack(side='left', padx=(5, 0))
        login_label2.bind('<Button-1>', lambda e: self.show_login_screen())
        
        # Start animation after UI is created
        self.root.after(100, self.start_background_animation)
    
    def on_entry_focus_in(self, event, entry):
        """Change border color when entry is focused"""
        entry.configure(highlightbackground=self.primary_color, highlightcolor=self.primary_color)
    
    def on_entry_focus_out(self, event, entry):
        """Change border color when entry loses focus"""
        entry.configure(highlightbackground='#dddddd', highlightcolor='#dddddd')
    
    def clear_screen(self):
        """Clear the current screen"""
        for widget in self.main_frame.winfo_children():
            if widget != self.canvas:
                widget.destroy()
    
    def login(self):
        """Handle login process"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if username in self.users and self.users[username]['password'] == password:
            messagebox.showinfo("Success", f"Welcome back, {self.users[username]['name']}!")
            # Here you would typically open the main application
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self):
        """Handle registration process"""
        name = self.name_entry.get()
        email = self.email_entry.get()
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validation
        if not all([name, email, username, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return
        
        # Save user
        self.users[username] = {
            'name': name,
            'email': email,
            'password': password
        }
        self.save_users()
        
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_screen()
    
    def forgot_password(self):
        """Handle forgot password functionality"""
        messagebox.showinfo("Forgot Password", "Please contact support to reset your password.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimatedLoginApp(root)
    root.mainloop()