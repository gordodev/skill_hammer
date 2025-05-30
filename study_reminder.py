import tkinter as tk
from tkinter import ttk
import json
import random
import time
from datetime import datetime
import threading
import os

class StudyReminder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Study Reminder")
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize variables
        self.correct_count = 0
        self.questions_required = self.config.get('questions_required', 3)
        self.time_remaining = self.config.get('interval_minutes', 10) * 60
        self.quiz_active = False
        self.current_question = None
        
        # Question bank
        self.questions = self.load_questions()
        
        # Setup tray window (small countdown)
        self.setup_tray_window()
        
        # Start countdown
        self.update_countdown()
        
    def load_config(self):
        """Load or create configuration file"""
        config_file = 'study_config.json'
        default_config = {
            'interval_minutes': 10,
            'questions_required': 3,
            'tray_width': 200,
            'tray_height': 50,
            'quiz_width': 800,
            'quiz_height': 600
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for key, value in default_config.items():
                        if key not in loaded_config:
                            loaded_config[key] = value
                    return loaded_config
            else:
                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config
    
    def load_questions(self):
        """Load comprehensive question bank"""
        return [
            # Python Questions
            {
                'category': 'Python',
                'question': 'What is the time complexity of dictionary lookup in Python?',
                'options': ['O(1)', 'O(n)', 'O(log n)', 'O(n²)'],
                'answer': 0,
                'explanation': 'Dictionary lookups in Python are O(1) on average because they use hash tables.'
            },
            {
                'category': 'Python',
                'question': 'Which Python data structure would you use for a FIFO queue?',
                'options': ['list', 'collections.deque', 'set', 'dict'],
                'answer': 1,
                'explanation': 'collections.deque is optimized for FIFO operations with O(1) append and popleft.'
            },
            {
                'category': 'Python',
                'question': 'What is the difference between list.append() and list.extend()?',
                'options': ['No difference', 'append adds one item, extend adds multiple', 'extend is faster', 'append only works with strings'],
                'answer': 1,
                'explanation': 'append() adds a single element to the end, extend() adds all elements from an iterable.'
            },
            {
                'category': 'Python',
                'question': 'In Python, what does the @property decorator do?',
                'options': ['Makes a method static', 'Converts a method to a property', 'Improves performance', 'Adds type hints'],
                'answer': 1,
                'explanation': '@property allows you to access a method like an attribute, enabling getter/setter functionality.'
            },
            {
                'category': 'Python',
                'question': 'What is a generator in Python?',
                'options': ['A function that returns multiple values at once', 'A function that yields values one at a time', 'A class that generates random numbers', 'A module for creating lists'],
                'answer': 1,
                'explanation': 'Generators yield values one at a time using the yield keyword, saving memory for large datasets.'
            },
            
            # SQL Questions
            {
                'category': 'SQL',
                'question': 'Which JOIN returns all rows from both tables?',
                'options': ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL OUTER JOIN'],
                'answer': 3,
                'explanation': 'FULL OUTER JOIN returns all rows from both tables, with NULL values where no match exists.'
            },
            {
                'category': 'SQL',
                'question': 'What SQL statement would you use to add a new column to an existing table?',
                'options': ['INSERT COLUMN', 'ALTER TABLE ADD', 'UPDATE TABLE', 'CREATE COLUMN'],
                'answer': 1,
                'explanation': 'ALTER TABLE table_name ADD column_name datatype; is the correct syntax.'
            },
            {
                'category': 'SQL',
                'question': 'What is the difference between WHERE and HAVING clauses?',
                'options': ['No difference', 'WHERE filters rows, HAVING filters groups', 'HAVING is faster', 'WHERE only works with strings'],
                'answer': 1,
                'explanation': 'WHERE filters rows before grouping, HAVING filters groups after GROUP BY.'
            },
            {
                'category': 'SQL',
                'question': 'Which SQL function would you use to get the current date?',
                'options': ['NOW()', 'GETDATE()', 'CURRENT_DATE', 'All of the above (varies by DBMS)'],
                'answer': 3,
                'explanation': 'Different database systems use different functions: MySQL uses NOW(), SQL Server uses GETDATE(), PostgreSQL uses CURRENT_DATE.'
            },
            {
                'category': 'SQL',
                'question': 'What does the SQL COALESCE function do?',
                'options': ['Joins tables', 'Returns first non-NULL value', 'Counts rows', 'Sorts data'],
                'answer': 1,
                'explanation': 'COALESCE returns the first non-NULL value from a list of expressions.'
            },
            
            # AWS Questions
            {
                'category': 'AWS',
                'question': 'What is AWS Lambda?',
                'options': ['A database service', 'A serverless compute service', 'A storage service', 'A networking service'],
                'answer': 1,
                'explanation': 'AWS Lambda is a serverless compute service that runs code in response to events.'
            },
            {
                'category': 'AWS',
                'question': 'Which AWS service would you use for a managed relational database?',
                'options': ['S3', 'EC2', 'RDS', 'Lambda'],
                'answer': 2,
                'explanation': 'Amazon RDS (Relational Database Service) provides managed relational databases.'
            },
            {
                'category': 'AWS',
                'question': 'What is the maximum execution time for an AWS Lambda function?',
                'options': ['5 minutes', '15 minutes', '30 minutes', '60 minutes'],
                'answer': 1,
                'explanation': 'AWS Lambda functions can run for a maximum of 15 minutes.'
            },
            {
                'category': 'AWS',
                'question': 'Which AWS service provides a CDN (Content Delivery Network)?',
                'options': ['Route 53', 'CloudFront', 'S3', 'EC2'],
                'answer': 1,
                'explanation': 'Amazon CloudFront is AWS\'s content delivery network service.'
            },
            {
                'category': 'AWS',
                'question': 'What is the purpose of AWS VPC?',
                'options': ['Virtual Private Cloud for network isolation', 'Virtual Processing Computer', 'Volume Persistent Cache', 'Virtual Platform Console'],
                'answer': 0,
                'explanation': 'VPC (Virtual Private Cloud) provides network isolation for your AWS resources.'
            },
            
            # Trading Systems Questions
            {
                'category': 'Trading Systems',
                'question': 'What does FIX stand for in FIX Protocol?',
                'options': ['Fast Internet Exchange', 'Financial Information eXchange', 'Fixed Income eXchange', 'Financial Integration eXchange'],
                'answer': 1,
                'explanation': 'FIX stands for Financial Information eXchange, the standard protocol for electronic trading.'
            },
            {
                'category': 'Trading Systems',
                'question': 'What is typical latency for high-frequency trading systems?',
                'options': ['Seconds', 'Milliseconds', 'Microseconds', 'Minutes'],
                'answer': 2,
                'explanation': 'Modern HFT systems operate in microseconds or even nanoseconds.'
            },
            {
                'category': 'Trading Systems',
                'question': 'What is a market maker?',
                'options': ['A trader who only buys', 'A trader who provides liquidity', 'A regulatory body', 'An exchange operator'],
                'answer': 1,
                'explanation': 'Market makers provide liquidity by continuously quoting both buy and sell prices.'
            },
            {
                'category': 'Trading Systems',
                'question': 'What is NUMA in the context of trading systems?',
                'options': ['Network Update Management API', 'Non-Uniform Memory Access', 'Normalized Unit Market Analysis', 'Network Unified Messaging Architecture'],
                'answer': 1,
                'explanation': 'NUMA (Non-Uniform Memory Access) is critical for optimizing memory access in multi-socket systems.'
            },
            {
                'category': 'Trading Systems',
                'question': 'What is the purpose of kernel bypass in trading systems?',
                'options': ['Security', 'Reduce latency', 'Increase storage', 'Improve UI'],
                'answer': 1,
                'explanation': 'Kernel bypass allows direct hardware access, reducing latency by avoiding OS overhead.'
            },
            {
                'category': 'Trading Systems',
                'question': 'What is a FIX session?',
                'options': ['A trading strategy', 'A connection between two FIX engines', 'A type of order', 'A market data feed'],
                'answer': 1,
                'explanation': 'A FIX session is a bi-directional stream of ordered messages between two FIX engines.'
            },
            {
                'category': 'Trading Systems',
                'question': 'What is the purpose of sequence numbers in FIX protocol?',
                'options': ['Encryption', 'Message ordering and gap detection', 'Routing', 'Compression'],
                'answer': 1,
                'explanation': 'Sequence numbers ensure message ordering and help detect missing messages.'
            },
            
            # General CS/Interview Questions
            {
                'category': 'Computer Science',
                'question': 'What is the time complexity of binary search?',
                'options': ['O(n)', 'O(log n)', 'O(n log n)', 'O(1)'],
                'answer': 1,
                'explanation': 'Binary search has O(log n) time complexity as it halves the search space each iteration.'
            },
            {
                'category': 'Computer Science',
                'question': 'What is a hash collision?',
                'options': ['When a hash function fails', 'When two inputs produce the same hash', 'When memory is full', 'When the network fails'],
                'answer': 1,
                'explanation': 'A hash collision occurs when two different inputs produce the same hash value.'
            },
            {
                'category': 'Computer Science',
                'question': 'What is the difference between a process and a thread?',
                'options': ['No difference', 'Threads share memory, processes don\'t', 'Processes are faster', 'Threads can\'t run in parallel'],
                'answer': 1,
                'explanation': 'Threads share memory space within a process, while processes have separate memory spaces.'
            },
            {
                'category': 'Computer Science',
                'question': 'What is a race condition?',
                'options': ['Fast code execution', 'When threads compete for resources unpredictably', 'Network latency', 'CPU optimization'],
                'answer': 1,
                'explanation': 'A race condition occurs when multiple threads access shared data concurrently, leading to unpredictable results.'
            },
            {
                'category': 'Computer Science',
                'question': 'What is the purpose of an index in a database?',
                'options': ['Store more data', 'Speed up queries', 'Encrypt data', 'Reduce storage'],
                'answer': 1,
                'explanation': 'Indexes speed up data retrieval by creating a sorted reference to rows in a table.'
            },
            
            # Automation/DevOps Questions
            {
                'category': 'Automation',
                'question': 'What is CI/CD?',
                'options': ['Continuous Integration/Continuous Deployment', 'Computer Interface/Computer Design', 'Code Integration/Code Debugging', 'Cloud Infrastructure/Cloud Development'],
                'answer': 0,
                'explanation': 'CI/CD automates the integration and deployment of code changes.'
            },
            {
                'category': 'Automation',
                'question': 'What is the purpose of Docker?',
                'options': ['Database management', 'Containerization', 'Network security', 'Code compilation'],
                'answer': 1,
                'explanation': 'Docker provides containerization, packaging applications with their dependencies.'
            },
            {
                'category': 'Automation',
                'question': 'What is Kubernetes?',
                'options': ['A programming language', 'A database', 'A container orchestration platform', 'A monitoring tool'],
                'answer': 2,
                'explanation': 'Kubernetes orchestrates and manages containerized applications at scale.'
            }
        ]
    
    def setup_tray_window(self):
        """Setup the small tray window"""
        # Configure tray window
        width = self.config.get('tray_width', 200)
        height = self.config.get('tray_height', 50)
        self.root.geometry(f"{width}x{height}+{self.root.winfo_screenwidth()-width-10}+10")
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#2b2b2b')
        
        # Create countdown label
        self.countdown_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 14, 'bold'),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        self.countdown_label.pack(expand=True, fill='both')
        
        # Prevent closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_tray_close)
    
    def on_tray_close(self):
        """Handle tray window close attempt"""
        if not self.quiz_active:
            self.root.quit()
    
    def update_countdown(self):
        """Update countdown timer"""
        if self.time_remaining > 0:
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            self.countdown_label.config(text=f"Next quiz: {minutes:02d}:{seconds:02d}")
            self.time_remaining -= 1
            self.root.after(1000, self.update_countdown)
        else:
            self.start_quiz()
    
    def start_quiz(self):
        """Start the quiz mode"""
        self.quiz_active = True
        self.correct_count = 0
        
        # Create quiz window
        self.quiz_window = tk.Toplevel(self.root)
        self.quiz_window.title("SKILL CHECK TIME!")
        self.quiz_window.attributes('-fullscreen', True)
        self.quiz_window.attributes('-topmost', True)
        self.quiz_window.configure(bg='#1e1e1e')
        
        # Prevent closing
        self.quiz_window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Main container
        main_frame = tk.Frame(self.quiz_window, bg='#1e1e1e')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Progress frame
        progress_frame = tk.Frame(main_frame, bg='#1e1e1e')
        progress_frame.pack(fill='x', pady=(0, 20))
        
        self.progress_label = tk.Label(
            progress_frame,
            text=f"Progress: {self.correct_count}/{self.questions_required}",
            font=('Arial', 18, 'bold'),
            bg='#1e1e1e',
            fg='#00ff00'
        )
        self.progress_label.pack(side='left')
        
        # Category label
        self.category_label = tk.Label(
            progress_frame,
            text="",
            font=('Arial', 16),
            bg='#1e1e1e',
            fg='#ffcc00'
        )
        self.category_label.pack(side='right')
        
        # Question frame
        self.question_frame = tk.Frame(main_frame, bg='#2b2b2b', relief='ridge', bd=2)
        self.question_frame.pack(fill='both', expand=True, pady=20)
        
        # Question label
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=('Arial', 20),
            bg='#2b2b2b',
            fg='white',
            wraplength=700,
            justify='left'
        )
        self.question_label.pack(pady=30, padx=30)
        
        # Options frame
        self.options_frame = tk.Frame(self.question_frame, bg='#2b2b2b')
        self.options_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Feedback label
        self.feedback_label = tk.Label(
            main_frame,
            text="",
            font=('Arial', 14),
            bg='#1e1e1e',
            fg='white',
            wraplength=700,
            justify='left'
        )
        self.feedback_label.pack(pady=10)
        
        # Skip button
        skip_button = tk.Button(
            main_frame,
            text="Skip Question",
            font=('Arial', 12),
            bg='#666666',
            fg='white',
            command=self.skip_question,
            width=15
        )
        skip_button.pack(pady=10)
        
        # Load first question
        self.load_question()
    
    def load_question(self):
        """Load a random question"""
        self.current_question = random.choice(self.questions)
        
        # Update labels
        self.category_label.config(text=f"Category: {self.current_question['category']}")
        self.question_label.config(text=self.current_question['question'])
        self.feedback_label.config(text="")
        
        # Clear old options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Create option buttons
        for i, option in enumerate(self.current_question['options']):
            btn = tk.Button(
                self.options_frame,
                text=f"{chr(65+i)}. {option}",
                font=('Arial', 16),
                bg='#3a3a3a',
                fg='white',
                anchor='w',
                padx=20,
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(fill='x', pady=5)
    
    def check_answer(self, selected_index):
        """Check if answer is correct"""
        if selected_index == self.current_question['answer']:
            self.correct_count += 1
            self.progress_label.config(text=f"Progress: {self.correct_count}/{self.questions_required}")
            
            if self.correct_count >= self.questions_required:
                self.end_quiz()
            else:
                self.feedback_label.config(text="✓ Correct! Loading next question...", fg='#00ff00')
                self.quiz_window.after(1500, self.load_question)
        else:
            self.feedback_label.config(
                text=f"✗ Wrong! {self.current_question['explanation']}",
                fg='#ff6666'
            )
            self.quiz_window.after(3000, self.load_question)
    
    def skip_question(self):
        """Skip current question"""
        self.load_question()
    
    def end_quiz(self):
        """End quiz and reset timer"""
        self.quiz_active = False
        self.quiz_window.destroy()
        self.time_remaining = self.config.get('interval_minutes', 10) * 60
        self.update_countdown()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = StudyReminder()
    app.run()
