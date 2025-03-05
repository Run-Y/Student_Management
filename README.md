# Student Management

## Overview

This project is designed for 'Student Management'. It provides functionalities for student, teacher, administrator.

- **For students:** view credits, GPA and other information, and support course selection and withdrawal operations.

- **For Teachers:** Teachers can enter student grades, delete students, and select the courses they teach.

- **For administrators:** Administrators can view, modify, and delete student information.

## Database Configuration

Before running the application, update the database configuration in `db_config.py`.

- Open `db_config.py`

- Modify the `password` field with your database password:
  
  ```python
  DB_CONFIG = {
      "host": "localhost",
      "port": 5432,
      "database": "your_database_name",
      "user": "postgres",
      "password": "your_password"
      # Change this to your database password
  }  
  ```

## Login Information

The application includes a login interface where users must enter a username and password. User credentials are stored in the `users.json` file.

- To add a new user, edit the `users.json` file and append the new user credentials.

- The file currently contains the following default users:

```json
{
    "users": [
        {"username": "2023SE001", "password": "123456", "role": "Student"},
        {"username": "T001", "password": "123456", "role": "Teacher"},
        {"username": "root", "password": "123456", "role": "Administrator"}
    ]
}
```
