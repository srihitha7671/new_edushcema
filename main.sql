create database edu1;
use edu1;
CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_description TEXT,
    course_start_date DATE,
    course_end_date DATE
);
CREATE TABLE Instructors (
    instructor_id INT AUTO_INCREMENT PRIMARY KEY,
    instructor_name VARCHAR(255) NOT NULL,
    instructor_email VARCHAR(255),
    instructor_bio TEXT
);
CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    student_email VARCHAR(255),
    student_date_of_birth DATE
);
CREATE TABLE Enrolments (
    enrolment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrolment_date DATE,
    completion_status ENUM('enrolled', 'completed'),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
CREATE TABLE Assessments (
    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    assessment_name VARCHAR(255) NOT NULL,
    assessment_date DATE,
    max_score INT,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
CREATE TABLE Grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT,
    student_id INT,
    score INT,
    FOREIGN KEY (assessment_id) REFERENCES Assessments(assessment_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);
ALTER TABLE Courses ADD COLUMN deleted TINYINT(1) DEFAULT 0;
ALTER TABLE Instructors ADD COLUMN deleted TINYINT(1) DEFAULT 0;
ALTER TABLE Students ADD COLUMN deleted TINYINT(1) DEFAULT 0;
ALTER TABLE Enrolments ADD COLUMN deleted TINYINT(1) DEFAULT 0;
ALTER TABLE Assessments ADD COLUMN deleted TINYINT(1) DEFAULT 0;
ALTER TABLE Grades ADD COLUMN deleted TINYINT(1) DEFAULT 0;

SELECT course_id, course_name, course_description, course_start_date, course_end_date, deleted
FROM Courses;

SELECT instructor_id, instructor_name, instructor_email, instructor_bio, deleted
FROM Instructors;

SELECT student_id, student_name, student_email, student_date_of_birth, deleted
FROM Students;

SELECT enrolment_id, student_id, course_id, enrolment_date, completion_status, deleted
FROM Enrolments;

SELECT assessment_id, course_id, assessment_name, assessment_date, max_score, deleted
FROM Assessments;

SELECT grade_id, assessment_id, student_id, score, deleted
FROM Grades;
-- Insert into Courses
INSERT INTO Courses (course_name, course_description, course_start_date, course_end_date, deleted)
VALUES
('Mathematics', 'An introductory course to Mathematics', '2024-07-01', '2024-12-15', 0),
('Physics', 'Fundamentals of Physics', '2024-07-01', '2024-12-15', 0),
('Chemistry', 'Basic Chemistry concepts', '2024-07-01', '2024-12-15', 0);

-- Insert into Instructors
INSERT INTO Instructors (instructor_name, instructor_email, instructor_bio, deleted)
VALUES
('Dr. Anil Kumar', 'anil.kumar@example.com', 'An expert in Mathematics with 20 years of experience', 0),
('Dr. Pooja Sharma', 'pooja.sharma@example.com', 'Physics professor with 15 years of teaching', 0),
('Dr. Ravi Verma', 'ravi.verma@example.com', 'Chemistry researcher and educator', 0);

-- Insert into Students
INSERT INTO Students (student_name, student_email, student_date_of_birth, deleted)
VALUES
('Aarav Singh', 'aarav.singh@example.com', '2002-05-10', 0),
('Mira Patel', 'mira.patel@example.com', '2001-08-20', 0),
('Rajesh Gupta', 'rajesh.gupta@example.com', '2000-11-15', 0);

-- Insert into Enrolments
INSERT INTO Enrolments (student_id, course_id, enrolment_date, completion_status, deleted)
VALUES
(1, 1, '2024-07-01', 'enrolled', 0),
(2, 2, '2024-07-01', 'enrolled', 0),
(3, 3, '2024-07-01', 'enrolled', 0);

-- Insert into Assessments
INSERT INTO Assessments (course_id, assessment_name, assessment_date, max_score, deleted)
VALUES
(1, 'Mathematics Midterm', '2024-09-15', 100, 0),
(2, 'Physics Midterm', '2024-09-15', 100, 0),
(3, 'Chemistry Midterm', '2024-09-15', 100, 0);

-- Insert into Grades
INSERT INTO Grades (assessment_id, student_id, score, deleted)
VALUES
(1, 1, 85, 0),
(2, 2, 90, 0),
(3, 3, 88, 0);
select * from enrolments;
select * from assessments;
select * from courses;
select * from grades;
select * from students;
select * from instructors;


