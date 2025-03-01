# import tkinter as tk
# from tkinter import messagebox
# from json_handler import check_login  # 读取 JSON 进行验证
# from dashboard import open_dashboard
#
# class LoginWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("登录")
#         self.root.geometry("300x200")
#
#         tk.Label(root, text="用户名:").pack()
#         self.username_entry = tk.Entry(root)
#         self.username_entry.pack()
#
#         tk.Label(root, text="密码:").pack()
#         self.password_entry = tk.Entry(root, show="*")
#         self.password_entry.pack()
#
#         tk.Label(root, text="身份:").pack()
#         self.role_var = tk.StringVar(value="Student")
#         tk.Radiobutton(root, text="学生", variable=self.role_var, value="Student").pack()
#         tk.Radiobutton(root, text="老师", variable=self.role_var, value="Teacher").pack()
#
#         tk.Button(root, text="登录", command=self.login).pack()
#
#     def login(self):
#         username = self.username_entry.get()
#         password = self.password_entry.get()
#         role = self.role_var.get()
#
#         if check_login(username, password, role):
#             self.root.destroy()  # 关闭登录窗口
#             open_dashboard(username, role)  # 打开看板
#         else:
#             messagebox.showerror("登录失败", "账号或密码错误")
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = LoginWindow(root)
#     root.mainloop()
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import hashlib
from dashboard import open_dashboard

def check_login(username, password, role):
    """
    Reads user.json and verifies login credentials.
    If the stored password is 32 characters long, assume it's an MD5 hash and compare accordingly.
    Otherwise, compare directly as plaintext.
    """
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for user in data.get("users", []):
                if username == user.get("username") and role == user.get("role"):
                    stored_password = user.get("password")
                    if len(stored_password) == 32:
                        password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
                        if password_hash == stored_password:
                            return True
                    else:
                        if password == stored_password:
                            return True
        return False
    except Exception as e:
        print("Error reading user.json:", e)
        return False

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("User Login")
        self.root.geometry("350x250")
        self.root.configure(bg="#f4f4f4")

        # Styling with ttk
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TLabel", font=("Arial", 11), background="#f4f4f4")
        style.configure("TRadiobutton", background="#f4f4f4", font=("Arial", 10))

        # Frame to contain input fields
        frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
        frame.pack(pady=20)

        ttk.Label(frame, text="Username:").grid(row=0, column=0, pady=5, sticky="w")
        self.username_entry = ttk.Entry(frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=5, sticky="w")
        self.password_entry = ttk.Entry(frame, show="*", font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Role:").grid(row=2, column=0, pady=5, sticky="w")
        self.role_var = tk.StringVar(value="Student")
        student_rb = ttk.Radiobutton(frame, text="Student", variable=self.role_var, value="Student")
        teacher_rb = ttk.Radiobutton(frame, text="Teacher", variable=self.role_var, value="Teacher")
        student_rb.grid(row=2, column=1, sticky="w", padx=5)
        teacher_rb.grid(row=3, column=1, sticky="w", padx=5)

        # Login button
        self.login_button = ttk.Button(frame, text="Login", command=self.login)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=15)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        if check_login(username, password, role):
            self.root.destroy()  # Close login window
            open_dashboard(username, role)  # Open dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()