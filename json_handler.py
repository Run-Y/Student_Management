import json
import hashlib

JSON_FILE = "users.json"

def hash_password(password):
    """ 生成密码的 SHA256 哈希值 """
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """ 读取 users.json 里的账号数据 """
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data["users"]
    except FileNotFoundError:
        print("错误: 用户数据文件未找到！")
        return []
    except json.JSONDecodeError:
        print("错误: JSON 文件格式错误！")
        return []

def check_login(username, password, role):
    """ 验证账号和哈希密码是否匹配 """
    users = load_users()
    password_hashed = hash_password(password)  # 把输入的密码转换成哈希
    for user in users:
        if user["username"] == username and user["password"] == password_hashed and user["role"] == role:
            return True
    return False
