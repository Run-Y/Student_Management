import db_config as connect

def get_user_info(user_id, role):
    conn = connect.connect_db()
    cur = conn.cursor()

    if role == "Student":
        sql = """
        SELECT s.StudentID, s.Student_Name, s.Gender, s.Birthday, s.Age, m.Major_Name
        FROM Student s
        JOIN Major m ON s.MajorID = m.MajorID
        WHERE s.StudentID = %s
        """
    elif role == "Teacher":
        sql = """
        SELECT t.TeacherID, t.Teacher_Name
        FROM Teacher t
        WHERE t.TeacherID = %s
        """
    else:
        return None

    cur.execute(sql, (user_id,))
    user_info = cur.fetchone()
    conn.close()

    return user_info

def get_course_info(student_id):
    """
    Retrieves courses assigned to a teacher.
    Returns: (CourseID, Course_Name, Schedule, Capacity)
    """
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT ci.CourseID, c.Course_Name, t.Teacher_Name, ci.Schedule, ci.Capacity "
           "FROM Course_Info ci "
           "JOIN Course c ON ci.CourseID = c.CourseID "
           "JOIN Teacher t ON ci.TeacherID = t.TeacherID WHERE ci.Courseid NOT IN (SELECT e.Courseid FROM enrollment e WHERE e.StudentID = %s and status = 'Success')")
    cur.execute(sql, (student_id, ))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_course_info_by_teacher(teacher_id):
    """
    Retrieves courses assigned to a teacher.
    Returns: (CourseID, Course_Name, Schedule, Capacity)
    """
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT ci.CourseID, c.Course_Name, ci.Schedule, ci.Capacity "
           "FROM Course_Info ci "
           "JOIN Course c ON ci.CourseID = c.CourseID "
           "WHERE ci.TeacherID = %s")
    cur.execute(sql, (teacher_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_teacher_id(teacher_name):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = """
        SELECT t.TeacherID
        FROM Teacher t
        WHERE t.teacher_name = %s
    """

    cur.execute(sql, (teacher_name,))
    teacher_id = cur.fetchone()
    conn.close()
    return teacher_id

#获取选课信息
def get_enrollment(student_id):
    """
    Retrieves courses a student is enrolled in.
    Returns: (CourseID, Course_Name, Teacher_Name, Status, Enrollment Date)
    """
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT e.CourseID, c.Course_Name, t.Teacher_Name, e.Status, e.Enrollment_Date "
           "FROM Enrollment e "
           "JOIN Course c ON e.CourseID = c.CourseID "
           "JOIN Teacher t ON e.TeacherID = t.TeacherID "
           "WHERE e.StudentID = %s")
    cur.execute(sql, (student_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def enroll_course(student_id, course_id, teacher_id):
    """
    Inserts a new enrollment record.
    """
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("INSERT INTO Enrollment (CourseID, TeacherID, StudentID, Status, Enrollment_Date) "
           "VALUES (%s, %s, %s, 'Success', CURRENT_DATE)")
    try:
        cur.execute(sql, (course_id, teacher_id, student_id))
        conn.commit()
        return True
    except Exception as e:
        print("Enrollment Error:", e)
        return False
    finally:
        conn.close()

def drop_course(student_id, course_id, teacher_id):
    """
    Removes a student's enrollment from a course.
    """
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = "DELETE FROM Enrollment WHERE StudentID = %s AND CourseID = %s AND TeacherID = %s"
    try:
        cur.execute(sql, (student_id, course_id, teacher_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Drop Course Error:", e)
        return False
    finally:
        conn.close()


def get_student_grades(student_id):
    """
    获取学生的成绩信息。
    返回：(CourseID, Course_Name, Teacher_Name, Grade, Date)
    """
    conn = connect.connect_db()
    cur = conn.cursor()

    sql = """
    SELECT g.CourseID, c.Course_Name, t.Teacher_Name, g.Grade, g.grade_Date
    FROM Grade g
    JOIN Course c ON g.CourseID = c.CourseID
    JOIN Course_Info ci ON g.CourseID = ci.CourseID
    JOIN Teacher t ON ci.TeacherID = t.TeacherID
    WHERE g.StudentID = %s
    """

    cur.execute(sql, (student_id,))
    rows = cur.fetchall()
    conn.close()

    return rows


def get_course_avg_grade(course_id, teacher_id):
    """
    Retrieves the average grade and student count for a course taught by a specific teacher.
    Returns: (num_students, avg_grade)
    """
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT COUNT(*) AS num_students, AVG(grade) AS avg_grade "
           "FROM grade "
           "WHERE courseid = %s")
    cur.execute(sql, (course_id,))

    row = cur.fetchone()
    conn.close()
    return row if row else (0, None)

def insert_grade(course_id, student_id,  teacher_id, grade, grade_date, enrolLment_date):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("INSERT INTO grade (courseid, studentid. teacherid, grade, grade_date, enrollment_ddate)"
           "VALUES (%s, %s, %s, %s, %s, %s)")
    cur.execute(sql,(course_id, student_id,  teacher_id, grade, grade_date, enrolLment_date, ))
    conn.commit()
    conn.close()
    return

def get_student_avg_grade(student_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT AVG(grade) as avg_grade "
           "FROM grade "
           "WHERE studentid = %s")
    cur.execute(sql,(student_id, ))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_credit_sum(student_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT SUM(c.credits)"
           "FROM course c "
           "JOIN grade g ON c.courseid = g.courseid "
           "WHERE studentid = %s")
    cur.execute(sql,(student_id, ))
    rows = cur.fetchall()
    conn.close()
    return rows

def query_teacher_course(teacher_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT *"
           "FROM course c"
           "JOIN course_info ci ON c.courseid = ci.courseid"
           "WHERE ci.teacherid = %s")
    cur.execute(sql,(teacher_id, ))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_stu(student_id):
    conn = connect.connect_db()
    cur = conn.cursor()

    try:
        conn.autocommit = False

        cur.execute("DELETE FROM grade WHERE studentid = %s;", (student_id,))
        cur.execute("DELETE FROM enrollment WHERE studentid = %s;", (student_id,))
        cur.execute("DELETE FROM student WHERE studentid = %s;", (student_id,))

        conn.commit()

    except:
        conn.rollback()  # Rollback in case of error

    finally:
        conn.close()

def get_stuid():
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT MAX(studentid) "
           "FROM student "
           "WHERE studentid LIKE '{current_year}{major_code}%")

    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_majors():
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT majorid "
           "FROM major ")

    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_student(studentid, name, gender, major, birthday, age):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("INSERT INTO student (studentid, student_name, gender, birthday, age, majorid) "
           "VALUES (%s, %s, %s, %s, %s, %s,)")

    try:
        cur.execute(sql, (studentid, name, gender, birthday, age, major))
        conn.commit()
        return True
    except Exception as e:
        print("Add Student Error:", e)
        return False
    finally:
        conn.close()

def get_enrollment_by_course(course_id):
    """
    获取某课程的所有学生信息。
    返回：(StudentID, Student_Name, Status, Enrollment Date)
    """
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("""
        SELECT s.StudentID, s.Student_Name, e.Status, e.Enrollment_Date
        FROM Enrollment e
        JOIN Student s ON e.StudentID = s.StudentID
        WHERE e.CourseID = %s
    """)
    cur.execute(sql, (course_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def update_student_grade(student_id, course_id, grade):
    conn = connect.connect_db()
    cur = conn.cursor()

    sql = """
    INSERT INTO Grade (CourseID, StudentID, Grade, Date)
    VALUES (%s, %s, %s, CURRENT_DATE)
    ON DUPLICATE KEY UPDATE Grade = VALUES(Grade), Date = VALUES(Date)
    """

    cur.execute(sql, (course_id, student_id, grade))
    conn.commit()
    conn.close()


def delete_student(student_id, course_id):
    conn = connect.connect_db()
    cur = conn.cursor()

    sql1 = "DELETE FROM Grade WHERE StudentID = %s AND CourseID = %s"
    sql2 = "DELETE FROM Enrollment WHERE StudentID = %s AND CourseID = %s"

    cur.execute(sql1, (student_id, course_id))
    cur.execute(sql2, (student_id, course_id))

    conn.commit()
    conn.close()


def get_students_by_course(course_id):
    conn = connect.connect_db()
    cur = conn.cursor()

    sql = """
    SELECT s.StudentID, s.Student_Name, s.Gender, m.Major_Name, 
           COALESCE(CAST(g.Grade AS TEXT), '-') AS Grade
    FROM Enrollment e
    JOIN Student s ON e.StudentID = s.StudentID
    JOIN Major m ON s.MajorID = m.MajorID
    LEFT JOIN Grade g ON g.StudentID = s.StudentID AND g.CourseID = e.CourseID
    WHERE e.CourseID = %s
    """

    cur.execute(sql, (course_id,))
    students = cur.fetchall()
    conn.close()

    return students







