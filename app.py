import streamlit as st
import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium White Theme CSS Injection
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global styling */
    .stApp {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #111111 !important;
    }

    /* Code editor area font styling */
    .stTextArea textarea {
        background-color: #FAFAFA !important;
        color: #111111 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        padding: 12px !important;
    }

    .stTextArea textarea:focus {
        border-color: #0f172a !important;
        box-shadow: 0 0 0 1px #0f172a !important;
    }

    /* Sidebar custom styling */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #0F172A !important;
    }

    /* Buttons styling */
    div.stButton > button {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border: 1px solid #0F172A !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }

    div.stButton > button:hover {
        background-color: #1E293B !important;
        border-color: #1E293B !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
        transform: translateY(-1px) !important;
    }

    div.stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background-color: #F8FAFC !important;
        border: 1px dashed #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    /* Custom tabs styling */
    button[data-baseweb="tab"] {
        color: #64748B !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        background-color: transparent !important;
        border-bottom: 2px solid transparent !important;
        padding: 10px 16px !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0F172A !important;
        border-bottom: 2px solid #0F172A !important;
    }

    /* Card designs for findings */
    .card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.01) !important;
    }

    .bug-card-high {
        border-left: 4px solid #EF4444 !important; /* Tailwind red-500 */
    }

    .bug-card-medium {
        border-left: 4px solid #F59E0B !important; /* Tailwind amber-500 */
    }

    .bug-card-low {
        border-left: 4px solid #64748B !important; /* Tailwind slate-500 */
    }

    .badge {
        display: inline-block;
        padding: 0.2em 0.6em;
        font-size: 75%;
        font-weight: 600;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.35rem;
        margin-bottom: 0.5rem;
    }

    .badge-high {
        background-color: #FEE2E2 !important;
        color: #991B1B !important;
    }

    .badge-medium {
        background-color: #FEF3C7 !important;
        color: #92400E !important;
    }

    .badge-low {
        background-color: #F1F5F9 !important;
        color: #334155 !important;
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0;
        margin-bottom: 0.5rem;
    }

    .card-body {
        font-size: 0.95rem;
        color: #334155;
    }

    .card-section-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748B;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem;
    }
    
    /* Code highlighting overrides for custom theme */
    div[data-testid="stMarkdownContainer"] pre {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }
    
    /* Toast / alert text color override */
    div.stAlert p {
        color: inherit !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Helpers
def get_language_from_filename(filename):
    if not filename:
        return "python"
    ext = filename.split('.')[-1].lower()
    mapping = {
        'py': 'python',
        'js': 'javascript',
        'jsx': 'javascript',
        'ts': 'typescript',
        'tsx': 'typescript',
        'java': 'java',
        'cpp': 'cpp',
        'cc': 'cpp',
        'c': 'c',
        'h': 'cpp',
        'cs': 'csharp',
        'go': 'go',
        'rs': 'rust',
        'php': 'php',
        'rb': 'ruby',
        'html': 'html',
        'css': 'css',
        'sql': 'sql',
        'sh': 'bash',
        'json': 'json',
        'yaml': 'yaml',
        'yml': 'yaml'
    }
    return mapping.get(ext, 'python')

def parse_json_response(text):
    """Robust parser to extract JSON from LLM response."""
    # Try standard json loads
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try pattern matching markdown json blocks
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
            
    # Try stripping out potential prefix/suffix text
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except json.JSONDecodeError:
            pass
            
    raise ValueError("The AI model's response could not be parsed as valid structured JSON. Try running the analysis again.")

# System Prompt construction
SYSTEM_PROMPT = """You are an expert software engineer and code reviewer. Analyze the given code carefully. Identify bugs, explain the logic, and provide an optimized version.

You must respond with a JSON object containing the following keys exactly:
{
  "explanation": "A detailed, step-by-step explanation of what the code does, its purpose, and its working in simple, clear language.",
  "bugs": [
    {
      "description": "Description of the bug, logic error, performance issue, security flaw, or bad practice.",
      "severity": "High" | "Medium" | "Low",
      "impact": "The impact this bug has on execution, resource usage, or security.",
      "solution": "Clear instruction or code snippet showing how to resolve this bug."
    }
  ],
  "improvements": [
    "A specific improvement suggestion (e.g. style improvements, optimization, modern syntax usages)."
  ],
  "optimized_code": "The complete improved and optimized version of the code. Maintain the exact same programming language and do not truncate the code. Add helpful comments explaining changes."
}

Special Instructions:
1. If the code is correct, secure, and has no bugs, leave the "bugs" list empty (i.e., []).
2. If the user input is NOT valid programming code (e.g., gibberish, chat conversations, plain text unrelated to code, or empty input), return a JSON object with a single key "error": "Descriptive message explaining that the input is not recognizable code." and omit all other keys.
3. Keep the feedback professional, precise, and highly constructive.
"""

def analyze_code(code_content, provider, model_name, api_key, temperature, custom_instructions, filename=None):
    """Call LLM APIs and retrieve structured code review report."""
    language = get_language_from_filename(filename) if filename else "Code Block"
    
    # Prompt construction
    user_prompt = f"Please review the following code:\n\n"
    if filename:
        user_prompt += f"Filename: {filename}\n"
    user_prompt += f"Language Context: {language}\n\n"
    user_prompt += f"```\n{code_content}\n```\n"
    
    if custom_instructions:
        user_prompt += f"\nCustom Review Requirements:\n{custom_instructions}\n"

    if provider == "Gemini":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_PROMPT
        )
        response = model.generate_content(
            user_prompt,
            generation_config={
                "temperature": temperature,
                "response_mime_type": "application/json"
            }
        )
        return parse_json_response(response.text)
    
    elif provider == "OpenAI":
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        return parse_json_response(response.choices[0].message.content)
    
    else:
        raise ValueError("Invalid Provider Selected")

