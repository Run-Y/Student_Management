import tkinter as tk
from database import get_user_info

def open_dashboard(username, role):
    root = tk.Tk()
    root.title(f"{role} 看板")
    root.geometry("400x300")

    user_info = get_user_info(username, role)

    tk.Label(root, text=f"欢迎, {user_info[1]}").pack()  # 显示用户名
    tk.Label(root, text=f"身份: {role}").pack()
    tk.Label(root, text=f"ID: {user_info[0]}").pack()

    if role == "Student":
        tk.Button(root, text="查看选课情况").pack()
    else:
        tk.Button(root, text="查看授课学生").pack()

    root.mainloop()
