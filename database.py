import db_config as connect

def get_user_info(user_id, role):
    conn = connect.connect_db()
    cur = conn.cursor()

    if role == "Student":
        sql = """
        SELECT *
        FROM student_info_view
        WHERE StudentID = %s
        """
    elif role == "Teacher":
        sql = """
        SELECT *
        FROM teacher_info_view
        WHERE TeacherID = %s
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

def insert_grade(course_id, student_id, grade, grade_date, enrollment_date):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("INSERT INTO grade (courseid, studentid, grade, grade_date, enrollment_date) "
           "VALUES (%s, %s, %s, %s, %s)")
    cur.execute(sql, (course_id, student_id, grade, grade_date, enrollment_date))
    conn.commit()
    conn.close()

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

def delete_stu(student_id):
    conn = connect.connect_db()
    cur = conn.cursor()

    try:
        conn.autocommit = False  # 关闭自动提交

        cur.execute("DELETE FROM grade WHERE studentid = %s;", (student_id,))
        cur.execute("DELETE FROM enrollment WHERE studentid = %s;", (student_id,))
        cur.execute("DELETE FROM student WHERE studentid = %s;", (student_id,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()  # 发生错误时回滚
        print(f"Error deleting student {student_id}: {e}")
        return False

    finally:
        cur.close()  # 关闭游标
        conn.close()  # 关闭连接

def get_stuid(current_year, major_code):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT MAX(studentid) "
           "FROM student "
           "WHERE studentid LIKE %s")

    pattern = f"{current_year}{major_code}%"
    cur.execute(sql, ([pattern, ]))
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
           "VALUES (%s, %s, %s, %s, %s, %s)")

    try:
        cur.execute(sql, (studentid, name, gender, birthday, age, major))
        conn.commit()
        return True
    except Exception as e:
        print("Add Student Error:", e)
        return False
    finally:
        conn.close()

def get_students_by_course(course_id):
    conn = connect.connect_db()
    cur = conn.cursor()

    sql = """
    SELECT s.StudentID, s.Student_Name, s.Gender, m.Major_Name, 
           COALESCE(CAST(g.Grade AS TEXT), '-') AS Grade,
           COALESCE(CAST(g.Grade_date AS TEXT), '-') AS Grade_date
    FROM Enrollment e
    JOIN Student s ON e.StudentID = s.StudentID
    JOIN Major m ON s.MajorID = m.MajorID
    LEFT JOIN Grade g ON g.StudentID = s.StudentID AND g.CourseID = e.CourseID
    WHERE e.CourseID = %s
    ORDER BY Grade_date DESC
    """

    cur.execute(sql, (course_id,))
    students = cur.fetchall()
    conn.close()

    return students

def get_enrollment_date(course_id, student_id):
    conn = connect.connect_db()
    cur = conn.cursor()

    sql = """
    SELECT enrollment_date 
    FROM enrollment 
    WHERE courseid = %s AND studentid = %s
    """

    cur.execute(sql, (course_id, student_id))
    result = cur.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None

def get_student_by_majors(major):
    conn = connect.connect_db()
    cur = conn.cursor()

    sql = ("SELECT s.studentid, s.student_name, s.age, s.gender, s.majorid, s.birthday "
           "FROM student s "
           "WHERE majorid = %s")

    cur.execute(sql, (major,))
    students = cur.fetchall()
    conn.close()

    return students

def get_stu_by_name(Name):
    conn = connect.connect_db()
    cur = conn.cursor()

    sql = ("SELECT s.studentid, s.student_name, s.age, s.gender, s.majorid, s.birthday "
           "FROM student s "
           "WHERE student_name = %s")

    cur.execute(sql, (Name,))
    students = cur.fetchall()
    conn.close()

    return students

def update_stu(Name, Birthday, Major, Gender, Age, StudentId):
    conn = connect.connect_db()
    cur = conn.cursor()

    sql = ("UPDATE student "
           "SET student_name = %s, birthday = %s, majorid = %s, gender = %s, age = %s "
           "WHERE studentid = %s")

    try:
        cur.execute(sql, (Name, Birthday, Major, Gender, Age, StudentId))
        conn.commit()
        return True
    except Exception as e:
        print("Add Student Error:", e)
        return False
    finally:
        conn.close()







