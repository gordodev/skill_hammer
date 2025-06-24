import tkinter as tk
from tkinter import ttk
import json
import random
import time
from datetime import datetime
import threading
import os
import argparse



def main():
    parser = argparse.ArgumentParser(description='Study Reminder')
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=10,
        help='Interval between quizzes, in minutes'
    )
    parser.add_argument(
        '--questions', '-q',
        type=int,
        default=3,
        help='Number of questions per quiz'
    )
    parser.add_argument(
        '--json-file', '-j',
        type=str,
        default='questions.json',
        help='Path to the questions JSON file'
    )
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Disable logging for tests'
    )
    args = parser.parse_args()

    # Initialize app with logging control
    app = StudyReminder(
        questions_file=args.json_file,
        disable_logging=args.test
    )
    app.config['interval_minutes']   = args.interval
    app.config['questions_required'] = args.questions
    app.questions_required = args.questions  # ADD THIS LINE
    app.time_remaining               = args.interval * 60

    app.run()


class StudyReminder:
    LOG_FILE = 'quiz_log.ndjson'
    def __init__(self, questions_file='questions.json', disable_logging=False):
        self.questions_file = questions_file
        self.logging_enabled = not disable_logging
        self.root = tk.Tk()
        self.root.title("Study Reminder")
        
        # Load configuration
        self.config = self.load_config()
        
        # Logging state
        self.log_entries = []
        
        # Quiz state
        self.correct_count      = 0
        self.questions_required = self.config.get('questions_required', 3)
        self.time_remaining     = self.config.get('interval_minutes', 10) * 60
        self.quiz_active        = False
        self.current_question   = None
        
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
            'interval_minutes':   10,
            'questions_required': 3,
            'tray_width':         200,
            'tray_height':        50,
            'quiz_width':         800,
            'quiz_height':        600
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
        """Load questions from external JSON file or fall back to defaults."""
        questions_file = self.questions_file

        try:
            if os.path.exists(questions_file):
                with open(questions_file, 'r') as f:
                    data = json.load(f)

                # If it's a dict with a "questions" key, use that.
                if isinstance(data, dict):
                    return data.get('questions', [])
                # If it's already a list of questions, return it directly.
                elif isinstance(data, list):
                    return data
                else:
                    print(f"Warning: unexpected JSON format, expected dict or list.")
                    return []

            else:
                print(f"Warning: {questions_file} not found. Using default questions.")
                return self.get_default_questions()

        except Exception as e:
            print(f"Error loading questions: {e}")
            return self.get_default_questions()

    def get_default_questions(self):
        """Fallback questions if JSON file is missing"""
        return [
            {
                'category': 'Python',
                'question': 'What is the time complexity of dictionary lookup in Python?',
                'options': ['O(1)', 'O(n)', 'O(log n)', 'O(n²)'],
                'answer': 0,
                'explanation': 'Dictionary lookups in Python are O(1) on average because they use hash tables.'
            },
            {
                'category': 'SQL',
                'question': 'Which JOIN returns all rows from both tables?',
                'options': ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL OUTER JOIN'],
                'answer': 3,
                'explanation': 'FULL OUTER JOIN returns all rows from both tables, with NULL values where no match exists.'
            }
        ]
    
    def setup_tray_window(self):
        """Setup the small tray window"""
        width = self.config.get('tray_width', 200)
        height = self.config.get('tray_height', 50)
        x = self.root.winfo_screenwidth() - width - 10
        y = 10
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#2b2b2b')

        self.countdown_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 14, 'bold'),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        self.countdown_label.pack(expand=True, fill='both')

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
        self.quiz_active = True
        self.correct_count = 0
        self.quiz_start_time = datetime.utcnow()
        self.log_entries       = []

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
        
        # Setup code frame (NEW - displays the context/setup)
        self.setup_frame = tk.Frame(main_frame, bg='#2b2b2b', relief='ridge', bd=2)
        self.setup_frame.pack(fill='x', pady=(0, 20))
        
        self.setup_label = tk.Label(
            self.setup_frame,
            text="",
            font=('Consolas', 12),
            bg='#2b2b2b',
            fg='#00ff00',
            justify='left',
            anchor='w'
        )
        self.setup_label.pack(pady=10, padx=20, fill='x')
        
        # Answer input frame
        input_frame = tk.Frame(main_frame, bg='#2b2b2b', relief='ridge', bd=2)
        input_frame.pack(fill='x', pady=(0, 20))
        
        input_label = tk.Label(
            input_frame,
            text="Type your answer first:",
            font=('Arial', 14),
            bg='#2b2b2b',
            fg='#ffcc00'
        )
        input_label.pack(pady=(10, 5))
        
        # Answer entry field
        self.answer_entry = tk.Entry(
            input_frame,
            font=('Arial', 16),
            bg='#3a3a3a',
            fg='white',
            insertbackground='white',
            width=50
        )
        self.answer_entry.pack(pady=(0, 10))
        self.answer_entry.bind('<Return>', lambda e: self.submit_typed_answer())
        
        # Submit button for typed answer
        submit_frame = tk.Frame(input_frame, bg='#2b2b2b')
        submit_frame.pack(pady=(0, 10))
        
        self.submit_button = tk.Button(
            submit_frame,
            text="Submit Answer",
            font=('Arial', 14, 'bold'),
            bg='#00ff00',
            fg='black',
            command=self.submit_typed_answer,
            padx=20,
            pady=5
        )
        self.submit_button.pack()
        
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
        
        # Multiple choice hint label
        hint_label = tk.Label(
            self.question_frame,
            text="Or select from options below:",
            font=('Arial', 12),
            bg='#2b2b2b',
            fg='#999999'
        )
        hint_label.pack(pady=(0, 10))
        
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
        self.question_start_time = datetime.utcnow()
        if not self.questions:
            self.feedback_label.config(text="No questions available!", fg='#ff6666')
            return
            
        self.current_question = random.choice(self.questions)
        
        # Update labels
        self.category_label.config(text=f"Category: {self.current_question['category']}")
        self.question_label.config(text=self.current_question['question'])
        self.feedback_label.config(text="")
        
        # Update setup code display (NEW)
        if 'setup_code' in self.current_question and self.current_question['setup_code']:
            self.setup_frame.pack(fill='x', pady=(0, 20))
            self.setup_label.config(text=self.current_question['setup_code'])
        else:
            self.setup_frame.pack_forget()
        
        # Clear answer entry
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus_set()
        
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
                command=lambda idx=i: self.select_multiple_choice(idx)
            )
            btn.pack(fill='x', pady=5)
            
    def record_answer(self, given, was_correct):
        duration = (datetime.utcnow() - self.question_start_time).total_seconds()
        entry = {
            'question':       self.current_question['question'],
            'given_answer':   given,
            'correct_answer': self.current_question['options'][self.current_question['answer']],
            'was_correct':    was_correct,
            'duration_secs':  duration
        }
        if self.logging_enabled:
            self.log_entries.append(entry)
            
    
    def submit_typed_answer(self):
        """Submit the typed answer"""
        typed_answer = self.answer_entry.get().strip()
        if not typed_answer:
            self.feedback_label.config(text="Please type an answer or select from options below", fg='#ffcc00')
            return
        
        # Check if typed answer matches any option
        correct_answer_text = self.current_question['options'][self.current_question['answer']].lower()
        typed_answer_lower = typed_answer.lower()
        
        # Check for exact match or if typed answer is contained in correct answer
        is_correct = (typed_answer_lower == correct_answer_text or 
                     typed_answer_lower in correct_answer_text or
                     correct_answer_text in typed_answer_lower)
        
        # Also check if it's a partial match of any option
        for i, option in enumerate(self.current_question['options']):
            if typed_answer_lower in option.lower() or option.lower() in typed_answer_lower:
                if i == self.current_question['answer']:
                    is_correct = True
                    break
        
        self.record_answer(typed_answer, is_correct)
        
        if is_correct:
            self.handle_correct_answer()
        else:
            self.feedback_label.config(
                text=f"✗ Wrong! The correct answer is: {self.current_question['options'][self.current_question['answer']]}\n{self.current_question['explanation']}",
                fg='#ff6666'
            )
            self.quiz_window.after(3000, self.load_question)
    
    def select_multiple_choice(self, selected_index):
        """Handle multiple choice selection - puts answer in text field"""
        selected_text = self.current_question['options'][selected_index]
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.insert(0, selected_text)
        self.answer_entry.focus_set()
    
    def handle_correct_answer(self):
        """Handle correct answer"""
        self.correct_count += 1
        # Log the correct answer
        self.record_answer(
            self.current_question['options'][self.current_question['answer']],
            True,
        )
        self.progress_label.config(text=f"Progress: {self.correct_count}/{self.questions_required}")
        
        if self.correct_count >= self.questions_required:
            self.end_quiz()
        else:
            self.feedback_label.config(text="✓ Correct! Loading next question...", fg='#00ff00')
            self.quiz_window.after(1500, self.load_question)
    
    def skip_question(self):
        """Skip current question"""
        # Log that the user skipped this question
        self.record_answer('skipped', False)
        self.load_question()
    
    def end_quiz(self):
        """End quiz and reset timer"""
        self.quiz_active = False
        self.quiz_window.destroy()

        # Build the quiz summary log
        quiz_end = datetime.utcnow()
        score = (self.correct_count / self.questions_required) * 100
        log = {
            'quiz_start':        self.quiz_start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'quiz_end':          quiz_end.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'questions_required': self.questions_required,
            'correct_count':      self.correct_count,
            'score_percent':      score,
            'questions':         self.log_entries
        }
        if self.logging_enabled:
            self.write_log(log)

        # Reset timer for next quiz
        self.time_remaining = self.config.get('interval_minutes', 10) * 60
        self.update_countdown()
        
    def write_log(self, log_data):
        try:
            with open(self.LOG_FILE, 'a') as f:
                f.write(json.dumps(log_data) + '\n')
        except Exception as e:
            print(f"Error writing log: {e}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    main()
