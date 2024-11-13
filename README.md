# Time Table Management

This project is a Python-based application designed to streamline schedule management for educational institutions, organizations, or businesses. It combines efficient timetable automation with strong security measures, ensuring that schedules are managed and protected effectively.

---

## Table of Contents

- [Features](#features)
- [Security Practices](#security-practices)
- [Admin Panel](#admin-panel)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
---

## Features

1. **CIA Triad Implementation**  
   Adheres to the principles of Confidentiality, Integrity, and Availability:
   - **Confidentiality**: Access control ensures data is available only to authorized users.
   - **Integrity**: Prevents unauthorized modifications to maintain data consistency.
   - **Availability**: Ensures reliable and consistent access to schedules.

2. **Secure Coding Practices**  
   Follows best practices in secure coding:
   - **Data Validation**: Validates user inputs to mitigate injection attacks and prevent invalid data entry.
   - **Error Handling**: Handles errors securely to prevent data leakage and unexpected application behavior.
   - **Avoidance of Hard-Coded Sensitive Data**: Sensitive information, such as passwords, is never hard-coded. Secure storage and encryption methods are used instead.

3. **Database Management**  
   Utilizes SQLite for efficient and secure data management:
   - **Optimized Queries**: Ensures performance and security when handling large data volumes.
   - **SQL Injection Prevention**: Uses parameterized queries to safeguard against SQL injection risks.

4. **Password Protection**  
   Enforces robust password policies:
   - Minimum length of 10 characters
   - At least one uppercase letter, one lowercase letter, one number, and one special character
   - Prevents common and weak passwords

5. **Automated Scheduling**  
   Generates timetables automatically based on customizable input constraints, reducing human errors and saving time.

6. **User-Friendly Interface**  
   A clean and intuitive interface suitable for non-technical users, allowing easy navigation and quick schedule management.

---

## Security Practices

- **Password Encryption**: Passwords are hashed and stored securely using industry-standard encryption algorithms.
- **Session Management**: Secure session handling with auto-logout on user inactivity.
- **Access Control & Role-Based Permissions**: Implements role-based access control (RBAC) to limit user permissions according to their roles.
- **Privilege Escalation Prevention**: Strict access restrictions prevent unauthorized privilege elevation.
- **Audit Logs**: Tracks user actions and changes within the application, enabling administrators to review activities.
- **Data Encryption**: Encrypts sensitive data in transit and at rest to prevent unauthorized access.

---

## Admin Panel

The Admin Panel is the central management console for administrators to oversee and manage users and roles. It includes:
- **User Management**: Add, update, or delete users and roles.
- **Activity Monitoring**: Keeps detailed logs of user activities to maintain a transparent and accountable environment.
- **Role-Based Permissions**: Assigns permissions based on user roles to ensure appropriate access levels.
- **Privilege Escalation Control**: Prevents unauthorized users from gaining elevated privileges.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lvexol/TIME-TABLE-MANAGEMENT.git
2. **Navigate to the project directory**:
   ```bash
   cd TIME-TABLE-MANAGEMENT
   ```

3. **Install dependencies**:
   Ensure you have Python 3 and pip installed, then install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

---

## Usage

1. **Start the Application**  
   Run the application to access the scheduling interface.
   
2. **Admin Login**  
   Log in as an admin to access the Admin Panel, where you can manage users and schedules.

3. **Automated Scheduling**  
   Enter scheduling constraints and let the system generate optimal timetables.

4. **Manage Users**  
   Add new users, assign roles, and set permissions as needed through the Admin Panel.

---

## Screenshots

![admin pannel](./images/Screenshot%202024-11-13%20152618.png)
![admin pannel](./images/Screenshot%2024-11-13%155304.png)


---

## Future Enhancements

- **Multi-Factor Authentication (MFA)**: Adding an extra layer of security for user logins.
- **Notifications & Reminders**: Automatic notifications for schedule updates or reminders.
- **Data Backup and Recovery**: Scheduled backups to safeguard data integrity.
- **Web-Based Version**: Transition to a web interface for broader accessibility.

---

## Contributing

We welcome contributions to enhance functionality, improve security, or add new features. Please follow these steps:
1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Submit a pull request.

For major changes, please open an issue first to discuss what you would like to modify.

---
