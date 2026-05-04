INSERT OR IGNORE INTO instructors (name, email) VALUES
  ('Sana Ahmad', 'sana@onlinecourse.com'),
  ('Rohan Patel', 'rohan@onlinecourse.com'),
  ('Layla Siddiqui', 'layla@onlinecourse.com'),
  ('Farhan Javed', 'farhan@onlinecourse.com'),
  ('Meera Sharma', 'meera@onlinecourse.com');

INSERT OR IGNORE INTO students (first_name, last_name, email) VALUES
  ('Ali', 'Khan', 'ali.khan@example.com'),
  ('Maya', 'Shah', 'maya.shah@example.com'),
  ('Noor', 'Rizvi', 'noor.rizvi@example.com'),
  ('Zara', 'Ahmed', 'zara.ahmed@example.com'),
  ('Imran', 'Ali', 'imran.ali@example.com');

INSERT OR IGNORE INTO courses (title, description, instructor_id, start_date, end_date, capacity) VALUES
  ('Database Systems', 'Relational database design, SQL, and DBMS principles.', 1, '2026-05-01', '2026-07-01', 30),
  ('Web Development', 'HTML, CSS, JavaScript and frontend development best practices.', 2, '2026-05-03', '2026-07-03', 40),
  ('Data Visualization', 'Visualization tools, charts, dashboards and storytelling with data.', 3, '2026-05-05', '2026-07-05', 35),
  ('Python Programming', 'Python syntax, data structures, and scripting for automation.', 4, '2026-05-10', '2026-07-10', 45),
  ('Cloud Fundamentals', 'Cloud computing models, services, and deployment workflows.', 5, '2026-05-12', '2026-07-12', 30);

INSERT OR IGNORE INTO modules (course_id, module_title, module_order, description) VALUES
  (1, 'Relational Models', 1, 'Principles of relational database design.'),
  (1, 'SQL Queries', 2, 'SELECT, JOIN, INSERT, UPDATE, DELETE.'),
  (1, 'Normalization', 3, 'Normal forms and schema design.'),
  (2, 'HTML Fundamentals', 1, 'Markup for page structure.'),
  (2, 'CSS Styling', 2, 'Visual design and responsive layouts.'),
  (2, 'JavaScript Essentials', 3, 'DOM interaction and client-side logic.'),
  (3, 'Data Storytelling', 1, 'Use data to craft compelling narratives.'),
  (3, 'Dashboard Design', 2, 'Build dashboards with charts and tables.'),
  (3, 'Visualization Tools', 3, 'Work with chart libraries and visualization best practice.'),
  (4, 'Python Basics', 1, 'Core language syntax and data types.'),
  (4, 'Control Flow', 2, 'Loops, conditionals, and functions.'),
  (4, 'Working with Data', 3, 'Files, APIs, and libraries like pandas.'),
  (5, 'Cloud Architecture', 1, 'Fundamental cloud design patterns.'),
  (5, 'Service Models', 2, 'IaaS, PaaS, SaaS explained.'),
  (5, 'Deployment Workflows', 3, 'Deploy apps using cloud platforms.');

INSERT OR IGNORE INTO enrollments (student_id, course_id) VALUES
  (1, 1),
  (1, 4),
  (2, 1),
  (2, 2),
  (3, 2),
  (3, 3),
  (4, 3),
  (5, 4),
  (5, 5);

INSERT OR IGNORE INTO progress (enrollment_id, module_id, completed, score) VALUES
  (1, 1, 1, 85.0),
  (1, 2, 0, NULL),
  (1, 3, 0, NULL),
  (2, 1, 1, 78.0),
  (2, 2, 1, 82.0),
  (2, 3, 0, NULL),
  (3, 4, 1, 90.0),
  (3, 5, 1, 88.0),
  (3, 6, 0, NULL),
  (4, 7, 1, 91.0),
  (4, 8, 1, 89.0),
  (4, 9, 0, NULL),
  (5, 10, 1, 87.0),
  (5, 11, 0, NULL),
  (5, 12, 0, NULL),
  (6, 13, 1, 84.0),
  (6, 14, 0, NULL),
  (6, 15, 0, NULL),
  (7, 7, 1, 80.0),
  (7, 8, 0, NULL),
  (7, 9, 0, NULL),
  (8, 10, 1, 92.0),
  (8, 11, 1, 88.0),
  (8, 12, 0, NULL),
  (9, 13, 0, NULL),
  (9, 14, 0, NULL),
  (9, 15, 0, NULL);
