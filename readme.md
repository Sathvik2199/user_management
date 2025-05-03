# 🚀 User Management System

A reliable and secure user management platform built with FastAPI, PostgreSQL, and Docker. This project addresses key security and functional issues and introduces enhanced filtering, validation, and testing features for production-grade user control.

---
## 🚀 **Key Links**  
- **GitHub Repository**: [User Management System](https://github.com/Sathvik2199/user_management)  
- **Closed Issues & Feature: User Search and Filtering API**:
  - [Issue #13 – User Search and Filtering API with Pagination](https://github.com/Sathvik2199/user_management/issues/13)
  - [Issue #11 – Profile Picture URL Validation](https://github.com/Sathvik2199/user_management/issues/11)
  - [Issue #9 – Role Override after Email Verification](https://github.com/Sathvik2199/user_management/issues/9)
  - [Issue #7 – Email and Nickname Uniqueness Validation](https://github.com/Sathvik2199/user_management/issues/7)
  - [Issue #5 – Password Strength Validation](https://github.com/Sathvik2199/user_management/issues/5)
  - [Issue #3 – Trivy Vulnerabilities](https://github.com/Sathvik2199/user_management/issues/3)
  - [Issue #1 – Docker Build Failure](https://github.com/Sathvik2199/user_management/issues/1)  
- **DockerHub**: [DockerHub Link](https://hub.docker.com/repository/docker/sathvik2107/user_management/general)

---
## 💬 **Reflection**

This project was a great hands-on experience in improving a real-world backend system through incremental bug fixes, validations, and feature additions. Tackling bugs like insecure password handling, improper role updates, and missing URL validation gave me solid insights into how easily data integrity and access control can be compromised if not carefully managed. Enhancing the system with a flexible user search API with pagination made the admin experience much more powerful and scalable.

Working on this also pushed me to learn how to handle CI/CD hygiene, secure Docker builds, and maintain a clean test suite. Writing validation logic and ensuring all edge cases are covered in tests improved both my Pydantic modeling and pytest skills. Altogether, this project helped me build confidence in writing production-grade code that’s not just functional but secure and maintainable.

---

## 🔧 Key Features and Issues fixed

| Feature                          | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| **🔍 User Filtering & Search**    | Search users by role, email, name, and registration date with pagination.  |
| **🔒 Strong Password Checks**     | Enforces secure password rules with length, case, digit, and symbol checks.|
| **📩 Email Verification Fix**     | Ensures role is preserved and token validation is secure.                  |
| **🖼️ Profile Picture Validation** | Accepts only properly formatted image URLs (jpg/png/jpeg).                 |
| **🐳 Docker Setup**               | Dockerized app with fixed build errors for consistent deployment.          |
| **🛡️ Dependency Security Fixes** | Removed critical vulnerabilities flagged by Trivy and pip audit.           |

---

## 🐳 Setup & Run

### 📌 Requirements
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL

### 📥 Installation Steps

```bash
git clone https://github.com/Sathvik2199/user_management.git
cd user_management
docker-compose up --build -d
```

Access the API at: [http://localhost/docs](http://localhost/docs)

---

## 🐞 Closed Issues

| ID  | Title                                   | Type   |
|-----|-----------------------------------------|--------|
| #1  | Docker Build Failure                    | Bug    |
| #3  | Trivy vulnerabilities                   | Bug    |
| #5  | Password Strength Validation            | Bug    |
| #7  | Email and Nickname uniqueness validation| Bug    |
| #9  | Role override after email verification  | Bug    |
| #11 | Profile Picture URL Validation          | Bug    |
| #13 | User Search and Filtering API           | Feature|

---

## 🧪 Testing

Run all test cases using:

```bash
docker-compose exec fastapi pytest tests/
```

Test cases include:
- Duplicate email/nickname update prevention
- Secure password requirements
- Token verification without role overwrite
- Search and filtering by role/email

---

## 📦 Deployment Notes

The app is containerized for production. To rebuild and redeploy:

```bash
docker-compose down
docker-compose up --build -d
```

---

## 👨‍💻 Author

- **Name**: Sathvik2199  
- **GitHub**: [github.com/Sathvik2199](https://github.com/Sathvik2199)

---

## 🧠 Learning Outcomes

This project improved my skills in:
- Writing and enforcing backend validation rules
- Debugging and patching deployment pipelines
- Securing API endpoints through access roles
- Implementing full-stack testing for reliability