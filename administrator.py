import database as db
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

def generate_student_id(major_code):
    """
    自动生成学号
    :param major_code: 专业代码（例如 'SE'）
    :return: 生成的学号（例如 '2023SE001'）
    """
    # 获取当前年份
    current_year = datetime.datetime.now().year

    # 查询数据库中当前年份和专业代码下的最大顺序号
    result = db.get_stuid()

    # 提取最大顺序号
    if result[0] is not None:
        last_student_id = result[0]
        last_sequence = int(last_student_id[-3:])  # 提取最后 3 位顺序号
        new_sequence = last_sequence + 1
    else:
        new_sequence = 1

    # 生成新的学号
    new_student_id = f"{current_year}{major_code}{new_sequence:03d}"
    return new_student_id

def submit_student(name, gender, major, birthday, right_frame):
    """
    提交学生信息
    """
    # 验证输入
    if not name or not gender or not major or not birthday:
        messagebox.showwarning("Input Error", "Please fill in all fields!")
        return

    # 验证生日格式
    try:
        birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid birthday format! Please use YYYY-MM-DD.")
        return

    # 计算年龄
    today = datetime.datetime.today()
    age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))

    student_id = generate_student_id(major)

    # 显示结果
    result = f"Student ID: {student_id}\nName: {name}\nGender: {gender}\nMajor: {major}\nBirthday: {birthday}\nAge: {age}"
    if db.add_student(student_id, name, gender, major, birthday, age):
        messagebox.showinfo("Submission Successful", result)
    else:
        messagebox.showinfo("Submission Failed")

    # 清空表单
    add_student(right_frame)

def add_student(right_frame):
    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text="Add New Student",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    title_label.pack(pady=(40, 20))  # 上方留出 10 像素，下方留出 20 像素

    # 创建表单框架
    form_frame = tk.Frame(right_frame, bg="#ffffff", padx=20, pady=20)
    form_frame.pack(fill=tk.BOTH, expand=True)

    # 姓名输入框
    tk.Label(form_frame, text="Student Name:", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(form_frame, width=30)
    name_entry.grid(row=0, column=1, pady=5)

    # 性别选择框
    tk.Label(form_frame, text="Gender:", bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
    gender_var = tk.StringVar()
    gender_combobox = ttk.Combobox(form_frame, textvariable=gender_var, values=["Male", "Female"], width=27)
    gender_combobox.grid(row=1, column=1, pady=5)
    gender_combobox.current(0)  # 默认选择第一个选项

    # 专业选择框
    tk.Label(form_frame, text="专业:", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
    major_var = tk.StringVar()
    major_combobox = ttk.Combobox(form_frame, textvariable=major_var, width=27)
    major_combobox.grid(row=2, column=1, pady=5)

    # 从数据库中加载专业列表
    majors = db.get_majors()
    if majors:
        major_combobox["values"] = majors
        major_combobox.current(0)  # 默认选择第一个选项
    else:
        messagebox.showwarning("Error", "Failed to load major list!")

    # 生日输入框
    tk.Label(form_frame, text="Birthday:", bg="#ffffff").grid(row=3, column=0, sticky="w", pady=5)
    birthday_entry = tk.Entry(form_frame, width=30)
    birthday_entry.grid(row=3, column=1, pady=5)

    # 提交按钮
    submit_button = ttk.Button(form_frame, text="Add", command=lambda: submit_student(
        name_entry.get(), gender_var.get(), major_var.get(), birthday_entry.get(), right_frame
    ))
    submit_button.grid(row=4, column=1, pady=10)

    return

def remove_student():
    return

def manage_student(right_frame):
    for widget in right_frame.winfo_children():
        widget.destroy()

    # 添加大标题
    title_label = tk.Label(
        right_frame,
        text="Student Management",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    title_label.pack(pady=(40, 20))  # 上方留出 10 像素，下方留出 20 像素

    button_frame = tk.Frame(right_frame, bg="#ffffff")
    button_frame.pack(pady=(0, 20))

    # 创建样式对象
    style = ttk.Style()
    style.configure("LargeFont.TButton", font=("Segoe UI", 18))

    button1 = ttk.Button(button_frame, text="Add Student", command=lambda: add_student(right_frame),
                         style="LargeFont.TButton")
    button1.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 20))

    button2 = ttk.Button(button_frame, text="Remove Student", command=lambda: remove_student(),
                         style="LargeFont.TButton")
    button2.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 20))