from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = 'online_course.db'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    courses = conn.execute('SELECT c.*, i.name AS instructor_name FROM courses c JOIN instructors i ON c.instructor_id = i.instructor_id').fetchall()
    enrollments = conn.execute(
        'SELECT e.enrollment_id, s.student_id, s.first_name || " " || s.last_name AS student_name, c.title AS course_title, e.status FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN courses c ON e.course_id = c.course_id'
    ).fetchall()
    conn.close()
    return render_template('index.html', students=students, courses=courses, enrollments=enrollments)


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    conn = get_db_connection()
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        conn.execute(
            'INSERT OR IGNORE INTO enrollments (student_id, course_id) VALUES (?, ?)',
            (student_id, course_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    students = conn.execute('SELECT * FROM students').fetchall()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return render_template('enroll.html', students=students, courses=courses)


@app.route('/courses')
def courses():
    conn = get_db_connection()
    courses = conn.execute(
        '''
        SELECT
            c.*, i.name AS instructor_name,
            COUNT(e.enrollment_id) AS enrolled_students
        FROM courses c
        JOIN instructors i ON c.instructor_id = i.instructor_id
        LEFT JOIN enrollments e ON c.course_id = e.course_id
        GROUP BY c.course_id
        ORDER BY c.start_date
        '''
    ).fetchall()
    conn.close()
    return render_template('courses.html', courses=courses)


@app.route('/courses/new', methods=['GET', 'POST'])
def new_course():
    conn = get_db_connection()
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        instructor_id = request.form['instructor_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        capacity = request.form['capacity']

        cursor = conn.execute(
            'INSERT INTO courses (title, description, instructor_id, start_date, end_date, capacity) VALUES (?, ?, ?, ?, ?, ?)',
            (title, description, instructor_id, start_date, end_date, capacity),
        )
        course_id = cursor.lastrowid

        for index in range(1, 6):
            module_title = request.form.get(f'module_{index}_title', '').strip()
            module_description = request.form.get(f'module_{index}_description', '').strip()
            if module_title:
                conn.execute(
                    'INSERT INTO modules (course_id, module_title, module_order, description) VALUES (?, ?, ?, ?)',
                    (course_id, module_title, index, module_description),
                )

        conn.commit()
        conn.close()
        return redirect(url_for('courses'))

    instructors = conn.execute('SELECT * FROM instructors ORDER BY name').fetchall()
    conn.close()
    return render_template('course_form.html', instructors=instructors)


@app.route('/course/<int:course_id>')
def course_detail(course_id):
    conn = get_db_connection()
    course = conn.execute(
        'SELECT c.*, i.name AS instructor_name FROM courses c JOIN instructors i ON c.instructor_id = i.instructor_id WHERE c.course_id = ?',
        (course_id,),
    ).fetchone()
    if course is None:
        conn.close()
        return redirect(url_for('courses'))

    modules = conn.execute(
        'SELECT * FROM modules WHERE course_id = ? ORDER BY module_order',
        (course_id,),
    ).fetchall()

    enrolled = conn.execute(
        'SELECT e.enrollment_id, s.student_id, s.first_name || " " || s.last_name AS student_name, e.status FROM enrollments e JOIN students s ON e.student_id = s.student_id WHERE e.course_id = ? ORDER BY s.last_name',
        (course_id,),
    ).fetchall()

    course_stats = conn.execute(
        '''
        SELECT
            COUNT(DISTINCT e.student_id) AS enrolled_students,
            ROUND(AVG(CASE WHEN p.completed = 1 THEN 1.0 ELSE 0.0 END) * 100, 1) AS completion_rate
        FROM enrollments e
        LEFT JOIN progress p ON e.enrollment_id = p.enrollment_id
        WHERE e.course_id = ?
        ''',
        (course_id,),
    ).fetchone()

    conn.close()
    return render_template('course_detail.html', course=course, modules=modules, enrolled=enrolled, course_stats=course_stats)


@app.route('/progress/update', methods=['POST'])
def update_progress():
    enrollment_id = request.form['enrollment_id']
    module_id = request.form['module_id']
    completed = 1 if request.form.get('completed') == 'on' else 0
    score = request.form.get('score')
    score = float(score) if score and score.strip() else None

    conn = get_db_connection()
    cursor = conn.execute(
        'UPDATE progress SET completed = ?, score = ?, updated_on = date("now") WHERE enrollment_id = ? AND module_id = ?',
        (completed, score, enrollment_id, module_id),
    )
    if cursor.rowcount == 0:
        conn.execute(
            'INSERT INTO progress (enrollment_id, module_id, completed, score) VALUES (?, ?, ?, ?)',
            (enrollment_id, module_id, completed, score),
        )

    student = conn.execute('SELECT student_id FROM enrollments WHERE enrollment_id = ?', (enrollment_id,)).fetchone()
    conn.commit()
    conn.close()

    if student:
        return redirect(url_for('student_progress', student_id=student['student_id']))
    return redirect(url_for('index'))


@app.route('/students')
def students():
    conn = get_db_connection()
    students = conn.execute(
        '''
        SELECT
            s.*,
            COUNT(e.course_id) AS course_count,
            MAX(c.end_date) AS next_end_date
        FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        LEFT JOIN courses c ON e.course_id = c.course_id
        GROUP BY s.student_id
        ORDER BY s.last_name, s.first_name
        '''
    ).fetchall()
    conn.close()
    return render_template('students.html', students=students)


@app.route('/students/new', methods=['GET', 'POST'])
def new_student():
    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        email = request.form['email'].strip().lower()

        conn = get_db_connection()
        conn.execute(
            'INSERT OR IGNORE INTO students (first_name, last_name, email) VALUES (?, ?, ?)',
            (first_name, last_name, email),
        )
        conn.commit()
        conn.close()
        return redirect(url_for('students'))

    return render_template('student_form.html')


@app.route('/student/<int:student_id>')
def student_progress(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    if student is None:
        conn.close()
        return redirect(url_for('index'))

    enrollments = conn.execute(
        'SELECT e.enrollment_id, c.course_id, c.title AS course_title, e.status FROM enrollments e JOIN courses c ON e.course_id = c.course_id WHERE e.student_id = ?',
        (student_id,),
    ).fetchall()

    progress_rows = []
    for enrollment in enrollments:
        progress = conn.execute(
            'SELECT m.module_id, m.module_title, p.completed, p.score FROM progress p JOIN modules m ON p.module_id = m.module_id WHERE p.enrollment_id = ? ORDER BY m.module_order',
            (enrollment['enrollment_id'],),
        ).fetchall()
        course_progress = {
            'course_title': enrollment['course_title'],
            'status': enrollment['status'],
            'progress': progress,
        }
        progress_rows.append(course_progress)

    conn.close()
    return render_template('student.html', student=student, progress_rows=progress_rows)


@app.route('/report')
def report():
    conn = get_db_connection()
    course_reports = conn.execute(
        '''
        SELECT
            c.course_id,
            c.title,
            COUNT(DISTINCT e.student_id) AS enrolled_students,
            ROUND(AVG(CASE WHEN p.completed = 1 THEN 1.0 ELSE 0.0 END) * 100, 1) AS completion_percentage
        FROM courses c
        LEFT JOIN enrollments e ON c.course_id = e.course_id
        LEFT JOIN progress p ON e.enrollment_id = p.enrollment_id
        GROUP BY c.course_id
        '''
    ).fetchall()

    student_reports = conn.execute(
        '''
        SELECT
            s.student_id,
            s.first_name || ' ' || s.last_name AS student_name,
            COUNT(DISTINCT e.course_id) AS courses_enrolled,
            ROUND(AVG(p.score), 1) AS average_score,
            ROUND(AVG(CASE WHEN p.completed = 1 THEN 1.0 ELSE 0.0 END) * 100, 1) AS completion_rate
        FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        LEFT JOIN progress p ON e.enrollment_id = p.enrollment_id
        GROUP BY s.student_id
        '''
    ).fetchall()
    conn.close()
    return render_template('reports.html', course_reports=course_reports, student_reports=student_reports)


if __name__ == '__main__':
    app.run(debug=True)
