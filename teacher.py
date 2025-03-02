import database as db
import tkinter as tk
from tkinter import ttk, messagebox


def show_courses(right_frame, user_id):
    for widget in right_frame.winfo_children():
        widget.destroy()

    courses = db.get_course_info_by_teacher(user_id)
    if not courses:
        messagebox.showinfo("Courses", "No courses assigned.")
        return

    columns = ("Course ID", "Course Name", "Schedule", "Capacity")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for course in courses:
        tree.insert("", "end", values=course)

    tree.bind("<Double-1>", lambda event: show_students(right_frame, tree))
    tree.pack(expand=True, fill="both", padx=10, pady=10)


def show_students(right_frame, tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a course.")
        return

    course_id = tree.item(selected_item)["values"][0]  # 获取课程ID

    students = db.get_students_by_course(course_id)  # 这里修正

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
        student_tree.column(col, width=120)

    for student in students:
        student_tree.insert("", "end", values=student)

    student_tree.pack(expand=True, fill="both", padx=10, pady=10)



def update_student_grade(right_frame, student_tree, course_id):
    selected_item = student_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student.")
        return

    student_id = student_tree.item(selected_item[0], "values")[0]

    grade_window = tk.Toplevel(right_frame)
    grade_window.title("Update Grade")

    tk.Label(grade_window, text="Enter New Grade:").pack(pady=5)
    grade_entry = tk.Entry(grade_window)
    grade_entry.pack(pady=5)

    def save_grade():
        new_grade = grade_entry.get()
        if not new_grade.isdigit():
            messagebox.showwarning("Invalid Input", "Grade must be a number.")
            return

        db.update_student_grade(course_id, student_id, new_grade)
        messagebox.showinfo("Success", "Grade updated successfully.")
        grade_window.destroy()
        show_students(right_frame, student_tree)

    tk.Button(grade_window, text="Save", command=save_grade).pack(pady=10)


def delete_student(right_frame, student_tree):
    selected_item = student_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student to delete.")
        return

    student_id = student_tree.item(selected_item[0], "values")[0]

    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
        db.delete_student(student_id)
        messagebox.showinfo("Success", "Student deleted successfully.")
        show_students(right_frame, student_tree)