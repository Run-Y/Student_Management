# dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
from database import (
    get_user_info, get_enrollment, get_course_info_by_teacher,
    drop_course, get_student_grades, get_course_avg_grade
)


def open_dashboard(user_id, role):
    """
    打开学生或教师的 Dashboard
    """
    root = tk.Tk()
    root.title(f"{role} Dashboard")
    root.geometry("600x500")

    user_info = get_user_info(user_id, role)

    ttk.Label(root, text=f"Welcome, {user_info[1]}", font=("Arial", 14, "bold")).pack(pady=10)
    ttk.Label(root, text=f"Role: {role}", font=("Arial", 12)).pack()
    ttk.Label(root, text=f"ID: {user_info[0]}", font=("Arial", 12)).pack(pady=10)

    if role == "Student":
        ttk.Button(root, text="View Enrolled Courses", command=lambda: show_courses(root, user_id)).pack(pady=10)
        ttk.Button(root, text="Drop Course", command=lambda: drop_course_ui(root, user_id)).pack(pady=10)
        ttk.Button(root, text="View Grades", command=lambda: show_grades(root, user_id)).pack(pady=10)
    else:
        ttk.Button(root, text="View Teaching Courses", command=lambda: show_teaching_courses(root, user_id)).pack(
            pady=10)
        ttk.Button(root, text="View Course Avg Grade", command=lambda: show_course_avg_grade(root, user_id)).pack(
            pady=10)

    root.mainloop()


def show_courses(root, student_id):
    """
    显示学生已选课程列表
    """
    courses = get_enrollment(student_id)
    if not courses:
        messagebox.showinfo("Courses", "No courses enrolled.")
        return

    course_window = tk.Toplevel(root)
    course_window.title("Enrolled Courses")
    course_window.geometry("600x350")

    columns = ("Course ID", "Course Name", "Teacher", "Status", "Enrollment Date")
    tree = ttk.Treeview(course_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for course in courses:
        tree.insert("", "end", values=course)

    tree.pack(expand=True, fill="both")
    ttk.Button(course_window, text="Close", command=course_window.destroy).pack(pady=5)


def drop_course_ui(root, student_id):
    """
    退课 UI
    """
    courses = get_enrollment(student_id)
    if not courses:
        messagebox.showinfo("Drop Course", "No courses to drop.")
        return

    drop_window = tk.Toplevel(root)
    drop_window.title("Drop Course")
    drop_window.geometry("400x250")

    ttk.Label(drop_window, text="Select a course to drop:", font=("Arial", 12)).pack(pady=10)

    selected_course = tk.StringVar()
    course_list = [f"{c[0]} - {c[1]}" for c in courses]
    course_dropdown = ttk.Combobox(drop_window, textvariable=selected_course, values=course_list)
    course_dropdown.pack(pady=10)

    def confirm_drop():
        if not selected_course.get():
            messagebox.showwarning("Drop Course", "Please select a course!")
            return

        course_id = selected_course.get().split(" - ")[0]  # 提取课程 ID
        teacher_id = next(c[2] for c in courses if c[0] == course_id)  # 获取教师 ID

        success = drop_course(student_id, course_id, teacher_id)
        if success:
            messagebox.showinfo("Drop Course", "Course dropped successfully!")
        else:
            messagebox.showerror("Drop Course", "Failed to drop course.")

        drop_window.destroy()

    ttk.Button(drop_window, text="Drop", command=confirm_drop).pack(pady=10)
    ttk.Button(drop_window, text="Cancel", command=drop_window.destroy).pack(pady=5)


def show_grades(root, student_id):
    """
    显示学生的成绩
    """
    grades = get_student_grades(student_id)
    if not grades:
        messagebox.showinfo("Grades", "No grades available.")
        return

    grade_window = tk.Toplevel(root)
    grade_window.title("Student Grades")
    grade_window.geometry("600x350")

    columns = ("Course ID", "Course Name", "Teacher", "Grade", "Date")
    tree = ttk.Treeview(grade_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for grade in grades:
        tree.insert("", "end", values=grade)

    tree.pack(expand=True, fill="both")
    ttk.Button(grade_window, text="Close", command=grade_window.destroy).pack(pady=5)


def show_teaching_courses(root, teacher_id):
    """
    显示教师的授课情况
    """
    courses = get_course_info_by_teacher(teacher_id)
    if not courses:
        messagebox.showinfo("Courses", "No courses assigned.")
        return

    course_window = tk.Toplevel(root)
    course_window.title("Teaching Courses")
    course_window.geometry("600x350")

    columns = ("Course ID", "Course Name", "Schedule", "Capacity")
    tree = ttk.Treeview(course_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for course in courses:
        tree.insert("", "end", values=course)

    tree.pack(expand=True, fill="both")
    ttk.Button(course_window, text="Close", command=course_window.destroy).pack(pady=5)


def show_course_avg_grade(root, teacher_id):
    """
    显示教师所授课程的平均成绩
    """
    courses = get_course_info_by_teacher(teacher_id)
    if not courses:
        messagebox.showinfo("Course Average Grades", "No courses assigned.")
        return

    avg_grade_window = tk.Toplevel(root)
    avg_grade_window.title("Course Average Grades")
    avg_grade_window.geometry("400x300")

    ttk.Label(avg_grade_window, text="Select a course:", font=("Arial", 12)).pack(pady=10)

    selected_course = tk.StringVar()
    course_list = [f"{c[0]} - {c[1]}" for c in courses]
    course_dropdown = ttk.Combobox(avg_grade_window, textvariable=selected_course, values=course_list)
    course_dropdown.pack(pady=10)

    def fetch_avg_grade():
        if not selected_course.get():
            messagebox.showwarning("Course Average", "Please select a course!")
            return

        course_id = selected_course.get().split(" - ")[0]
        avg_data = get_course_avg_grade(course_id, teacher_id)

        if avg_data and avg_data[0] > 0:
            messagebox.showinfo("Course Average", f"Students: {avg_data[0]}\nAverage Grade: {avg_data[1]:.2f}")
        else:
            messagebox.showinfo("Course Average", "No grade data available.")

    ttk.Button(avg_grade_window, text="Get Average Grade", command=fetch_avg_grade).pack(pady=10)
    ttk.Button(avg_grade_window, text="Close", command=avg_grade_window.destroy).pack(pady=5)




