import database as db
import tkinter as tk
from tkinter import ttk, messagebox

def enroll_course(tree, student_id):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Enroll Course", "Please select a course!")
        return

    # 获取选中课程的值
    selected_course = tree.item(selected_item, "values")
    course_id = selected_course[0]  # 提取课程 ID
    course_name = selected_course[1]  # 提取课程名称
    teacher_name = selected_course[2]  # 提取教师名称

    # 弹出确认窗口
    confirm = messagebox.askyesno("Enroll Course", f"Are you sure you want to enroll {course_name}?")
    if confirm:
        # 获取教师 ID
        teacher_id = db.get_teacher_id(teacher_name)

        # 调用退课函数
        success = db.enroll_course(student_id, course_id, teacher_id)
        if success:
            messagebox.showinfo("Enroll Course", "Course enrolled successfully!")
            # 刷新表格
            show_courses(tree.master.master, student_id)  # 刷新表格内容
        else:
            messagebox.showerror("Enroll Course", "Failed to enroll course.")

    return

def show_course_info(right_frame, student_id):
    for widget in right_frame.winfo_children():
        widget.destroy()

    # 添加大标题
    title_label = tk.Label(
        right_frame,
        text="Course Can Be Enrolled",
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

    button1 = ttk.Button(button_frame, text="Enroll", command=lambda: enroll_course(tree, student_id),
                         style="LargeFont.TButton")
    button1.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 20))

    # 创建表格容器
    table_frame = tk.Frame(right_frame, bg="#ffffff")
    table_frame.pack(padx=20, pady=(0, 20))

    courses = db.get_course_info(student_id)
    if not courses:
        messagebox.showinfo("Courses", "No courses can be enrolled.")
        return

    columns = ("Course ID", "Course Name", "Teacher", "Schedule", "Capacity")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

    # 设置列标题
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")  # 居中对齐

    tree.column("Course ID", width=90, anchor="center")  # 第一列窄一点
    tree.column("Course Name", width=150, anchor="center")  # 第二列宽一点
    tree.column("Teacher", width=120, anchor="center")  # 第三列中等宽度
    tree.column("Schedule", width=150, anchor="center")  # 第四列窄一点
    tree.column("Capacity", width=90, anchor="center")  # 第五列中等宽度

    # 插入数据
    for course in courses:
        tree.insert("", "end", values=course)

    # 显示表格
    tree.pack(expand=True, fill="both")

    style = ttk.Style()
    # 设置表格样式
    style.theme_use("default")  # 使用默认主题
    style.configure("Treeview",
                    font=("Segoe UI", 12),  # 设置表格字体大小
                    background="#ffffff",
                    foreground="#333333",
                    rowheight=25,
                    fieldbackground="#ffffff")
    style.map("Treeview", background=[("selected", "#0078d7")])  # 选中行的背景颜色

    # 设置表头样式
    style.configure("Treeview.Heading",
                    font=("Segoe UI", 12, "bold"),
                    background="#f0f0f0",  # 表头背景颜色
                    foreground="#333333")  # 表头字体颜色

    return

def drop_selected_course(tree, student_id):
    """
    退选已选课程
    """
    # 获取选中的课程
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Drop Course", "Please select a course!")
        return

    # 获取选中课程的值
    selected_course = tree.item(selected_item, "values")
    course_id = selected_course[0]  # 提取课程 ID
    course_name = selected_course[1]  # 提取课程名称
    teacher_name = selected_course[2]  # 提取课程名称

    # 弹出确认窗口
    confirm = messagebox.askyesno("Drop Course", f"Are you sure you want to drop {course_name}?")
    if confirm:
        # 获取教师 ID
        teacher_id = db.get_teacher_id(teacher_name)

        # 调用退课函数
        print(student_id, course_id,teacher_id)
        success = db.drop_course(student_id, course_id, teacher_id)
        if success:
            messagebox.showinfo("Drop Course", "Course dropped successfully!")
            # 刷新表格
            show_courses(tree.master.master, student_id)  # 刷新表格内容
        else:
            messagebox.showerror("Drop Course", "Failed to drop course.")

# def drop_course_ui(student_id):
#     """
#     退课 UI
#     """
#     courses = db.get_enrollment(student_id)
#     if not courses:
#         messagebox.showinfo("Drop Course", "No courses to drop.")
#         return
#
#     drop_window = tk.Tk()
#     drop_window.title("Drop Course")
#     drop_window.geometry("400x250")
#
#     ttk.Label(drop_window, text="Select a course to drop:", font=("Arial", 12)).pack(pady=10)
#
#     selected_course = tk.StringVar()
#     course_list = [f"{c[0]} - {c[1]}" for c in courses]
#     print(f"Course List: {course_list}")
#     # 创建 Combobox，但不绑定到 StringVar
#     course_dropdown = ttk.Combobox(drop_window, values=course_list)
#     course_dropdown.pack(pady=10)
#
#     # 默认选中第一项
#     if course_list:
#         course_dropdown.current(0)
#
#     def confirm_drop(selected_course):
#         selected = selected_course.get()
#         print(f"Selected Course: {selected}")  # 打印选中的课程
#         if not selected_course.get():
#             messagebox.showwarning("Drop Course", "Please select a course!")
#             return
#
#         course_id = selected_course.get().split(" - ")[0]  # 提取课程 ID
#         teacher_id = next(c[2] for c in courses if c[0] == course_id)  # 获取教师 ID
#
#         success = db.drop_course(student_id, course_id, teacher_id)
#         if success:
#             messagebox.showinfo("Drop Course", "Course dropped successfully!")
#         else:
#             messagebox.showerror("Drop Course", "Failed to drop course.")
#
#         drop_window.destroy()
#
#     ttk.Button(drop_window, text="Drop", command= lambda: confirm_drop(selected_course)).pack(pady=10)
#     ttk.Button(drop_window, text="Cancel", command= lambda: drop_window.destroy()).pack(pady=5)

