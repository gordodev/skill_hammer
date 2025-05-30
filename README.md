# Skill Hammer - Active Learning Study Reminder

A modern, forced-learning application designed to maintain and sharpen technical skills through interactive quizzes. Ideal for professionals preparing for technical interviews in software engineering, DevOps, and financial technology.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## 🎯 Purpose

In today's tech job market, consistent practice is non-negotiable. **Skill Hammer** keeps your skills sharp by enforcing regular, full-screen quizzes you can't ignore or delay.

---

## ✨ Features

### 🔒 Core Functionality

* **Forced Learning**: Blocks all other activity until the quiz is completed.
* **Hybrid Answer Input**: Type your answer first, then verify via multiple choice.
* **Smart Scheduling**: Custom intervals between sessions (default: 10 minutes).
* **Progress Lock**: Continue only after answering a set number of questions correctly.
* **Persistent Timer**: Always-on countdown tray visible during work.

### 🧠 Learning Experience

* **Question Clicking**: Click a question to instantly Google it if you’re stuck.
* **Intelligent Feedback**: Wrong answers display explanations to reinforce learning (note: clears too quickly; improvement planned).
* **Skip Option**: Skip questions without penalty to keep momentum.

### 🖥️ Technical Coverage

* **Python**: Data structures, algorithms, libraries, best practices.
* **SQL**: Queries, optimization, design.
* **AWS**: Lambda, RDS, architecture.
* **DevOps**: Docker, Kubernetes, CI/CD.
* **Trading Tech**: FIX protocol, market microstructure, trading system architecture.
* **Unix/Linux**: Shell, scripting, system fundamentals.
* **Computer Science**: Complexity, system design, concurrency.
* **Code Exercises**: Write or complete code (e.g., define an empty function).

---

## 🚀 Installation

### Prerequisites

* Python 3.7 or higher
* `tkinter` (usually bundled with Python)

### Setup

```bash
git clone https://github.com/gordodev/skill_hammer.git
cd skill_hammer
python study_reminder.py
```

---

## 📖 Usage

### Starting the App

```bash
python study_reminder.py
```

### Workflow

1. **Timer Phase**: A tray timer counts down to the next quiz.
2. **Quiz Phase**: A full-screen quiz launches automatically.
3. **Answering**:

   * Type your response
   * Review multiple choice to verify
   * Submit or change your answer
4. **Completion**: Continue only after getting the required number of correct answers.

### Configuration

Customize `study_config.json`:

```json
{
  "interval_minutes": 10,
  "questions_required": 3,
  "tray_width": 200,
  "tray_height": 50,
  "quiz_width": 800,
  "quiz_height": 600
}
```

---

## 🏗️ Architecture

### File Structure

```
skill_hammer/
├── study_reminder.py       # Main app
├── study_config.json       # Config file
├── questions.json          # Question database (coming soon)
├── question_editor.py      # Planned GUI tool for managing questions
└── README.md               # This file
```

### Components

* **StudyReminder**: Main app logic
* **Timer System**: Countdown manager
* **Quiz UI**: Full-screen enforced interface
* **Question Bank**: Growing repository of topics

---

## 🔄 Roadmap

### v2.0 (In Development)

* [x] Hybrid answer input
* [ ] External JSON question file
* [ ] 2000Hz audio reminder
* [ ] GUI question editor
* [ ] Progress tracking/stats
* [ ] Adaptive difficulty
* [ ] Study by topic/category

### Future Ideas

* Spaced repetition
* Cloud sync
* Import/export question sets
* Calendar integration
* Performance dashboard

---

## 👥 Target Users

* Engineers prepping for tech interviews
* DevOps professionals maintaining broad knowledge
* FinTech pros needing regular FIX protocol practice
* Career switchers needing refresher drills
* Anyone needing structured, forced learning

---

## 🤝 Contributing

Pull requests are welcome!

### Development Steps

1. Fork this repo
2. Create a branch (`git checkout -b feature/myFeature`)
3. Commit your changes (`git commit -m "Add myFeature"`)
4. Push it (`git push origin feature/myFeature`)
5. Open a PR

---

## 📊 Technical Skills Covered

### Programming

* Python, OOP, common libraries
* SQL: Joins, indexing, tuning
* Bash/Shell scripting

### Infrastructure

* AWS (Lambda, RDS, VPC)
* Docker & Kubernetes
* CI/CD principles

### FinTech

* FIX protocol
* Low-latency systems
* Market microstructure

### CS Fundamentals

* Algorithms & Big O
* Data structures
* System & concurrency design

---

## 📝 License

MIT License. See `LICENSE` for full terms.

---

## 🙏 Acknowledgments

* Built for job seekers staying sharp
* Inspired by personal experience with skill decay
* Designed with modern UX principles (even in `tkinter`)

---

**Stay sharp. Stay ready. Let Skill Hammer do the reminding.**
