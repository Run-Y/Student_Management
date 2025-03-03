import database as db
import tkinter as tk
from tkinter import ttk, messagebox

def enroll_course(tree, student_id):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Enroll Course", "Please select a course!")
        return


    selected_course = tree.item(selected_item, "values")
    course_id = selected_course[0]  # 提取课程 ID
    course_name = selected_course[1]  # 提取课程名称
    teacher_name = selected_course[2]  # 提取教师名称


    confirm = messagebox.askyesno("Enroll Course", f"Are you sure you want to enroll {course_name}?")
    if confirm:

        teacher_id = db.get_teacher_id(teacher_name)

        pre_course_id = db.get_pre_course_id(course_id)

        enroll_course_id = db.get_enrollment(student_id)

        pre_course_list = []
        enroll_course_list = []
        for pre_id in pre_course_id:
            pre_course_list.append(pre_id[0])
        for cou_id in enroll_course_id:
            enroll_course_list.append(cou_id[0])

        pre_course_set = set(pre_course_list)
        enroll_course_set = set(enroll_course_list)


        if pre_course_set.issubset(enroll_course_set):

            success = db.enroll_course(student_id, course_id, teacher_id)
            if success:
                messagebox.showinfo("Enroll Course", "Course enrolled successfully!")

                show_courses(tree.master.master, student_id)
            else:
                messagebox.showerror("Enroll Course", "Failed to enroll course.")
        else:
            messagebox.showerror("Enroll Course", "Student is missing some prerequisite courses.")





    return

def show_detail(tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a course.")
        return
    course_id = tree.item(selected_item)["values"][0]

    teacher_name = tree.item(selected_item)["values"][2]

    course_detail = db.get_course_info_for_stu(course_id, teacher_name)

    if course_detail:

        course_id = course_detail[0][0]
        course_name = course_detail[0][1]
        teacher_name = course_detail[0][2]
        credits = course_detail[0][3]
        schedule = course_detail[0][4]
        capacity = course_detail[0][5]

        message = (
            f"Course ID: {course_id}\n"
            f"Course Name: {course_name}\n"
            f"Teacher: {teacher_name}\n"
            f"Credits: {credits}\n"
            f"Schedule: {schedule}\n"
            f"Capacity: {capacity}"
        )

        # 使用 messagebox 显示信息
        messagebox.showinfo("Course Details", message)
    else:
        messagebox.showwarning("No Data", "No course details found.")


def show_course_info(right_frame, student_id):
    for widget in right_frame.winfo_children():
        widget.destroy()


    title_label = tk.Label(
        right_frame,
        text="Course Can Be Enrolled",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#ffffff",
    )
    title_label.pack(pady=(40, 20))

    button_frame = tk.Frame(right_frame, bg="#ffffff")
    button_frame.pack(pady=(0, 20))


    button1 = ttk.Button(button_frame, text="Enroll", command=lambda: enroll_course(tree, student_id),
                         style="LargeFont.TButton")
    button1.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 20))

    table_frame = tk.Frame(right_frame, bg="#ffffff")
    table_frame.pack(padx=20, pady=(0, 20))

    courses = db.get_course_info(student_id)
    if not courses:
        messagebox.showinfo("Courses", "No courses can be enrolled.")
        return

    columns = ("Course ID", "Course Name", "Teacher", "Schedule", "Slots")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")


    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.column("Course ID", width=90, anchor="center")
    tree.column("Course Name", width=150, anchor="center")
    tree.column("Teacher", width=120, anchor="center")
    tree.column("Schedule", width=150, anchor="center")
    tree.column("Slots", width=90, anchor="center")


    for course in courses:
        tree.insert("", "end", values=course)

    tree.bind("<Double-1>", lambda event: show_detail(tree))
    tree.pack(expand=True, fill="both")

    return