def show_courses(right_frame, student_id):
    for widget in right_frame.winfo_children():
        widget.destroy()

    # 添加大标题
    title_label = tk.Label(
        right_frame,
        text="Course",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    title_label.pack(pady=(40, 20))  # 上方留出 10 像素，下方留出 20 像素

    button_frame = tk.Frame(right_frame, bg="#ffffff")
    button_frame.pack(pady=(0, 20))

    # 创建样式对象
    style = ttk.Style()
    style.configure("LargeFont.TButton", font=("Segoe UI", 14))

    button1 = ttk.Button(button_frame, text="Enroll Course", command=lambda: show_course_info(right_frame, student_id),
                         style="LargeFont.TButton")
    button1.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 20))

    button2 = ttk.Button(button_frame, text="Drop Course", command=lambda: drop_selected_course(tree, student_id),
                         style="LargeFont.TButton")
    button2.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 20))

    # 创建表格容器
    table_frame = tk.Frame(right_frame, bg="#ffffff")
    table_frame.pack(padx=20, pady=(0, 20))

    courses = db.get_enrollment(student_id)

    if not courses:
        messagebox.showinfo("Courses", "No courses enrolled.")
        return



    # 创建 Treeview 显示成绩信息
    columns = ("Course ID", "Course Name", "Teacher", "Status", "Enrollment Date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

    # 设置列标题
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")  # 居中对齐

    tree.column("Course ID", width=100, anchor="center")    # 第一列窄一点
    tree.column("Course Name", width=150, anchor="center") # 第二列宽一点
    tree.column("Teacher", width=120, anchor="center")     # 第三列中等宽度
    tree.column("Status", width=100, anchor="center")        # 第四列窄一点
    tree.column("Enrollment Date", width=150, anchor="center")        # 第五列中等宽度

    # 插入数据
    for course in courses:
        tree.insert("", "end", values=course)

    # 显示表格
    tree.pack(expand=True, fill="both")

    # 设置表格样式
    style.theme_use("default")  # 使用默认主题
    style.configure("Treeview",
                    font=("Segoe UI", 12),  # 设置表格字体大小
                    background="#ffffff",
                    foreground="#333333",
                    rowheight=25,
                    fieldbackground="#ffffff")
    style.map("Treeview", background=[("selected", "#0078d7")])  # 选中行的背景颜色

    # 设置表头样式
    style.configure("Treeview.Heading",
                    font=("Segoe UI", 12, "bold"),
                    background="#f0f0f0",  # 表头背景颜色
                    foreground="#333333")  # 表头字体颜色


def show_grades(right_frame, student_id):
    # 清空右侧显示区域
    for widget in right_frame.winfo_children():
        widget.destroy()

    # 获取成绩数据
    grades = db.get_student_grades(student_id)
    if not grades:
        messagebox.showinfo("Grades", "No grades available.")
        return

    avg_grade = db.get_student_avg_grade(student_id)
    avg_grade_value = float(avg_grade[0][0])

    sum_credit = db.get_credit_sum(student_id)
    sum_credit_value = float(sum_credit[0][0])


    # 添加大标题
    title_label = tk.Label(
        right_frame,
        text="Grades",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    title_label.pack(pady=(40, 20))  # 上方留出 10 像素，下方留出 20 像素

    info_frame = tk.Frame(right_frame, bg="#ffffff")
    info_frame.pack(padx = 0, pady=(0,20))

    # 显示平均成绩和学分
    grade_label = tk.Label(
        info_frame,
        text=f"Average Grade: {avg_grade_value:.2f}",
        font=("Segoe UI", 14),
        fg="#555555",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    grade_label.pack(side=tk.LEFT, padx=(0,10), pady=(0,20))  # 靠左显示

    credit_label = tk.Label(
        info_frame,
        text=f"Credit: {sum_credit_value}",
        font=("Segoe UI", 14),
        fg="#555555",  # 字体颜色
        bg="#ffffff",  # 背景颜色
    )
    credit_label.pack(side=tk.LEFT, padx=(10,0), pady=(0,20))  # 靠左显示，与 grade_label 并排


    # 创建表格容器
    table_frame = tk.Frame(right_frame, bg="#ffffff")
    table_frame.pack(padx=20, pady=(0, 20))

    # 创建 Treeview 显示成绩信息
    columns = ("Course ID", "Course Name", "Teacher", "Grade", "Date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

    # 设置列标题
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")  # 居中对齐

    # 插入数据
    for grade in grades:
        tree.insert("", "end", values=grade)

    # 显示表格
    tree.pack(expand=True, fill="both")

    # 设置表格样式
    style = ttk.Style()
    style.theme_use("default")  # 使用默认主题
    style.configure("Treeview",
                    font=("Segoe UI", 12),  # 设置表格字体大小
                    background="#ffffff",
                    foreground="#333333",
                    rowheight=25,
                    fieldbackground="#ffffff")
    style.map("Treeview", background=[("selected", "#0078d7")])  # 选中行的背景颜色

    # 设置表头样式
    style.configure("Treeview.Heading",
                    font=("Segoe UI", 12, "bold"),
                    background="#f0f0f0",  # 表头背景颜色
                    foreground="#333333")  # 表头字体颜色



