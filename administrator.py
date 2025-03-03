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
    result = db.get_stuid(current_year, major_code)

    # 提取最大顺序号
    if result[0][0] is not None:
        last_student_id = result[0][0]
        last_sequence = int(last_student_id[-3:])  # 提取最后 3 位顺序号
        new_sequence = last_sequence + 1
    else:
        new_sequence = 1

    # 生成新的学号
    new_student_id = f"{current_year}{major_code}{new_sequence:03d}"
    return new_student_id

def submit_student(name, gender, major, birthday, right_frame):

    if not name or not gender or not major or not birthday:
        messagebox.showwarning("Input Error", "Please fill in all fields!")
        return

    try:
        birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid birthday format! Please use YYYY-MM-DD.")
        return

    today = datetime.datetime.today()
    age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))

    student_id = generate_student_id(major)

    result = f"Student ID: {student_id}\nName: {name}\nGender: {gender}\nMajor: {major}\nBirthday: {birthday}\nAge: {age}"
    if db.add_student(student_id, name, gender, major, birthday, age):
        messagebox.showinfo("Submission Successful", result)
    else:
        messagebox.showinfo("Submission Failed", "Try Again!")

    # 清空表单
    add_student(right_frame)

def add_student(right_frame):
    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text="Add New Student",
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

    tk.Label(form_frame, text="Student Name:", font=font_style, bg="#ffffff", width=label_width, anchor="e").grid(row=0, column=0, pady=6, padx=20, sticky="e")
    name_entry = tk.Entry(form_frame, font=font_style, width=input_width)
    name_entry.grid(row=0, column=1, pady=6, padx=20, sticky="w")

    tk.Label(form_frame, text="Gender:", font=font_style, bg="#ffffff", width=label_width, anchor="e").grid(row=1, column=0, pady=6, padx=20, sticky="e")
    gender_var = tk.StringVar()
    gender_combobox = ttk.Combobox(form_frame, textvariable=gender_var, values=["Male", "Female"], font=font_style, width=input_width - 2)
    gender_combobox.grid(row=1, column=1, pady=6, padx=20, sticky="w")
    gender_combobox.current(0)


    tk.Label(form_frame, text="Major:", font=font_style, bg="#ffffff", width=label_width, anchor="e").grid(row=2, column=0, pady=6, padx=20, sticky="e")
    major_var = tk.StringVar()
    major_combobox = ttk.Combobox(form_frame, textvariable=major_var, font=font_style, width=input_width - 2)
    major_combobox.grid(row=2, column=1, pady=6, padx=20, sticky="w")

    majors = db.get_majors()
    if majors:
        major_combobox["values"] = majors
        major_combobox.current(0)
    else:
        messagebox.showwarning("Error", "Failed to load major list!")

    tk.Label(form_frame, text="Birthday:", font=font_style, bg="#ffffff", width=label_width, anchor="e").grid(row=3, column=0, pady=6, padx=20, sticky="e")
    birthday_entry = tk.Entry(form_frame, font=font_style, width=input_width)
    birthday_entry.grid(row=3, column=1, pady=6, padx=20, sticky="w")

    submit_button = ttk.Button(
        form_frame,
        text="Add",
        command=lambda: submit_student(
            name_entry.get(), gender_var.get(), major_var.get(), birthday_entry.get(), right_frame
        )
    )
    submit_button.grid(row=4, column=0, columnspan=2, pady=15)

    return

def search_stu_by_name(table_frame, StudentName):
    students = db.get_stu_by_name(StudentName)

    for widget in table_frame.winfo_children():
        widget.destroy()

    columns = ("Student ID", "Name", "Age", "Gender", "Major")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for student in students:
        tree.insert("", "end", values=student)

    tree.pack(expand=True, fill="both")

    return tree

def search_stu_by_major(table_frame, MajorID):
    students = db.get_student_by_majors(MajorID)

    for widget in table_frame.winfo_children():
        widget.destroy()


    columns = ("Student ID", "Name", "Age", "Gender")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for student in students:
        tree.insert("", "end", values=student)

    tree.pack(expand=True, fill="both")

    return tree

def get_selected_student(tree):
    selected = tree.selection()
    if selected:
        return tree.item(selected[0])["values"]
    return None


