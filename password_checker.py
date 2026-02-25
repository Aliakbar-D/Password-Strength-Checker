import tkinter as tk
from tkinter import ttk, messagebox
import re
import math
import pyperclip

class PasswordStrengthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Strength Checker")
        self.root.geometry("550x650")
        self.root.resizable(False, False)
        
        # Set color scheme
        self.colors = {
            'bg': '#f5f5f5',
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#00C851',
            'warning': '#ffbb33',
            'danger': '#ff4444',
            'text': '#333333',
            'light': '#f8f9fa',
            'border': '#e0e0e0'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Center the window
        self.center_window()
        
        # Create main frame
        self.create_widgets()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'550x650+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg='white', relief='flat', bd=0)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🔐 Password Strength Checker",
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg=self.colors['text']
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Check your password security in real-time",
            font=('Segoe UI', 10),
            bg='white',
            fg='#666666'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Password input frame
        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(fill='x', pady=(0, 15))
        
        # Password entry
        self.password_var = tk.StringVar()
        self.password_var.trace('w', self.check_strength)
        
        self.password_entry = tk.Entry(
            input_frame,
            textvariable=self.password_var,
            font=('Segoe UI', 12),
            bg=self.colors['light'],
            fg=self.colors['text'],
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightcolor=self.colors['primary'],
            highlightbackground=self.colors['border']
        )
        self.password_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        # Show/Hide password button
        self.show_password = False
        self.toggle_btn = tk.Button(
            input_frame,
            text='👁️',
            font=('Segoe UI', 12),
            bg=self.colors['light'],
            fg=self.colors['text'],
            relief='flat',
            bd=1,
            cursor='hand2',
            command=self.toggle_password
        )
        self.toggle_btn.pack(side='right', padx=(5, 0), ipadx=10, ipady=5)
        
        # Strength meter frame
        meter_frame = tk.Frame(main_frame, bg='white')
        meter_frame.pack(fill='x', pady=(0, 15))
        
        # Strength label
        self.strength_label = tk.Label(
            meter_frame,
            text="Strength:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=self.colors['text']
        )
        self.strength_label.pack(anchor='w')
        
        # Progress bar
        self.progress = ttk.Progressbar(
            meter_frame,
            length=400,
            mode='determinate',
            style='Strength.Horizontal.TProgressbar'
        )
        self.progress.pack(fill='x', pady=(5, 0))
        
        # Strength text
        self.strength_text = tk.Label(
            meter_frame,
            text="Enter a password",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        )
        self.strength_text.pack(pady=(5, 0))
        
        # Criteria frame
        criteria_frame = tk.Frame(main_frame, bg='white')
        criteria_frame.pack(fill='x', pady=(0, 15))
        
        # Create criteria items
        self.criteria = {}
        criteria_list = [
            ('length', '8+ characters'),
            ('uppercase', 'Uppercase letter'),
            ('lowercase', 'Lowercase letter'),
            ('number', 'Number'),
            ('special', 'Special character'),
            ('common', 'No common patterns')
        ]
        
        # Create grid for criteria
        for i, (key, text) in enumerate(criteria_list):
            frame = tk.Frame(criteria_frame, bg='white', relief='solid', bd=1)
            frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky='ew')
            criteria_frame.grid_columnconfigure(i%2, weight=1)
            
            icon = tk.Label(frame, text='⭕', font=('Segoe UI', 12), bg='white')
            icon.pack(side='left', padx=5, pady=5)
            
            label = tk.Label(frame, text=text, font=('Segoe UI', 10), bg='white')
            label.pack(side='left', padx=5, pady=5)
            
            self.criteria[key] = {'frame': frame, 'icon': icon, 'label': label}
        
        # Feedback section
        self.feedback_frame = tk.Frame(main_frame, bg='#fff3cd', relief='solid', bd=1)
        self.feedback_frame.pack(fill='x', pady=(0, 15))
        self.feedback_frame.pack_forget()  # Hide initially
        
        feedback_title = tk.Label(
            self.feedback_frame,
            text='💡 Suggestions to improve:',
            font=('Segoe UI', 10, 'bold'),
            bg='#fff3cd',
            fg='#856404'
        )
        feedback_title.pack(anchor='w', padx=10, pady=(10, 5))
        
        self.feedback_list = tk.Frame(self.feedback_frame, bg='#fff3cd')
        self.feedback_list.pack(fill='x', padx=10, pady=(0, 10))
        
        # Info frame
        info_frame = tk.Frame(main_frame, bg='#e8f4fd', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(0, 15))
        
        # Entropy and crack time
        info_inner = tk.Frame(info_frame, bg='#e8f4fd')
        info_inner.pack(pady=10)
        
        self.entropy_label = tk.Label(
            info_inner,
            text='📊 Entropy: -',
            font=('Segoe UI', 10),
            bg='#e8f4fd',
            fg='#0c5460'
        )
        self.entropy_label.pack(side='left', padx=10)
        
        self.crack_label = tk.Label(
            info_inner,
            text='⏱️ Crack time: -',
            font=('Segoe UI', 10),
            bg='#e8f4fd',
            fg='#0c5460'
        )
        self.crack_label.pack(side='left', padx=10)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill='x', pady=(0, 10))
        
        # Copy button
        self.copy_btn = tk.Button(
            button_frame,
            text='📋 Copy Password',
            font=('Segoe UI', 10),
            bg=self.colors['light'],
            fg=self.colors['text'],
            relief='solid',
            bd=1,
            cursor='hand2',
            command=self.copy_password
        )
        self.copy_btn.pack(side='left', expand=True, fill='x', padx=(0, 5), ipady=5)
        
        # Clear button
        self.clear_btn = tk.Button(
            button_frame,
            text='🗑️ Clear',
            font=('Segoe UI', 10),
            bg=self.colors['light'],
            fg=self.colors['text'],
            relief='solid',
            bd=1,
            cursor='hand2',
            command=self.clear_password
        )
        self.clear_btn.pack(side='left', expand=True, fill='x', padx=(5, 0), ipady=5)
        
        # Configure style for progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Strength.Horizontal.TProgressbar',
            background=self.colors['primary'],
            troughcolor=self.colors['border'],
            bordercolor=self.colors['border'],
            lightcolor=self.colors['primary'],
            darkcolor=self.colors['primary']
        )
    
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password:
            self.password_entry.config(show='*')
            self.toggle_btn.config(text='👁️')
        else:
            self.password_entry.config(show='')
            self.toggle_btn.config(text='🔒')
        self.show_password = not self.show_password
    
    def calculate_entropy(self, password):
        """Calculate password entropy"""
        charset = 0
        if re.search(r'[a-z]', password):
            charset += 26
        if re.search(r'[A-Z]', password):
            charset += 26
        if re.search(r'\d', password):
            charset += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            charset += 32
        
        if charset == 0 or len(password) == 0:
            return 0
        return round(len(password) * math.log2(charset))
    
    def estimate_crack_time(self, entropy):
        """Estimate crack time based on entropy"""
        if entropy == 0:
            return '-'
        if entropy < 28:
            return 'Instant'
        if entropy < 35:
            return 'Minutes'
        if entropy < 60:
            return 'Hours/Days'
        if entropy < 80:
            return 'Years'
        if entropy < 100:
            return 'Centuries'
        return 'Eternity'
    
    def reset_criteria(self):
        """Reset all criteria icons"""
        for key in self.criteria:
            self.criteria[key]['icon'].config(text='⭕')
            self.criteria[key]['frame'].config(bg='white')
            self.criteria[key]['icon'].config(bg='white')
            self.criteria[key]['label'].config(bg='white')
    
    def check_strength(self, *args):
        """Main strength checking function"""
        password = self.password_var.get()
        
        # Reset UI
        self.reset_criteria()
        
        # Hide feedback frame
        self.feedback_frame.pack_forget()
        
        if len(password) == 0:
            self.progress['value'] = 0
            self.strength_text.config(text='Enter a password', fg='#666666', bg='white')
            self.entropy_label.config(text='📊 Entropy: -')
            self.crack_label.config(text='⏱️ Crack time: -')
            return
        
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 25
            self.update_criteria('length', '✅', 'valid')
        elif len(password) >= 8:
            score += 15
            self.update_criteria('length', '⚠️', 'warning')
            feedback.append('Use 12+ characters for better security')
        else:
            self.update_criteria('length', '❌', 'invalid')
            feedback.append('Use at least 8 characters')
        
        # Uppercase check
        if re.search(r'[A-Z]', password):
            score += 15
            self.update_criteria('uppercase', '✅', 'valid')
        else:
            self.update_criteria('uppercase', '❌', 'invalid')
            feedback.append('Add uppercase letters')
        
        # Lowercase check
        if re.search(r'[a-z]', password):
            score += 15
            self.update_criteria('lowercase', '✅', 'valid')
        else:
            self.update_criteria('lowercase', '❌', 'invalid')
            feedback.append('Add lowercase letters')
        
        # Number check
        if re.search(r'\d', password):
            score += 15
            self.update_criteria('number', '✅', 'valid')
        else:
            self.update_criteria('number', '❌', 'invalid')
            feedback.append('Add numbers')
        
        # Special character check
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 20
            self.update_criteria('special', '✅', 'valid')
        else:
            self.update_criteria('special', '❌', 'invalid')
            feedback.append('Add special characters')
        
        # Common patterns check
        common_patterns = ['123', 'abc', 'password', 'qwerty', 'admin', '123456', 'letmein', 'welcome']
        has_common_pattern = any(pattern in password.lower() for pattern in common_patterns)
        
        if has_common_pattern:
            score -= 15
            self.update_criteria('common', '❌', 'invalid')
            feedback.append('Avoid common patterns')
        else:
            self.update_criteria('common', '✅', 'valid')
        
        # Bonus points
        if len(password) >= 16:
            score += 10
        if re.search(r'[A-Z].*[A-Z]', password):
            score += 5
        if re.search(r'\d.*\d', password):
            score += 5
        if re.search(r'[!@#$%^&*(),.?":{}|<>].*[!@#$%^&*(),.?":{}|<>]', password):
            score += 5
        
        # Cap score
        score = max(0, min(100, score))
        
        # Update progress bar
        self.progress['value'] = score
        
        # Calculate entropy
        entropy = self.calculate_entropy(password)
        self.entropy_label.config(text=f'📊 Entropy: {entropy} bits')
        
        # Estimate crack time
        crack_time = self.estimate_crack_time(entropy)
        self.crack_label.config(text=f'⏱️ Crack time: {crack_time}')
        
        # Update strength text and progress bar color
        if score < 40:
            self.strength_text.config(text='Weak Password', fg=self.colors['danger'], bg='#ffebee')
            style = ttk.Style()
            style.configure('Strength.Horizontal.TProgressbar', background=self.colors['danger'])
        elif score < 70:
            self.strength_text.config(text='Medium Password', fg='#ff8800', bg='#fff3e0')
            style = ttk.Style()
            style.configure('Strength.Horizontal.TProgressbar', background=self.colors['warning'])
        else:
            self.strength_text.config(text='Strong Password', fg=self.colors['success'], bg='#e8f5e9')
            style = ttk.Style()
            style.configure('Strength.Horizontal.TProgressbar', background=self.colors['success'])
        
        # Show feedback if any
        if feedback:
            self.feedback_frame.pack(fill='x', pady=(0, 15))
            
            # Clear previous feedback
            for widget in self.feedback_list.winfo_children():
                widget.destroy()
            
            # Add new feedback items
            for item in feedback:
                item_frame = tk.Frame(self.feedback_list, bg='#fff3cd')
                item_frame.pack(fill='x', pady=2)
                
                bullet = tk.Label(item_frame, text='•', font=('Segoe UI', 12), bg='#fff3cd', fg='#856404')
                bullet.pack(side='left', padx=(0, 5))
                
                label = tk.Label(item_frame, text=item, font=('Segoe UI', 10), bg='#fff3cd', fg='#856404')
                label.pack(side='left')
    
    def update_criteria(self, key, icon, status):
        """Update criteria icon and background"""
        self.criteria[key]['icon'].config(text=icon)
        
        if status == 'valid':
            self.criteria[key]['frame'].config(bg='#d4edda')
            self.criteria[key]['icon'].config(bg='#d4edda')
            self.criteria[key]['label'].config(bg='#d4edda')
        elif status == 'invalid':
            self.criteria[key]['frame'].config(bg='#ffebee')
            self.criteria[key]['icon'].config(bg='#ffebee')
            self.criteria[key]['label'].config(bg='#ffebee')
        elif status == 'warning':
            self.criteria[key]['frame'].config(bg='#fff3cd')
            self.criteria[key]['icon'].config(bg='#fff3cd')
            self.criteria[key]['label'].config(bg='#fff3cd')
    
    def copy_password(self):
        """Copy password to clipboard"""
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")
    
    def clear_password(self):
        """Clear password field"""
        self.password_var.set('')
        self.password_entry.focus()

def main():
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()

if __name__ == "__main__":
    # Check if pyperclip is installed, if not, install it
    try:
        import pyperclip
    except ImportError:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
        import pyperclip
    
    main()