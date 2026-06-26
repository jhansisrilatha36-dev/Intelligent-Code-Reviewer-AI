# Intelligent-Code-Reviewer-AI
Built an AI-powered Code Reviewer &amp; Explainer using Generative AI that helps developers understand, debug, and improve their code. The application performs automated code analysis, generates structured bug reports, explains code functionality, and provides optimized solutions with syntax-highlighted output.
# 🛡️ AI Code Reviewer

A premium, developer-first AI code review tool built with **Streamlit** and Python. This tool automates code quality reviews, identifies logical bugs and security vulnerabilities, provides structured optimization suggestions, and generates clean, refactored, and optimized versions of your code instantly.

---

## ✨ Features

- **Double LLM Support**: Fully compatible with both **Google Gemini API** (using `google-generativeai`) and **OpenAI API** (using `openai`).
- **Structured Bug Reports**: Outputs specific issues categorized with **High**, **Medium**, and **Low** severity levels, including clear descriptions, impacts, and solutions.
- **Code Working Explanations**: Provides step-by-step explanations of the code's purpose and logic in simple, clear language.
- **Actionable Optimization Suggestions**: Gives clean bulleted recommendations for style conformance (PEP8, ESLint, etc.), memory safety, performance, and modern syntax.
- **Syntax-Highlighted Refactoring**: Generates a fully-commented and optimized code block ready for deployment.
- **GitHub Portfolio Aesthetic**: A customized modern white-themed user interface with clean typography (Google Fonts - Inter and JetBrains Mono) and minimal styling.
- **Dynamic File Ingestion**: Copy-paste snippets or drag-and-drop source code files (`.py`, `.js`, `.ts`, `.java`, `.cpp`, `.rs`, `.go`, and more).
- **Flexible Context**: Add custom review focus instructions (e.g. "Focus on SQL injection risks" or "Verify thread safety").

---

## 🛠️ Technology Stack

- **Frontend UI**: Streamlit
- **Backend**: Python
- **AI Core**: Google Gemini SDK (`google-generativeai`) & OpenAI SDK (`openai`)
- **Environment Management**: `python-dotenv`

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.10+** installed. Check your version with:
```bash
python --version
```

### 2. Clone and Setup
Navigate to the directory and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. API Key Setup
Create a `.env` file from the template:
```bash
copy .env.example .env
```
Open the `.env` file and add your Gemini or OpenAI API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```
*Note: If you don't configure keys in `.env`, you can also enter them directly in the application's sidebar during runtime.*

### 4. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```
The app will automatically open in your default browser at `http://localhost:8501`.

---

## 📖 How to Use

1. **Configure Model**: Select **Gemini** or **OpenAI** in the sidebar. If your API key isn't loaded from a `.env` file, paste it directly in the key input.
2. **Set Parameters**: Adjust model temperature (lower values lead to more logical, deterministic reviews). Optionally, add custom review instructions (e.g. "Verify complexity is under O(n log n)").
3. **Submit Code**: Either upload a source file or select a language and paste your code directly into the editor.
4. **Analyze**: Click **🚀 Analyze Code**.
5. **Review**: Flip through the generated report tabs:
   - **📖 Explanation**: Simple code working breakdown.
   - **🐛 Bug Report**: Structured severity-coded issues.
   - **💡 Suggestions**: Structural/style improvements.
   - **✨ Optimized Code**: Full refactored copy-paste code.
