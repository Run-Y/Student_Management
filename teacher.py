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


def generate_course_id(major_code):

    # 查询数据库中当前年份和专业代码下的最大顺序号
    result = db.get_course_id(major_code)

    # 提取最大顺序号
    if result[0][0] is not None:
        last_course_id = result[0][0]
        last_sequence = int(last_course_id[-2:])  # 提取最后 3 位顺序号
        new_sequence = last_sequence + 1
    else:
        new_sequence = 1

    # 生成新的学号
    new_course_id = f"{major_code}{new_sequence:02d}"
    return new_course_id

def submit_course(name, credit, major, schedule, capacity, teacher_id):

    if not name or not credit or not major:
        messagebox.showwarning("Input Error", "Please fill in all fields!")
        return

    course_id = generate_course_id(major)


    if db.add_course(course_id, name, credit, major, schedule, capacity, teacher_id):
        messagebox.showinfo("Success", "Submission Successful")
    else:
        messagebox.showinfo("Submission Failed", "Try Again!")

def update_course_info(course_id, teacher_id, schedule, capacity):

    if not schedule or not capacity:
        messagebox.showwarning("Input Error", "Please fill in all fields!")
        return


    if db.insert_course_info(course_id, teacher_id, schedule, capacity):
        messagebox.showinfo("Success", "Submission Successful")
    else:
        messagebox.showinfo("Submission Failed", "Try Again!")

def add_course(right_frame, teacher_id):

    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text="Add New Course",
        font=("Segoe UI", 22, "bold"),
        fg="#333333",
        bg="#ffffff",
    )
    title_label.pack(pady=(30, 10))

    form_frame = tk.Frame(right_frame, bg="#ffffff")
    form_frame.pack(pady=(30, 10))


    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)

    label_width = 15
    input_width = 20
    font_style = ("Segoe UI", 14)

    tk.Label(form_frame, text="Course Name:", font=font_style, bg="#ffffff", width=label_width, anchor="e").grid(row=0, column=0, pady=6, padx=20, sticky="e")
    name_entry = tk.Entry(form_frame, font=font_style, width=input_width)
    name_entry.grid(row=0, column=1, pady=6, padx=20, sticky="w")

    tk.Label(form_frame, text="Major:", font=font_style, bg="#ffffff", width=label_width, anchor="e").grid(row=1, column=0, pady=6, padx=20, sticky="e")
    major_var = tk.StringVar()
    major_combobox = ttk.Combobox(form_frame, textvariable=major_var, font=font_style, width=input_width - 2)
    major_combobox.grid(row=1, column=1, pady=6, padx=20, sticky="w")

    majors = db.get_majors()
    if majors:
        major_combobox["values"] = majors
    else:
        messagebox.showwarning("Error", "Failed to load major list!")


    tk.Label(form_frame, text="Credit:", font=font_style, bg="#ffffff", width=label_width, anchor="e").grid(row=2, column=0, pady=6, padx=20, sticky="e")
    credit_entry = tk.Entry(form_frame, font=font_style, width=input_width)
    credit_entry.grid(row=2, column=1, pady=6, padx=20, sticky="w")

    tk.Label(form_frame, text="Schedule:", font=font_style, bg="#ffffff", width=label_width, anchor="e").grid(row=3, column=0, pady=6, padx=20, sticky="e")
    schedule_entry = tk.Entry(form_frame, font=font_style, width=input_width)
    schedule_entry.grid(row=3, column=1, pady=6, padx=20, sticky="w")

    tk.Label(form_frame, text="Capacity:", font=font_style, bg="#ffffff", width=label_width, anchor="e").grid(row=4, column=0, pady=6, padx=20, sticky="e")
    capacity_entry = tk.Entry(form_frame, font=font_style, width=input_width)
    capacity_entry.grid(row=4, column=1, pady=6, padx=20, sticky="w")


    submit_button = ttk.Button(
        form_frame,
        text="Add",
        command=lambda: submit_course(
            name_entry.get(), credit_entry.get(), major_var.get(), schedule_entry.get(), capacity_entry.get(), teacher_id
        )
    )
    submit_button.grid(row=5, column=0, columnspan=2, pady=15)


    return

def enroll_course(tree, teacher_id):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a course.")
        return

    course_id = tree.item(selected_item)["values"][0]
    schedule = tree.item(selected_item)["values"][4]
    capacity = tree.item(selected_item)["values"][5]

    update_course_info(course_id, teacher_id, schedule, capacity)

    return


def edit_course(tree, teacher_id):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a course.")
        return


    course_id = tree.item(selected_item)["values"][0]
    schedule = tree.item(selected_item)["values"][4]
    capacity = tree.item(selected_item)["values"][5]



    edit_form = tk.Toplevel()
    edit_form.title("Edit Course Info")
    edit_form.geometry("400x300")

    tk.Label(edit_form, text="Schedule:").grid(row=0, column=0, padx=10, pady=5)
    schedule_entry = tk.Entry(edit_form)
    schedule_entry.grid(row=0, column=1, padx=10, pady=5)
    schedule_entry.insert(0, schedule)

    tk.Label(edit_form, text="Capacity:").grid(row=1, column=0, padx=10, pady=5)
    capacity_entry = tk.Entry(edit_form)
    capacity_entry.grid(row=1, column=1, padx=10, pady=5)
    capacity_entry.insert(0, capacity)


    save_button = ttk.Button(edit_form, text="Enroll",
                             command=lambda: update_course_info(course_id, teacher_id, schedule_entry.get(), capacity_entry.get()))
    save_button.grid(row=5, column=1, pady=10)

    return

def manage_course(right_frame, teacher_id):
    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text="Course Management",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#ffffff",
    )
    title_label.pack(pady=(40, 20))

    table_frame = tk.Frame(right_frame, bg="#ffffff")
    table_frame.pack(padx=20, pady=(0, 20))

    courses = db.get_all_course(teacher_id)

    if not courses:
        messagebox.showinfo("Courses", "No courses available.")
        return

    columns = ("Course ID", "Course Name", "Credit", "Major", "Schedule", "Capacity")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.column("Course ID", width=100, anchor="center")
    tree.column("Course Name", width=150, anchor="center")
    tree.column("Credit", width=80, anchor="center")
    tree.column("Major", width=80, anchor="center")
    tree.column("Schedule", width=150, anchor="center")
    tree.column("Capacity", width=80, anchor="center")

    for course in courses:
        tree.insert("", "end", values=course)

    tree.pack(expand=True, fill="both")

    button_frame = tk.Frame(right_frame, bg="#ffffff")
    button_frame.pack(pady=(10, 20))

    button1 = ttk.Button(button_frame, text="Add New Course", command=lambda: add_course(right_frame, teacher_id),
                         style="LargeFont.TButton")
    button1.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 20))

    button2 = ttk.Button(button_frame, text="Edit Course", command=lambda: edit_course(tree, teacher_id),
                         style="LargeFont.TButton")
    button2.pack(side=tk.LEFT, padx=(10, 10), pady=(0, 20))

    button3 = ttk.Button(button_frame, text="Enroll", command=lambda: enroll_course(tree, teacher_id),
                          style="LargeFont.TButton")
    button3.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 20))


    style = ttk.Style()
    style.configure("LargeFont.TButton", font=("Segoe UI", 14))
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
    return