def drop_selected_course(tree, student_id):

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Drop Course", "Please select a course!")
        return

    selected_course = tree.item(selected_item, "values")
    course_id = selected_course[0]
    course_name = selected_course[1]
    teacher_name = selected_course[2]
    status = selected_course[3]
    enroll_date = selected_course[4]

    if status == 'Enrolled':
        confirm = messagebox.askyesno("Drop Course", f"Are you sure you want to drop {course_name}?")
        if confirm:

            teacher_id = db.get_teacher_id(teacher_name)

            success = db.drop_course(student_id, course_id, teacher_id, enroll_date)
            if success:
                messagebox.showinfo("Drop Course", "Course dropped successfully!")
                # 刷新表格
                show_courses(tree.master.master, student_id)  # 刷新表格内容
            else:
                messagebox.showerror("Drop Course", "Failed to drop course.")
    else:
        messagebox.showerror("Drop Course", "Courses marked as success or fail cannot be dropped.")

def show_courses(right_frame, student_id):
    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text="Course",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#ffffff",
    )
    title_label.pack(pady=(40, 20))

    button_frame = tk.Frame(right_frame, bg="#ffffff")
    button_frame.pack(pady=(0, 20))

    style = ttk.Style()
    style.configure("LargeFont.TButton", font=("Segoe UI", 14))

    button1 = ttk.Button(button_frame, text="Enroll Course", command=lambda: show_course_info(right_frame, student_id),
                         style="LargeFont.TButton")
    button1.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 20))

    button2 = ttk.Button(button_frame, text="Drop Course", command=lambda: drop_selected_course(tree, student_id),
                         style="LargeFont.TButton")
    button2.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 20))

    table_frame = tk.Frame(right_frame, bg="#ffffff")
    table_frame.pack(padx=20, pady=(0, 20))

    courses = db.get_enrollment(student_id)

    if not courses:
        messagebox.showinfo("Courses", "No courses enrolled.")
        return


    columns = ("Course ID", "Course Name", "Teacher", "Status", "Enrollment Date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")


    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.column("Course ID", width=100, anchor="center")
    tree.column("Course Name", width=150, anchor="center")
    tree.column("Teacher", width=120, anchor="center")
    tree.column("Status", width=100, anchor="center")
    tree.column("Enrollment Date", width=150, anchor="center")

    for course in courses:
        tree.insert("", "end", values=course)

    tree.bind("<Double-1>", lambda event: show_detail(tree))
    tree.pack(expand=True, fill="both")

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


def show_grades(right_frame, student_id):
    for widget in right_frame.winfo_children():
        widget.destroy()

    grades = db.get_student_grades(student_id)
    if not grades:
        messagebox.showinfo("Grades", "No grades available.")
        return

    avg_grade = db.get_student_avg_grade(student_id)
    avg_grade_value = float(avg_grade[0][0])

    sum_credit = db.get_credit_sum(student_id)
    sum_credit_value = float(sum_credit[0][0])


    title_label = tk.Label(
        right_frame,
        text="Grades",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#ffffff",
    )
    title_label.pack(pady=(40, 20))

    info_frame = tk.Frame(right_frame, bg="#ffffff")
    info_frame.pack(padx = 0, pady=(0,20))


    grade_label = tk.Label(
        info_frame,
        text=f"Average Grade: {avg_grade_value:.2f}",
        font=("Segoe UI", 14),
        fg="#555555",
        bg="#ffffff",
    )
    grade_label.pack(side=tk.LEFT, padx=(0,10), pady=(0,20))

    credit_label = tk.Label(
        info_frame,
        text=f"Credit: {sum_credit_value}",
        font=("Segoe UI", 14),
        fg="#555555",
        bg="#ffffff",
    )
    credit_label.pack(side=tk.LEFT, padx=(10,0), pady=(0,20))


    table_frame = tk.Frame(right_frame, bg="#ffffff")
    table_frame.pack(padx=20, pady=(0, 20))

    columns = ("Course ID", "Course Name", "Teacher", "Grade", "Date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for grade in grades:
        tree.insert("", "end", values=grade)

    tree.bind("<Double-1>", lambda event: show_detail(tree))
    tree.pack(expand=True, fill="both")

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