# Sidebar Implementation
st.sidebar.title("🧠 AI Code Reviewer")
st.sidebar.markdown("Configure your AI model settings below.")

# Provider selection
provider_option = st.sidebar.selectbox("API Provider", ["Gemini", "OpenAI"], index=0)

# API Keys and Model selection
if provider_option == "Gemini":
    gemini_env_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.sidebar.text_input(
        "Gemini API Key",
        value=gemini_env_key,
        type="password",
        placeholder="AIzaSy...",
        help="Obtained from Google AI Studio. Pre-filled from .env if present."
    )
    model_option = st.sidebar.selectbox(
        "Gemini Model",
        ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-3.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        help="gemini-2.5-flash is the modern, stable model recommended for your API key."
    )
else:
    openai_env_key = os.getenv("OPENAI_API_KEY", "")
    api_key_input = st.sidebar.text_input(
        "OpenAI API Key",
        value=openai_env_key,
        type="password",
        placeholder="sk-...",
        help="Obtained from OpenAI developer dashboard. Pre-filled from .env if present."
    )
    model_option = st.sidebar.selectbox(
        "OpenAI Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
        index=0,
        help="gpt-4o-mini is ultra-fast; gpt-4o is state-of-the-art."
    )

# Generation parameters
temperature_input = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1, help="Lower temperatures yield more precise, deterministic code reviews.")

st.sidebar.subheader("🎯 Customization")
custom_instructions_input = st.sidebar.text_area(
    "Review focus",
    value="",
    placeholder="e.g. Enforce memory efficiency, verify type safety, check for SQL injection...",
    help="Add specific rules or focus areas you want the AI reviewer to pay extra attention to."
)

st.sidebar.markdown("---")
st.sidebar.caption("AI Code Reviewer v1.0.0 | Developer Portfolio Tool")

# Main Application Layout
st.title("🛡️ AI Code Reviewer")
st.markdown("Automate code quality, find hidden bugs, and optimize performance in real time.")

col_left, col_right = st.columns([2, 3])

uploaded_file_name = None
code_input = ""

with col_left:
    st.subheader("📥 Input Code")
    
    # Selection of input method
    input_method = st.radio("Choose input method:", ["Paste Code", "Upload File"], horizontal=True)
    
    if input_method == "Paste Code":
        pasted_lang = st.selectbox(
            "Language of pasted code:",
            ["python", "javascript", "typescript", "cpp", "java", "go", "rust", "csharp", "html", "css", "sql", "bash", "json"]
        )
        code_input = st.text_area(
            "Code Editor Style Input",
            height=400,
            placeholder="# Paste your code here...\ndef bubble_sort(arr):\n    pass",
            label_visibility="collapsed"
        )
        uploaded_file_name = f"snippet.{pasted_lang}"
    else:
        uploaded_file = st.file_uploader(
            "Drop your code file here",
            type=["py", "js", "jsx", "ts", "tsx", "java", "cpp", "c", "h", "cs", "go", "rs", "php", "rb", "html", "css", "sql", "sh", "json", "yaml"],
            help="Supported: Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, Ruby, HTML/CSS, SQL, Shell, JSON, YAML"
        )
        if uploaded_file is not None:
            uploaded_file_name = uploaded_file.name
            try:
                # Read content
                code_input = uploaded_file.read().decode("utf-8")
                # Visual feedback
                st.info(f"Loaded: `{uploaded_file_name}` ({len(code_input)} chars)")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                code_input = ""

    # Button
    analyze_btn = st.button("🚀 Analyze Code")

