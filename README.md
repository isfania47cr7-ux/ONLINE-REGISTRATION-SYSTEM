# Online Course Registration System

A sample relational database application for managing course enrollments, tracking student progress, and generating performance reports.

## Features
- Student registration and course enrollment
- Dynamic course catalog with course creation
- Course details and instructor assignment
- Module-level progress updates and performance reports

## Usage
- Visit `/students` to manage learners.
- Visit `/courses` to view course catalog and create new courses.
- Use `/enroll` to enroll students in courses.
- Track progress and scores from the student profile page.

## Setup
1. Install Python 3.10+.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\\Scripts\\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   python setup_db.py
   ```
5. Start the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

## Database Schema
- `students`
- `courses`
- `instructors`
- `modules`
- `enrollments`
- `progress`

## Usage
- Register students, enroll them in courses, and track progress by module.
- Generate performance reports showing completed modules and average completion percentages.
