import tkinter as tk
from tkinter import ttk, messagebox
import database as db
import teacher as tc
import student as st
import administrator as ad


def show_user_info(right_frame, user_id, role):
    for widget in right_frame.winfo_children():
        widget.destroy()

    user_info = db.get_user_info(user_id, role)
    # 欢迎信息
    welcome_label = tk.Label(
        right_frame,
        text=f"Welcome, {user_info[1]}!",
        font=("Segoe UI", 20, "bold"),
        fg="#333333",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    welcome_label.pack(pady=10)

    # 用户ID
    id_label = tk.Label(
        right_frame,
        text=f"ID: {user_info[0]}",
        font=("Segoe UI", 14),
        fg="#555555",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    id_label.pack(pady=5)

    # 用户角色
    role_label = tk.Label(
        right_frame,
        text=f"Role: {role}",
        font=("Segoe UI", 14),
        fg="#555555",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    role_label.pack(pady=5)

    if role == "Student":
        avg_grade = db.get_student_avg_grade(user_id)
        if avg_grade[0][0] is None:
            avg_grade_value = 0
        else:
            avg_grade_value = float(avg_grade[0][0])
        grade_label = tk.Label(
            right_frame,
            text=f"Average Grade: {avg_grade_value:.2f}",
            font=("Segoe UI", 14),
            fg="#555555",  # 字体颜色
            bg="#ffffff",  # 背景颜色
            )
        grade_label.pack(pady=5)

        sum_credit = db.get_credit_sum(user_id)
        if sum_credit[0][0] is None:
            sum_credit_value = 0
        else:
            sum_credit_value = float(sum_credit[0][0])
        credit_label = tk.Label(
        right_frame,
        text=f"Credit: {sum_credit_value}",
        font=("Segoe UI", 14),
        fg="#555555",  # 字体颜色
        bg="#ffffff",  # 背景颜色
        )
        credit_label.pack(pady=5)


    # TODO:展示一些信息 甭管展示什么 最后再说

def open_admin_dashboard():
    root = tk.Tk()
    root.title(f"Dashboard")
    root.geometry("800x600")

    # 左侧功能区
    left_frame = tk.Frame(root, width=200, bg="#f0f0f0")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    # 右侧显示区域
    right_frame = tk.Frame(root, bg="#ffffff")
    right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)


    button1 = ttk.Button(left_frame, text="Student\nManagement", command=lambda: ad.manage_student(right_frame))
    button1.pack(pady=10, padx=10, fill=tk.X)

    title_label = tk.Label(
        right_frame,
        text="Welcome Back!",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    title_label.pack(pady=(40, 20))  # 上方留出 10 像素，下方留出 20 像素

    root.mainloop()

def open_dashboard(user_id, role):
    root = tk.Tk()
    root.title(f"Dashboard")
    root.geometry("800x600")

    # 左侧功能区
    left_frame = tk.Frame(root, width=200, bg="#f0f0f0")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    # 右侧显示区域
    right_frame = tk.Frame(root, bg="#ffffff")
    right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    show_user_info(right_frame, user_id, role)

    # 添加功能区按钮
    button1 = ttk.Button(left_frame, text="Profile", command=lambda: show_user_info(right_frame, user_id, role))
    button1.pack(pady=10, padx=10, fill=tk.X)

    if role == "Student":
        button2 = ttk.Button(left_frame, text="Grade", command=lambda: st.show_grades(right_frame, user_id))
        button2.pack(pady=10, padx=10, fill=tk.X)
    else:
        button2 = ttk.Button(left_frame, text="Course", command=lambda: tc.show_courses(right_frame, user_id))
        button2.pack(pady=10, padx=10, fill=tk.X)

    if role == "Student":
        button3 = ttk.Button(left_frame, text="Course", command=lambda: st.show_courses(right_frame, user_id))
        button3.pack(pady=10, padx=10, fill=tk.X)
    # else:
    #     button3 = ttk.Button(left_frame, text="Course", command=lambda: tc.show_courses(right_frame, user_id))
    #     button3.pack(pady=10, padx=10, fill=tk.X)

    root.mainloop()


# 主程序
if __name__ == "__main__":
    # 假设用户ID为 student_123 或 teacher_456，角色为 Student 或 Teacher
    #open_admin_dashboard()
    #open_dashboard("T001", "Teacher")
    open_dashboard(user_id="2023SE001", role="Student")