with col_right:
    st.subheader("📊 Review Report")
    
    if analyze_btn:
        # 1. Input validation
        if not code_input.strip():
            st.warning("⚠️ Code input is empty. Please paste some code or upload a file first.")
        elif not api_key_input:
            st.error("🔑 API Key is missing. Please provide a valid API Key in the sidebar, or configure it in your `.env` file.")
        else:
            with st.spinner("Analyzing code quality and logic..."):
                try:
                    # Run analysis
                    report = analyze_code(
                        code_content=code_input,
                        provider=provider_option,
                        model_name=model_option,
                        api_key=api_key_input,
                        temperature=temperature_input,
                        custom_instructions=custom_instructions_input,
                        filename=uploaded_file_name
                    )
                    
                    # Store report in session state to persist it across rerun UI components
                    st.session_state["report"] = report
                    st.session_state["analyzed_lang"] = get_language_from_filename(uploaded_file_name)
                    st.success("Analysis Completed Successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Note: Double-check your API provider selection, API key validity, and network connection.")
                    
    # Render report if present in session state
    if "report" in st.session_state:
        report = st.session_state["report"]
        lang = st.session_state["analyzed_lang"]
        
        # Check if AI identified input as invalid/gibberish
        if "error" in report and report["error"]:
            st.error(f"⚠️ Validation Error: {report['error']}")
        else:
            # Render Tabs
            tab_explanation, tab_bugs, tab_suggestions, tab_optimized = st.tabs([
                "📖 Explanation", 
                "🐛 Bug Report", 
                "💡 Suggestions", 
                "✨ Optimized Code"
            ])
            
            with tab_explanation:
                st.markdown("### Code Working & Purpose")
                explanation_content = report.get("explanation", "No explanation provided.")
                st.markdown(explanation_content)
                
            with tab_bugs:
                st.markdown("### Detected Issues & Fixes")
                bugs_list = report.get("bugs", [])
                
                if not bugs_list:
                    st.markdown(
                        """
                        <div class="card" style="border-left: 4px solid #10B981 !important; background-color: #ECFDF5 !important;">
                            <p style="color: #065F46 !important; font-weight: 600; font-size: 1.1rem; margin: 0;">🎉 No bugs found!</p>
                            <p style="color: #047857 !important; margin: 0.5rem 0 0 0;">The AI reviewer did not identify any obvious logical issues, syntax errors, or vulnerabilities. Good job!</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    for i, bug in enumerate(bugs_list):
                        sev = bug.get("severity", "Low").strip().capitalize()
                        sev_class = "bug-card-low"
                        badge_class = "badge-low"
                        
                        if sev == "High" or sev == "Critical":
                            sev_class = "bug-card-high"
                            badge_class = "badge-high"
                        elif sev == "Medium":
                            sev_class = "bug-card-medium"
                            badge_class = "badge-medium"
                            
                        st.markdown(
                            f"""
                            <div class="card {sev_class}">
                                <span class="badge {badge_class}">{sev} Severity</span>
                                <div class="card-title">Bug #{i+1}: {bug.get('description', 'Code Bug')}</div>
                                <div class="card-section-title">Impact</div>
                                <div class="card-body">{bug.get('impact', 'N/A')}</div>
                                <div class="card-section-title">Solution</div>
                                <div class="card-body">{bug.get('solution', 'N/A')}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
            with tab_suggestions:
                st.markdown("### Actionable Improvements")
                improvements = report.get("improvements", [])
                if not improvements:
                    st.info("No style or structural suggestions found. Code is clean and matches best practices!")
                else:
                    for item in improvements:
                        st.markdown(f"- {item}")
                        
            with tab_optimized:
                st.markdown("### Refactored & Optimized Code")
                optimized = report.get("optimized_code", "")
                if not optimized:
                    st.warning("No optimized code was generated by the model.")
                else:
                    st.code(optimized, language=lang)
                    st.caption("Copy this optimized block and replace your original implementation.")
    else:
        st.markdown(
            """
            <div style="border: 1px solid #E2E8F0; border-radius: 8px; padding: 3rem; text-align: center; color: #64748B;">
                <h4 style="margin: 0; color: #64748B !important;">No Analysis Performed</h4>
                <p style="margin: 1rem 0 0 0; color: #94A3B8 !important;">Input your code on the left pane and click "Analyze Code" to generate your detailed review report.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
