import tkinter as tk
from tkinter import messagebox
from json_handler import check_login  # 读取 JSON 进行验证
from dashboard import open_dashboard

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("登录")
        self.root.geometry("300x200")

        tk.Label(root, text="用户名:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="密码:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Label(root, text="身份:").pack()
        self.role_var = tk.StringVar(value="Student")
        tk.Radiobutton(root, text="学生", variable=self.role_var, value="Student").pack()
        tk.Radiobutton(root, text="老师", variable=self.role_var, value="Teacher").pack()

        tk.Button(root, text="登录", command=self.login).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        if check_login(username, password, role):
            self.root.destroy()  # 关闭登录窗口
            open_dashboard(username, role)  # 打开看板
        else:
            messagebox.showerror("登录失败", "账号或密码错误")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
