import database as db
import tkinter as tk
from tkinter import ttk, messagebox

#TODO: 美化界面 加标题
def show_courses(right_frame, user_id):
    for widget in right_frame.winfo_children():
        widget.destroy()
    # 教师功能：显示所授课程
    courses = db.get_course_info_by_teacher(user_id)
    if not courses:
        messagebox.showinfo("Courses", "No courses assigned.")
        return

    # 创建 Treeview 显示课程信息
    columns = ("Course ID", "Course Name", "Schedule", "Capacity")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for course in courses:
        tree.insert("", "end", values=course)  # (CourseID, Course_Name, Schedule, Capacity)

    tree.pack(expand=True, fill="both", padx=10, pady=10)



def show_course_avg_grade(root, teacher_id):
    """
    显示教师所授课程的平均成绩
    """
    courses = db.get_course_info_by_teacher(teacher_id)
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
        avg_data = db.get_course_avg_grade(course_id, teacher_id)

        if avg_data and avg_data[0] > 0:
            messagebox.showinfo("Course Average", f"Students: {avg_data[0]}\nAverage Grade: {avg_data[1]:.2f}")
        else:
            messagebox.showinfo("Course Average", "No grade data available.")

    ttk.Button(avg_grade_window, text="Get Average Grade", command=fetch_avg_grade).pack(pady=10)
    ttk.Button(avg_grade_window, text="Close", command=avg_grade_window.destroy).pack(pady=5)