def edit_student(right_frame):
    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text="Edit Student",
        font=("Segoe UI", 22, "bold"),
        fg="#333333",
        bg="#ffffff",
    )
    title_label.pack(pady=(30, 10))

    info_frame = tk.Frame(right_frame, bg="#ffffff")
    info_frame.pack(pady=(30, 10))

    font_style = ("Segoe UI", 14)


    tk.Label(info_frame, text="Student Name:", font=font_style, bg="#ffffff", width=15, anchor="e").grid(
        row=0, column=0, pady=6, padx=20, sticky="e"
    )


    name_entry = tk.Entry(info_frame, font=font_style, width=20)
    name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")


    search_name_button = ttk.Button(info_frame, text="Search", command=lambda: set_tree(search_stu_by_name(table_frame, name_entry.get())))
    search_name_button.grid(row=0, column=2, padx=10, pady=5)

    tk.Label(info_frame, text="Select Major:", font=font_style, bg="#ffffff", width=15, anchor="e").grid(
        row=1, column=0, pady=6, padx=20, sticky="e"
    )

    major_var = tk.StringVar()
    major_combobox = ttk.Combobox(info_frame, textvariable=major_var, font=font_style, width=18)  # 保持统一
    major_combobox.grid(row=1, column=1, pady=5, padx=10, sticky="w")

    search_major_button = ttk.Button(info_frame, text="Search", command=lambda: set_tree(search_stu_by_major(table_frame, major_var.get())))
    search_major_button.grid(row=1, column=2, padx=10, pady=5)

    majors = db.get_majors()
    if majors:
        major_combobox["values"] = majors
    else:
        messagebox.showwarning("Error", "Failed to load major list!")

    table_frame = tk.Frame(right_frame, bg="#ffffff")
    table_frame.pack(padx=20, pady=(0, 20))

    button_frame = tk.Frame(right_frame, bg="#ffffff")
    button_frame.pack(pady=(0, 20))

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

    tree_var = {"tree": None}

    def set_tree(new_tree):
        tree_var["tree"] = new_tree

    def update_student(name, gender, major, birthday, student_id):

        if not name_entry or not gender or not major_var or not birthday:
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return

        try:
            birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid birthday format! Please use YYYY-MM-DD.")
            return


        today = datetime.datetime.today()
        age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))

        result = f"Student ID: {student_id}\nName: {name}\nGender: {gender}\nMajor: {major}\nBirthday: {birthday}\nAge: {age}"
        if db.update_stu(name, birthday, major, gender, age, student_id):
            messagebox.showinfo("Submission Successful", result)
        else:
            messagebox.showinfo("Submission Failed", "Try Again!")

        return

    def edit_selected():
        tree = tree_var["tree"]
        if tree is None:
            messagebox.showwarning("Warning", "Please search for students first!")
            return

        selected_student = get_selected_student(tree)
        if selected_student is None:
            messagebox.showwarning("Warning", "Please select a student to edit!")
            return

        student_id, name, age, gender, major, birthday = selected_student

        edit_form = tk.Toplevel()
        edit_form.title("Edit Student Info")
        edit_form.geometry("400x300")

        tk.Label(edit_form, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(edit_form)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.insert(0, name)

        tk.Label(edit_form, text="Birthday:").grid(row=1, column=0, padx=10, pady=5)
        birth_entry = tk.Entry(edit_form)
        birth_entry.grid(row=1, column=1, padx=10, pady=5)
        birth_entry.insert(0, birthday)

        tk.Label(edit_form, text="Gender:").grid(row=2, column=0, padx=10, pady=5)
        gender_var = tk.StringVar()
        gender_combobox = ttk.Combobox(edit_form, textvariable=gender_var, values=["Male", "Female"], width=18)
        gender_combobox.grid(row=2, column=1, padx=12, pady=5)
        gender_var.set(gender)


        tk.Label(edit_form, text="Major:").grid(row=3, column=0, padx=10, pady=5)
        major_var = tk.StringVar()
        major_combobox = ttk.Combobox(edit_form, textvariable=major_var, width=18)
        major_combobox.grid(row=3, column=1, padx=12, pady=5,)
        major_var.set(major)

        majors = db.get_majors()
        if majors:
            major_combobox["values"] = majors
        else:
            messagebox.showwarning("Error", "Failed to load major list!")

        save_button = ttk.Button(edit_form, text="Update",
                                 command=lambda: update_student(name_entry.get(), gender_var.get(), major_var.get(), birth_entry.get(), student_id))
        save_button.grid(row=5, column=1, pady=10)

    def remove_selected():
        tree = tree_var["tree"]
        if tree is None:
            messagebox.showwarning("Warning", "Please search for students first!")
            return

        selected_student = get_selected_student(tree)
        if selected_student is None:
            messagebox.showwarning("Warning", "Please select a student to edit!")
            return

        student_id = selected_student[0]
        confirm = messagebox.askyesno("Remove Student", f"Are you sure you want to remove {student_id}?")
        if confirm:
            success = db.delete_stu(student_id)
            if success:
                messagebox.showinfo("Remove Student", "Student removed successfully!")
            else:
                messagebox.showerror("Remove Student", "Failed to remove student.")



    button1 = ttk.Button(button_frame, text="Edit", command=lambda: edit_selected())
    button1.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 20))

    button2 = ttk.Button(button_frame, text="Remove", command=lambda: remove_selected())
    button2.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 20))

    return

def manage_student(right_frame):
    for widget in right_frame.winfo_children():
        widget.destroy()

    # 添加大标题
    title_label = tk.Label(
        right_frame,
        text="Student Management",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#ffffff",
    )
    title_label.pack(pady=(40, 20))
    button_frame = tk.Frame(right_frame, bg="#ffffff")
    button_frame.pack(pady=(0, 20))

    style = ttk.Style()
    style.configure("LargeFont.TButton", font=("Segoe UI", 18))

    button1 = ttk.Button(button_frame, text="Add Student", command=lambda: add_student(right_frame),
                         style="LargeFont.TButton")
    button1.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 20))

    button2 = ttk.Button(button_frame, text="Edit Student", command=lambda: edit_student(right_frame),
                         style="LargeFont.TButton")
    button2.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 20))

