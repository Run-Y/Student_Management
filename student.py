import database as db
import tkinter as tk
from tkinter import ttk, messagebox

def show_courses(right_frame, student_id):
    for widget in right_frame.winfo_children():
        widget.destroy()

    courses = db.get_enrollment(student_id)
    if not courses:
        messagebox.showinfo("Courses", "No courses enrolled.")
        return

    # 创建 Treeview 显示课程信息
    columns = ("Course ID", "Course Name", "Teacher", "Status", "Enrollment Date")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for course in courses:
        tree.insert("", "end", values=course)  # (CourseID, Course_Name, Schedule, Capacity)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

def show_grades(right_frame, student_id):
    for widget in right_frame.winfo_children():
        widget.destroy()

    grades = db.get_student_grades(student_id)
    if not grades:
        messagebox.showinfo("Grades", "No grades available.")
        return

    # 创建 Treeview 显示课程信息
    columns = ("Course ID", "Course Name", "Teacher", "Grade", "Date")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for grade in grades:
        tree.insert("", "end", values=grade)  # (CourseID, Course_Name, Schedule, Capacity)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

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



