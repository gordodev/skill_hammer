# skill_hammer
# Skill Hammer - Active Learning Study Reminder

A modern, forced-learning application designed to maintain and improve technical skills through regular, interactive quizzes. Built specifically for professionals preparing for technical interviews in software engineering, DevOps, and financial technology roles.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🎯 Purpose

In today's competitive tech job market, keeping skills sharp while job searching is critical. Skill Hammer ensures you maintain proficiency in key technical areas through forced, regular practice sessions that can't be ignored or postponed.

## ✨ Features

### Core Functionality
- **Forced Learning System**: Full-screen quizzes that block other activities until completed
- **Hybrid Answer Mode**: Type your answer first, then verify with multiple choice options
- **Smart Scheduling**: Customizable intervals between study sessions (default: 10 minutes)
- **Progress Tracking**: Requires correct answers before allowing you to continue
- **Always-On Display**: Small countdown timer that stays visible while working

### Technical Coverage
- **Python**: Data structures, algorithms, libraries, best practices
- **SQL**: Query optimization, joins, database design
- **AWS**: Cloud services, Lambda, RDS, architecture
- **Trading Systems**: FIX protocol, low-latency concepts, market microstructure
- **Computer Science**: Algorithms, complexity, system design
- **DevOps**: Docker, Kubernetes, CI/CD, automation

### User Experience
- **Modern Dark Theme**: Professional appearance with high contrast
- **Intelligent Feedback**: Explanations for wrong answers to facilitate learning
- **Non-Intrusive Timer**: Small tray window shows time until next session
- **Skip Functionality**: Move past difficult questions without penalty

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually comes with Python)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/Skill Hammer.git
cd Skill Hammer

# Run the application
python study_reminder.py
```

## 📖 Usage

### Starting the Application
```bash
python study_reminder.py
```

### Workflow
1. **Timer Phase**: A small window appears in the top-right corner counting down to the next quiz
2. **Quiz Phase**: Full-screen quiz launches automatically when timer reaches zero
3. **Answer Process**: 
   - Type your answer in the input field (new feature)
   - Review multiple choice options to verify
   - Submit your answer or select a different option
4. **Completion**: Answer required number of questions correctly to continue working

### Configuration
Edit `study_config.json` to customize:
```json
{
  "interval_minutes": 10,      // Time between quizzes
  "questions_required": 3,     // Correct answers needed
  "tray_width": 200,          // Timer window width
  "tray_height": 50,          // Timer window height
  "quiz_width": 800,          // Quiz window width
  "quiz_height": 600         // Quiz window height
}
```

## 🏗️ Architecture

### File Structure
```
Skill Hammer/
├── study_reminder.py      # Main application
├── questions.json         # Question database (coming soon)
├── study_config.json      # User configuration
├── question_editor.py     # Question management tool (planned)
└── README.md             # This file
```

### Key Components
- **StudyReminder**: Main application class
- **Question Bank**: Comprehensive set of technical questions
- **Timer System**: Background countdown mechanism
- **Quiz Interface**: Full-screen interactive quiz system

## 🔄 Upcoming Features

### Version 2.0 (In Development)
- [x] Hybrid answer input (type + multiple choice)
- [ ] Separate question file (JSON format)
- [ ] Audio reminder system (2000Hz tone)
- [ ] Question editor GUI tool
- [ ] Progress statistics tracking
- [ ] Difficulty adjustment based on performance
- [ ] Category-specific study sessions

### Future Enhancements
- Cloud synchronization for multi-device support
- Spaced repetition algorithm
- Custom question import/export
- Performance analytics dashboard
- Integration with calendar apps

## 🎯 Target Audience

This tool is specifically designed for:
- Software engineers preparing for technical interviews
- DevOps professionals maintaining diverse skill sets
- Financial technology specialists needing FIX protocol knowledge
- Developers transitioning between technologies
- Anyone needing forced practice to maintain technical skills

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📊 Technical Skills Covered

### Programming & Scripting
- Python (data structures, OOP, libraries)
- SQL (optimization, complex queries)
- Bash/Shell scripting concepts

### Cloud & Infrastructure
- AWS services (Lambda, RDS, VPC)
- Docker & containerization
- Kubernetes orchestration

### Financial Technology
- FIX protocol
- Trading systems architecture
- Low-latency optimization
- Market microstructure

### Computer Science Fundamentals
- Algorithm complexity (Big O)
- Data structures
- System design patterns
- Concurrency concepts

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- Designed for professionals facing the challenge of maintaining skills during job searches
- Inspired by the need for consistent practice in rapidly evolving technical fields
- Built with modern UI/UX principles despite using tkinter


---

**Remember**: Consistency is key. Let Skill Hammer keep your skills sharp while you focus on landing your next role!
