# 🤖 AI Code Review Portal

An AI-powered web application that automatically reviews Python code, identifies potential bugs, provides improvement suggestions, recommends best practices, and analyzes time complexity using Google Gemini AI.

## 🌐 Live Demo

👉 https://ai-code-review-portal.onrender.com/login

## ✨ Features

- User Registration and Login
- Upload Python (.py) files
- AI-powered code review
- Code Quality Score
- Bug Detection
- Improvement Suggestions
- Best Practice Recommendations
- Time Complexity Analysis
- Review History
- User Dashboard
- Secure Session Management

## 🛠️ Tech Stack

**Frontend**
- HTML5
- CSS3
- JavaScript
- Bootstrap

**Backend**
- Python
- Flask

**Database**
- MySQL

**AI Integration**
- Google Gemini API
- Google GenAI SDK

**Deployment**
- Render

## 📂 Project Structure

```text
AI-Code-Review-Portal/
│
├── app.py
├── requirements.txt
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── reviews.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── database/
│   └── db.py
├── utils/
│   └── gemini_ai.py
└── uploads/
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Code-Review-Portal
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

> Never upload your actual `.env` file or API key to GitHub.

### 6. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 🔄 How It Works

```text
User Login/Register
        ↓
Dashboard
        ↓
Upload Python File
        ↓
Flask Backend
        ↓
Gemini AI Analysis
        ↓
Code Review Generated
        ↓
Store Review
        ↓
Display Review History
```

## 🔐 Security

Sensitive information such as Gemini API keys and database credentials should be stored using environment variables and should never be committed to GitHub.

## 🚀 Future Enhancements

- Support Java, C and C++
- GitHub repository analysis
- Security vulnerability detection
- AI-generated corrected code
- PDF code review reports
- Code complexity visualization
- Admin analytics dashboard

## 👩‍💻 Author

**Sathya B**

Computer Science and Engineering Student

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐.
