import database as db
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def show_courses(right_frame, user_id):
    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text="Your Courses",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#ffffff",
    )
    title_label.pack(pady=(40, 20))

    table_frame = tk.Frame(right_frame, bg="#ffffff")
    table_frame.pack(padx=20, pady=10)

    courses = db.get_course_info_by_teacher(user_id)
    if not courses:
        messagebox.showinfo("Courses", "No courses assigned.")
        return

    columns = ("Course ID", "Course Name", "Schedule", "Capacity")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.column("Course ID", width=100, anchor="center")
    tree.column("Course Name", width=180, anchor="center")
    tree.column("Schedule", width=180, anchor="center")
    tree.column("Capacity", width=100, anchor="center")

    for course in courses:
        tree.insert("", "end", values=course)

    tree.bind("<Double-1>", lambda event: show_students(right_frame, tree))
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    style = ttk.Style()
    style.configure("Treeview",
                    font=("Segoe UI", 12),
                    background="#ffffff",
                    foreground="#333333",
                    rowheight=25,
                    fieldbackground="#ffffff")
    style.map("Treeview", background=[("selected", "#0078d7")])


    style.configure("Treeview.Heading",
                    font=("Segoe UI", 12, "bold"),
                    background="#f0f0f0",
                    foreground="#333333")

def show_students(right_frame, tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a course.")
        return

    course_id = tree.item(selected_item)["values"][0]  # 获取课程ID

    students = db.get_students_by_course(course_id)

    if not students:
        messagebox.showinfo("Students", "No students enrolled in this course.")
        return

    for widget in right_frame.winfo_children():
        widget.destroy()



    # 创建 Treeview 显示学生信息
    columns = ("Student ID", "Name", "Gender", "Major", "Grade", "Grade_date")
    student_tree = ttk.Treeview(right_frame, columns=columns, show="headings")

    for col in columns:
        student_tree.heading(col, text=col)
        student_tree.column(col, width=120, anchor="center")

    student_tree.column("Student ID", width=90, anchor="center")
    student_tree.column("Name", width=80, anchor="center")
    student_tree.column("Gender", width=80, anchor="center")
    student_tree.column("Major", width=160, anchor="center")
    student_tree.column("Grade", width=80, anchor="center")
    student_tree.column("Grade_date", width=120, anchor="center")

    for student in students:
        student_tree.insert("", "end", values=student)

    student_tree.bind("<Double-1>", lambda event: add_grade(student_tree, course_id))
    student_tree.pack(expand=True, fill="both", padx=10, pady=10)

    # 添加删除学生按钮
    delete_button = tk.Button(right_frame, text="Delete Student", command=lambda: delete_student(student_tree, course_id))
    delete_button.pack(pady=10)

def add_grade(student_tree, course_id):
    selected_item = student_tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student.")
        return

    student_data = student_tree.item(selected_item)["values"]
    student_id, student_name, _, _, grade, _ = student_data

    if grade != "-":
        messagebox.showinfo("Info", f"Student {student_name} already has a grade: {grade}")
        return

    grade = simpledialog.askstring("Input", f"Enter grade for {student_name}:")
    if not grade:
        return
    if 0 > int(grade) or int(grade) > 5:
        messagebox.showwarning("Input Error", "Grade must be between 0 and 5.")
        return

    grade_date = simpledialog.askstring("Input", "Enter grade date (YYYY-MM-DD):")
    if not grade_date:
        return

    enrollment_date = db.get_enrollment_date(course_id, student_id)  # 从数据库获取入学日期
    if not enrollment_date:
        messagebox.showerror("Error", "Failed to retrieve enrollment date.")
        return

    db.insert_grade(course_id, student_id, grade, grade_date, enrollment_date)
    messagebox.showinfo("Success", "Grade added successfully!")
    show_students(student_tree.master, student_tree)

def delete_student(student_tree, course_id):
    selected_item = student_tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student.")
        return

    student_data = student_tree.item(selected_item)["values"]
    student_id, student_name, *_ = student_data

    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {student_name}?")
    if not confirm:
        return

    db.delete_enrollment(student_id, course_id)
    messagebox.showinfo("Success", f"Student {student_name} deleted successfully!")
    show_students(student_tree.master, student_tree)  # 重新加载学生列表

