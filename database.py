import db_config as connect


def check_login(username, password, role):
    conn = connect.connect_db()
    if not conn:
        return False  # 数据库连接失败

    cursor = conn.cursor()
    table = "student" if role == "Student" else "teacher"
    sql = f"SELECT * FROM {table} WHERE username = %s AND password = %s"
    cursor.execute(sql, (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None

# 获取用户信息
def get_user_info(username, role):
    conn = connect.connect_db()
    if not conn:
        return None  # 连接失败

    cursor = conn.cursor()
    table = "student" if role == "Student" else "teacher"
    sql = f"SELECT * FROM {table} WHERE username = %s"
    cursor.execute(sql, (username,))
    user_info = cursor.fetchone()

    cursor.close()
    conn.close()
    return user_info

def get_stu_info(student_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = "SELECT * FROM student WHERE studentid = %s"
    cur.execute(sql,(student_id,))
    rows = cur.fetchall()
    return rows

def get_course_info():
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = "SELECT course.courseid, course.course_name, course_info.teacherid, major.major_name FROM course_info"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def get_course_info_by_major(major_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT course.courseid, course.course_name, course_info.teacherid, major.major_name "
           "FROM course_info "
           "JOIN course ON course.courseid = course_info.courseid "
           "JOIN major ON major.majorid = course_info.majorid "
           "WHERE course_info.majorid = %s")
    cur.execute(sql, (major_id,))
    rows = cur.fetchall()
    return rows

def get_enrollment(student_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT enrollment.courseid, course.course_name, enrollment.enrollment_date"
           "FROM enrollment"
           "JOIN course on course.courseid = enrollment.courseid"
           "WHERE enrollment.studentid = %s")
    cur.execute(sql,(student_id,))
    rows = cur.fetchall()
    return rows

def enroll_course(student_id, course_id, teacher_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("INSERT INTO enrollment (courseid, teacherid, studentid, status, enrollment_date)"
           "VALUES (%s, %s, %s, 'Success', CURRENT_DATE)")
    if cur.execute(sql,(course_id, teacher_id, student_id,)):
        return True
    else:
        return False

def drop_course(student_id, course_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("DELETE FROM enrollment "
           "WHERE studentid = %s and courseid = %s")
    if cur.execute(sql,(student_id, course_id, )):
        return True
    else:
        return False

def update_stu_info(student_id, course_id, teacher_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("UPDATE grade WHERE studentid = %s and courseid = %s and teacherid = %s")
    if cur.execute(sql,(student_id, course_id, teacher_id, )):
        return True
    else:
        return False

def get_grade(student_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = "SELECT * FROM grade WHERE studentid = %s"
    cur.execute(sql,(student_id,))
    rows = cur.fetchall()
    return rows

def get_course_avg_grade(course_id, teacher_id):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("SELECT count(*) AS num_students, AVG(grade) AS avg_grade"
           "FROM grade"
           "WHERE courseid = %s and teacherid = %s")
    cur.execute(sql,(course_id, teacher_id, ))
    rows = cur.fetchall()
    return rows

def insert_grade(course_id, student_id,  teacher_id, grade, grade_date, enrolLment_date):
    conn = connect.connect_db()
    cur = conn.cursor()
    sql = ("INSERT INTO grade (courseid, studentid. teacherid, grade, grade_date, enrollment_ddate)"
           "VALUES (%s, %s, %s, %s, %s, %s)")
    cur.execute(sql,(course_id, student_id,  teacher_id, grade, grade_date, enrolLment_date, ))
    return

def get_ccourse_avg_grade():




