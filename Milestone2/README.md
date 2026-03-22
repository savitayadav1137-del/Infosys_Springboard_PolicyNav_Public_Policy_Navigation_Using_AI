## 🔐 PolicyNav – Milestone 2
## Secure Authentication System with OTP & JWT

## 📌 Project Overview

#### PolicyNav is developed as part of the Infosys Virtual Internship Program.

In Milestone 2, the focus is on building a secure authentication system that ensures user data protection and safe login mechanisms.

This milestone strengthens the system by integrating modern security practices like encryption, token-based authentication, and OTP verification.

## 🚀 Key Features
## 🔑 Authentication Features
✅ User Signup – New users can register securely
✅ User Login – Authenticated access to system
✅ Forgot Password – Password recovery functionality
✅ Security Question Verification – Extra identity check
✅ OTP-based Authentication – One-time password verification
✅ JWT Token Generation – Secure session handling

🛡 Security Enhancements
## Password Hashing (bcrypt)
   Passwords are never stored in plain text
   Strong encryption ensures safety
## JWT-based Authentication
   Generates secure tokens after login
   Prevents unauthorized access
## Input Validation
   No spaces allowed in passwords/security answers
   Prevents invalid or weak inputs
## Secure Database (SQLite)
   Structured and safe data storage
## Token Expiration Handling
Automatically logs out users after time limit

## 🛠️ Tech Stack
Frontend: Streamlit
Backend: Python
Database: SQLite
Security Libraries:
bcrypt
PyJWT
OTP libraries

## ⚙️ How to Run the Application
1️⃣ Clone the Repository
2️⃣ Install Dependencies
3️⃣ Run the Application
4️⃣ (Optional) Run with ngrok for Public URL

## 📸 Screenshots Included
Milestone 2 includes the following UI pages:
## ✅ Login Page
<img width="1919" height="842" alt="Screenshot 2026-03-21 151902" src="https://github.com/user-attachments/assets/0812fc4b-3fb7-4ceb-a6f4-5c4e4ecbc402" />

## ✅ Signup Page
<img width="1904" height="846" alt="Screenshot 2026-03-21 152030" src="https://github.com/user-attachments/assets/614bf565-2741-4969-8c14-5ff3241d9248" />
## ✅ Forgot Password Page and OTP verification page
<img width="1914" height="848" alt="Screenshot 2026-03-21 151946" src="https://github.com/user-attachments/assets/a7d9d3ad-eabf-4d7d-8f6e-308bf4728b86" />
<img width="1890" height="869" alt="Screenshot 2026-03-21 152538" src="https://github.com/user-attachments/assets/29a07964-e9a6-431c-a5c9-6af5eca5feac" />
<img width="1919" height="880" alt="Screenshot 2026-03-21 152314" src="https://github.com/user-attachments/assets/0ac21b0d-ec10-40f4-a4d3-fb59bb36ea72" />

## 🔐 Security Improvements Compared to Milestone 1

| Feature            | Milestone 1 | Milestone 2     |
|------------------|------------|-----------------|
| Password Hashing | Basic      | bcrypt          |
| Session Handling | Basic      | JWT             |
| OTP Authentication | ❌        | ✅              |
| Input Validation | Limited    | Enhanced        |
| Deployment       | Local      | ngrok Enabled   |

## 🎯 Learning Outcomes
Implemented secure authentication mechanisms
Learned JWT-based session handling
Improved password security with hashing
Understood OTP verification logic
Practiced deploying Streamlit apps using ngrok

## 👩‍💻 Author
Savita Yadav
Infosys Virtual Internship
