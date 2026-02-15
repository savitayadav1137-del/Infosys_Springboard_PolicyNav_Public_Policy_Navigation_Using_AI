import streamlit as st
import sqlite3
import jwt
import datetime
import re
import time
import hashlib
import os
from contextlib import contextmanager

# ================= CONFIG =================
SECRET_KEY = "super_secret_key_for_demo_2024_enhanced"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ================= DATABASE CONNECTION MANAGER =================
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect("users.db", timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def execute_query(query, params=(), fetch_one=False, fetch_all=False):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            if fetch_one:
                return cur.fetchone()
            elif fetch_all:
                return cur.fetchall()
            else:
                conn.commit()
                return True
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None if (fetch_one or fetch_all) else False

# ================= DATABASE INITIALIZATION =================
def init_database():
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    security_question TEXT NOT NULL,
                    security_answer TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    login_count INTEGER DEFAULT 0
                )
            """)
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        return False

# Initialize database
init_database()

# ================= DATABASE FUNCTIONS =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(username, email, password, question, answer):
    try:
        existing = execute_query(
            "SELECT email FROM users WHERE email = ?", 
            (email,), 
            fetch_one=True
        )
        
        if existing:
            return False, "Email already exists"
        
        success = execute_query(
            """INSERT INTO users 
               (username, email, password, security_question, security_answer) 
               VALUES (?, ?, ?, ?, ?)""",
            (username, email, hash_password(password), question, hash_password(answer))
        )
        
        if success:
            return True, "Success"
        else:
            return False, "Failed to create account"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def get_user(email):
    result = execute_query(
        "SELECT username, password, COALESCE(login_count, 0) FROM users WHERE email=?", 
        (email,), 
        fetch_one=True
    )
    return result

def update_login_stats(email):
    try:
        execute_query(
            """UPDATE users SET 
               last_login = CURRENT_TIMESTAMP, 
               login_count = COALESCE(login_count, 0) + 1 
               WHERE email=?""",
            (email,)
        )
        return True
    except:
        return False

def get_question(email):
    result = execute_query(
        "SELECT security_question FROM users WHERE email=?", 
        (email,), 
        fetch_one=True
    )
    return result[0] if result else None

def check_answer(email, ans):
    result = execute_query(
        "SELECT id FROM users WHERE email=? AND security_answer=?", 
        (email, hash_password(ans)), 
        fetch_one=True
    )
    return result is not None

def update_password(email, pwd):
    return execute_query(
        "UPDATE users SET password=? WHERE email=?", 
        (hash_password(pwd), email)
    )

# ================= JWT =================
def create_token(email, username):
    payload = {
        "sub": email,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None

# ================= SESSION =================
if "jwt" not in st.session_state:
    st.session_state.jwt = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "reset" not in st.session_state:
    st.session_state.reset = None
if "q" not in st.session_state:
    st.session_state.q = None
if "chat_input_key" not in st.session_state:
    st.session_state.chat_input_key = 0

# ================= UI CONFIG =================
st.set_page_config(
    page_title="PolicyNav Pro",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* ===== SIDEBAR STYLING ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a1f36 0%, #2d3748 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p {
        color: white !important;
    }
    
    /* Avatar container */
    .sidebar-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: 600;
        color: white;
        margin: 0 auto 1rem;
        border: 3px solid rgba(255,255,255,0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* ===== MAIN CONTENT STYLING ===== */
    /* Project Title - Enhanced */
    # .project-title {
    #     text-align: center;
    #     # color: white;
    #     font-size: 4rem;
    #     font-weight: 800;
    #     margin: 0.5rem 0 0.2rem 0;
    #     text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    #     letter-spacing: 3px;
    #     font-family: 'Poppins', sans-serif;
    #     background: linear-gradient(135deg, #fff 0%, #e0e0e0 100%);
    #     -webkit-background-clip: text;
    #     -webkit-text-fill-color: transparent;
    #     background-clip: text;
    # }
/* Project Title - Enhanced with vibrant gradient */
.project-title {
    text-align: center;
    color: black;
    font-size: 4rem;
    font-weight: 800;
    margin: 0.5rem 0 0.2rem 0;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    letter-spacing: 3px;
    font-family: 'Poppins', sans-serif;
    
    /* Vibrant Blue to Purple Gradient */
    background: linear-gradient(135deg, 
        #00C9FF 0%, 
        #4facfe 50%, 
        #00f2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    background-size: 200% 200%;
    animation: titleGradient 5s ease infinite;
}

@keyframes titleGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.project-subtitle {
        text-align: center;
        color: rgba(255,255,255,0.95);
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
        font-weight: 400;
        letter-spacing: 1px;
    }
            

    
    .project-tagline {
        text-align: center;
        color: rgba(255,255,255,0.8);
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Auth Container */
    .auth-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    /* Auth Headers */
    .auth-header {
        color: white !important;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .auth-subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        margin-bottom: 1.5rem;
        font-size: 1rem;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        color: #1f2937 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Selectbox */
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Secondary Button */
    .secondary-btn .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(5px);
    }
    
    /* Checkbox */
    .stCheckbox {
        margin: 1rem 0 !important;
        color: white !important;
    }
    
    .stCheckbox label {
        color: white !important;
    }
    
    /* Forgot password link */
    .forgot-link .stButton > button {
        background: transparent !important;
        color: white !important;
        border: none !important;
        padding: 0 !important;
        font-size: 0.9rem !important;
        text-decoration: underline;
        box-shadow: none !important;
    }
    
    .forgot-link .stButton > button:hover {
        color: rgba(255,255,255,0.8) !important;
        transform: none !important;
    }
    
    /* Dashboard Welcome */
    .welcome-header {
        color: white !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
        padding: 0.8rem 2rem;
        border-radius: 50px;
        display: inline-block;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .welcome-subheader {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 400 !important;
        margin-bottom: 2rem !important;
        text-shadow: 0 1px 5px rgba(0,0,0,0.2);
        background: rgba(0,0,0,0.2);
        padding: 0.5rem 2rem;
        border-radius: 40px;
        display: inline-block;
    }
    
    /* Chat Styles */
    .user-msg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 4px 20px;
        margin: 10px 0;
        max-width: 70%;
        margin-left: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        display: inline-block;
        float: right;
        clear: both;
    }
    
    .bot-msg {
        background: rgba(255, 255, 255, 0.95);
        color: #1a1f36;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 4px;
        margin: 10px 0;
        max-width: 70%;
        margin-right: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        display: inline-block;
        float: left;
        clear: both;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .chat-container {
        width: 100%;
        min-height: 350px;
        margin: 20px 0;
        overflow-y: auto;
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .chat-container:after {
        content: "";
        display: table;
        clear: both;
    }
    
    /* Quick action buttons */
    .quick-action-btn .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 25px !important;
        padding: 8px 16px !important;
        font-size: 0.9rem !important;
        backdrop-filter: blur(5px);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.9);
        padding: 2rem 0 1rem 0;
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= SIGNUP =================
def signup():
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        st.markdown("<h1 class='project-title'>PolicyNav Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p class='project-subtitle'>Create Your Account</p>", unsafe_allow_html=True)
        
        
        
        username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
        email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
        
        col_a, col_b = st.columns(2)
        with col_a:
            password = st.text_input("Password", type="password", placeholder="Create password", key="signup_pass")
        with col_b:
            confirm_password = st.text_input("Confirm", type="password", placeholder="Confirm password", key="signup_confirm")
        
        security_question = st.selectbox("Security Question", [
            "What is your pet's name?",
            "What is your mother's maiden name?",
            "What was your first car?",
            "What city were you born in?"
        ])
        
        security_answer = st.text_input("Security Answer", placeholder="Your answer", key="signup_answer")
        
        terms = st.checkbox("I agree to the Terms of Service")

        if st.button("Create Account", key="signup_btn"):
            if not username or not email or not password or not confirm_password or not security_answer:
                st.error("❌ All fields are required!")
            elif not re.match(r"[^@]+@[^@]+\.[a-zA-Z]{2,}", email):
                st.error("❌ Please enter a valid email address!")
            elif len(password) < 8:
                st.error("❌ Password must be at least 8 characters long!")
            elif password != confirm_password:
                st.error("❌ Passwords do not match!")
            elif not terms:
                st.error("❌ Please accept the terms!")
            else:
                with st.spinner("Creating account..."):
                    success, message = save_user(username, email, password, security_question, security_answer)
                    if success:
                        st.session_state.jwt = create_token(email, username)
                        update_login_stats(email)
                        st.success("✅ Account created successfully!")
                        st.balloons()
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("← Back to Login", key="back_to_login"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ================= LOGIN =================
def login():
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        # Enhanced Project Title
        st.markdown("<h1 class='project-title' >PolicyNav Login</h1>", unsafe_allow_html=True)
        st.markdown("<p class='auth-subtitle'>Sign in to continue your journey</p>", unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="Enter your email", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        col_rem, col_forgot = st.columns(2)
        with col_rem:
            remember = st.checkbox("Remember me")
        with col_forgot:
            st.markdown('<div class="forgot-link">', unsafe_allow_html=True)
            if st.button("Forgot Password?", key="forgot_link"):
                st.session_state.page = "forgot"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Sign In", key="login_btn"):
            if not email or not password:
                st.error("❌ Please enter both email and password!")
            else:
                with st.spinner("Verifying..."):
                    user = get_user(email)
                    if user and user[1] == hash_password(password):
                        st.session_state.jwt = create_token(email, user[0])
                        update_login_stats(email)
                        st.success("✅ Login successful!")
                        st.balloons()
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password!")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white; font-size: 1rem;'>Don't have an account</p>", unsafe_allow_html=True)
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("Create New Account", key="create_btn"):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ================= FORGOT PASSWORD =================
def forgot():
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        st.markdown("<h1 class='project-title'>PolicyNav Pro</h1>", unsafe_allow_html=True)
        
        
        st.markdown("<h2 class='auth-header'>Reset Password</h2>", unsafe_allow_html=True)
        st.markdown("<p class='auth-subtitle'>Recover your account</p>", unsafe_allow_html=True)

        if "q" not in st.session_state or not st.session_state.q:
            email = st.text_input("Registered Email", placeholder="Enter your email", key="reset_email")
            
            if st.button("Verify Email", key="get_question"):
                if not email:
                    st.error("❌ Please enter your email!")
                else:
                    with st.spinner("Searching..."):
                        question = get_question(email)
                        if question:
                            st.session_state.reset = email
                            st.session_state.q = question
                            st.success("✅ Email verified! Answer security question.")
                            st.rerun()
                        else:
                            st.error("❌ Email not found!")

        if "q" in st.session_state and st.session_state.q:
            st.info(f"**Security Question:** {st.session_state.q}")
            
            answer = st.text_input("Your Answer", placeholder="Enter your answer", key="security_answer")
            new_password = st.text_input("New Password", type="password", placeholder="Enter new password", key="new_password")
            confirm_new = st.text_input("Confirm Password", type="password", placeholder="Confirm password", key="confirm_password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Reset Password", key="reset_btn"):
                    if not answer or not new_password:
                        st.error("❌ Please fill all fields!")
                    elif len(new_password) < 8:
                        st.error("❌ Password must be at least 8 characters!")
                    elif new_password != confirm_new:
                        st.error("❌ Passwords don't match!")
                    else:
                        with st.spinner("Updating..."):
                            if check_answer(st.session_state.reset, answer):
                                update_password(st.session_state.reset, new_password)
                                st.success("✅ Password updated!")
                                st.balloons()
                                st.session_state.q = None
                                st.session_state.reset = None
                                time.sleep(1.5)
                                st.session_state.page = "login"
                                st.rerun()
                            else:
                                st.error("❌ Incorrect answer!")
            
            with col_b:
                if st.button("← Back", key="back_btn"):
                    st.session_state.q = None
                    st.session_state.reset = None
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ================= DASHBOARD =================
def dashboard():
    data = verify_token(st.session_state.jwt)
    if not data:
        st.session_state.jwt = None
        st.session_state.page = "login"
        st.rerun()
        return
    
    username = data.get("username", "User")
    email = data.get("sub", "")
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem 0;'>
            <div class="sidebar-avatar">
                {username[0].upper()}
            </div>
            <div style='color: white; font-size: 1.3rem; font-weight: 600;'>{username}</div>
            <div style='color: rgba(255,255,255,0.7); font-size: 0.85rem; word-break: break-all;'>{email}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("➕ New Chat", use_container_width=True):
            if 'chat_history' in st.session_state:
                st.session_state.chat_history = [{
                    'type': 'bot',
                    'message': 'Hello! I am PolicyNav Pro. How can I help you with policies today?'
                }]
            st.rerun()
        
        st.markdown("---")
        st.markdown('<p style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Recent Chats</p>', unsafe_allow_html=True)
        
        history_items = [
            "Healthcare policy analysis",
            "Insurance claim process", 
            "Tax regulation 2024",
            "Compliance checklist"
        ]
        
        for item in history_items:
            st.markdown(f'<div style="color: rgba(255,255,255,0.8); padding: 8px 12px; border-radius: 6px; cursor: pointer;">📄 {item}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.jwt = None
            st.session_state.page = "login"
            st.rerun()

    # Main Content
    st.markdown(f"<h1 class='welcome-header'>Welcome back, {username}! 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-subheader'>How can I assist you with policies today?</p>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2); margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # Chat container
    # st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{
            'type': 'bot',
            'message': 'Hello! I am PolicyNav Pro. Ask me anything about policies, regulations, or compliance!'
        }]
    
    for msg in st.session_state.chat_history:
        if msg['type'] == 'user':
            st.markdown(f'<div class="user-msg">{msg["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg">{msg["message"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # User input
    st.markdown('<div style="margin: 20px 0;">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        input_key = f"chat_input_{st.session_state.chat_input_key}"
        user_input = st.text_input(
            "Message",
            placeholder="Ask about policies, regulations, or compliance...",
            label_visibility="collapsed",
            key=input_key
        )
    
    with col2:
        send_button = st.button("📤 Send", use_container_width=True)
    
    if send_button and user_input:
        st.session_state.chat_history.append({
            'type': 'user',
            'message': user_input
        })
        
        # Simulated response
        response = f"I understand you're asking about: '{user_input}'. As PolicyNav Pro, I can help you navigate through complex policies and regulations. Please provide more details so I can assist you better."
        
        st.session_state.chat_history.append({
            'type': 'bot',
            'message': response
        })
        
        st.session_state.chat_input_key += 1
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Policy Analysis", use_container_width=True):
            st.session_state.chat_history.append({
                'type': 'user',
                'message': "Can you help me analyze this policy?"
            })
            st.rerun()
    
    with col2:
        if st.button("⚖️ Compliance Check", use_container_width=True):
            st.session_state.chat_history.append({
                'type': 'user',
                'message': "Check compliance for my business"
            })
            st.rerun()
    
    with col3:
        if st.button("📝 Document Review", use_container_width=True):
            st.session_state.chat_history.append({
                'type': 'user',
                'message': "Review this policy document"
            })
            st.rerun()
    
    with col4:
        if st.button("🔍 Regulation Search", use_container_width=True):
            st.session_state.chat_history.append({
                'type': 'user',
                'message': "Find regulations for my industry"
            })
            st.rerun()

# ================= FOOTER =================
def footer():
    st.markdown("""
    <div class="footer">
        <p>© 2024 PolicyNav Pro - Your Intelligent Policy Navigation Platform</p>
    </div>
    """, unsafe_allow_html=True)

# ================= MAIN =================
try:
    if st.session_state.jwt:
        dashboard()
    else:
        if st.session_state.page == "signup":
            signup()
        elif st.session_state.page == "forgot":
            forgot()
        else:
            login()
    
    footer()
    
except Exception as e:
    st.error(f"Error: {str(e)}")