# dashboard.py


import tkinter as tk
from tkinter import ttk, messagebox
from database import get_user_info, get_enrollment, get_course_info_by_teacher


def open_dashboard(user_id, role):
    root = tk.Tk()
    root.title(f"{role} Dashboard")
    root.geometry("500x400")

    user_info = get_user_info(user_id, role)

    ttk.Label(root, text=f"Welcome, {user_info[1]}", font=("Arial", 14, "bold")).pack(pady=10)
    ttk.Label(root, text=f"Role: {role}", font=("Arial", 12)).pack()
    ttk.Label(root, text=f"ID: {user_info[0]}", font=("Arial", 12)).pack(pady=10)

    # 根据角色显示不同功能
    if role == "Student":
        ttk.Button(root, text="View Enrolled Courses", command=lambda: show_courses(root, user_id)).pack(pady=10)
    else:
        ttk.Button(root, text="View Teaching Courses", command=lambda: show_teaching_courses(root, user_id)).pack(
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
    course_window.geometry("500x300")

    columns = ("Course ID", "Course Name", "Teacher", "Status", "Enrollment Date")
    tree = ttk.Treeview(course_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for course in courses:
        tree.insert("", "end", values=course)  # (CourseID, Course_Name, Teacher_Name, Status, Enrollment Date)

    tree.pack(expand=True, fill="both")
    ttk.Button(course_window, text="Close", command=course_window.destroy).pack(pady=5)


def show_teaching_courses(root, teacher_id):
    """
    显示教师所授课程列表
    """
    courses = get_course_info_by_teacher(teacher_id)
    if not courses:
        messagebox.showinfo("Courses", "No courses assigned.")
        return

    course_window = tk.Toplevel(root)
    course_window.title("Teaching Courses")
    course_window.geometry("500x300")

    columns = ("Course ID", "Course Name", "Schedule", "Capacity")
    tree = ttk.Treeview(course_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for course in courses:
        tree.insert("", "end", values=course)  # (CourseID, Course_Name, Schedule, Capacity)

    tree.pack(expand=True, fill="both")
    ttk.Button(course_window, text="Close", command=course_window.destroy).pack(pady=5)


