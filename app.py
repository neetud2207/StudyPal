import streamlit as st
import google.generativeai as genai
import time
from PIL import Image


logo = Image.open("/content/StudyPal.png")


# ======================================================
# Gemini Configuration
# ======================================================

genai.configure(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

model = genai.GenerativeModel(
    "models/gemini-flash-latest"
)

# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="StudyPal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# Session State
# ======================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "responses" not in st.session_state:
    st.session_state.responses = 0

if "last_topic" not in st.session_state:
    st.session_state.last_topic = "None"

# ======================================================
# Custom CSS
# ======================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* -------------------- */
/* Global */
/* -------------------- */

html, body, [class*="css"], .stMarkdown, .stTextInput, .stSelectbox {
    font-family:'Poppins', sans-serif !important;
}

.stApp{
    background:
    radial-gradient(
        circle at top left,
        #EEF2FF,
        transparent 35%
    ),
    linear-gradient(
        180deg,
        #F8FAFC,
        #F5F3FF
    );
}

/* -------------------- */
/* Sidebar */
/* -------------------- */

section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

section[data-testid="stSidebar"] *{
    color:#1E293B !important;
}

/* Reduce Streamlit default spacing */

.block-container{
    padding-top:2rem !important;
    padding-bottom:1rem !important;
    max-width:1150px !important;
}


/* Remove huge gaps */

div[data-testid="stVerticalBlock"]{
    gap:0.35rem;
}


/* Compact headings */

h1,h2,h3{

    letter-spacing:-1px;
    color:#0F172A;

}


/* Card styling */

div[data-testid="stExpander"],
div[data-testid="stVerticalBlockBorderWrapper"]{

background:rgba(255,255,255,0.85);

backdrop-filter:blur(12px);

border-radius:20px;

border:1px solid #E0E7FF;

box-shadow:
0 12px 35px rgba(99,102,241,0.10);

padding:12px;

}

/* -------------------- */
/* Inputs */
/* -------------------- */

.stTextInput input,
.stTextArea textarea{

    background:white !important;

    border:2px solid #E2E8F0 !important;

    border-radius:15px !important;

    color:#1E293B !important;

    font-size:16px;

}

.stTextInput input:focus,
.stTextArea textarea:focus{

    border:2px solid #6366F1 !important;

    box-shadow:0 0 12px rgba(99,102,241,.25);

}

/* -------------------- */
/* Select Box */
/* -------------------- */

.stSelectbox div[data-baseweb="select"]{

    border-radius:15px !important;

}

/* -------------------- */
/* Buttons */
/* -------------------- */

.stButton>button{

    width:100%;

    height:58px;

    border:none;

    border-radius:16px;

    background:
    linear-gradient(
    90deg,
    #6366F1,
    #8B5CF6
    );

    color:white;

    font-size:18px;

    font-weight:700;

    transition:0.3s;

    box-shadow:0 8px 25px rgba(79,70,229,.30);

}

.stButton>button:hover{

    transform:translateY(-3px);

    box-shadow:0 12px 30px rgba(79,70,229,.40);

}

/* -------------------- */
/* Download Button */
/* -------------------- */

.stDownloadButton>button{

    width:100%;

    border-radius:16px;

}

/* -------------------- */
/* Metrics */
/* -------------------- */

div[data-testid="metric-container"]{

background:
linear-gradient(
135deg,
#FFFFFF,
#EEF2FF
);

border-radius:18px;

padding:15px;

border:1px solid #E0E7FF;

box-shadow:
0 8px 25px rgba(99,102,241,.12);

}

/* -------------------- */
/* Alerts */
/* -------------------- */

div[data-testid="stAlert"]{

    border-radius:16px;

}

/* -------------------- */
/* Containers */
/* -------------------- */

div[data-testid="stVerticalBlock"]>div:has(div.stTextInput){

    border-radius:18px;

}

/* -------------------- */
/* Scrollbar */
/* -------------------- */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#6366F1;

    border-radius:20px;

}

::-webkit-scrollbar-track{

    background:#EEF2FF;

}


/* -------------------- */
/* Glass Workspace */
/* -------------------- */



/* -------------------- */
/* Premium Sidebar */
/* -------------------- */

section[data-testid="stSidebar"]{

background:
linear-gradient(
180deg,
#FFFFFF,
#EEF2FF
);

}


section[data-testid="stSidebar"] h3{

color:#4F46E5 !important;

}

div[data-testid="metric-container"] p{
    font-size:13px !important;
}


div[data-testid="metric-container"] div{
    font-size:28px !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]{
    background:white;
    border-radius:22px !important;
    border:1px solid #E5E7EB !important;
    box-shadow:0 10px 30px rgba(99,102,241,.12);
    padding:20px;
}
/* Learning Workspace */

div[data-testid="stVerticalBlockBorderWrapper"]{
    background:rgba(255,255,255,.82);
    backdrop-filter:blur(14px);
    border-radius:24px;
    border:1px solid #E5E7EB;
    box-shadow:0 12px 35px rgba(79,70,229,.10);
    padding:20px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# Sidebar
# ======================================================

with st.sidebar:

    # --------------------------
    # Logo + Branding
    # --------------------------

    col1, col2 = st.columns([1, 3], vertical_alignment="center")

    with col1:
        st.image(logo, width=45)

    with col2:
        st.markdown("""
        <h2 style="
        margin:0;
        color:#4F46E5;
        font-weight:800;
        ">
        StudyPal
        </h2>

        <p style="
        margin:0;
        color:#64748B;
        font-size:14px;
        ">
        AI Learning Platform
        </p>
        """, unsafe_allow_html=True)


    st.markdown("---")


    # --------------------------
    # Dashboard
    # --------------------------

    st.markdown("### 📊 Dashboard")


    c1, c2 = st.columns(2)


    with c1:
        st.metric(
            "Topics",
            len(st.session_state.history)
        )


    with c2:
        st.metric(
            "Responses",
            st.session_state.responses
        )


    st.info(
        f"📌 Last Topic\n\n**{st.session_state.last_topic}**"
    )


    st.markdown("---")


    # --------------------------
    # Recent Topics
    # --------------------------

    st.markdown("### 🕒 Recent Topics")


    if st.session_state.history:

        for topic in st.session_state.history:

            st.markdown(
                f"""
                <div style="
                padding:10px;
                border:1px solid #E2E8F0;
                border-radius:12px;
                margin-bottom:8px;
                background:#FFFFFF;
                font-size:14px;
                ">
                📚 {topic}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.caption("No recent topics")


    st.markdown("---")


    # --------------------------
    # Clear History
    # --------------------------

    if st.button(
        "🗑️ Clear History",
        use_container_width=True,
        key="clear_history_btn"
    ):

        st.session_state.history = []
        st.session_state.responses = 0
        st.session_state.last_topic = "None"

        st.rerun()



# --------------------------
# Header
# --------------------------



# --------------------------
# Header
# --------------------------

# --------------------------
# Header
# --------------------------

col1, col2 = st.columns([1,5], vertical_alignment="center")

with col1:
    st.image(logo, width=85)

with col2:
    st.markdown("""
    <h1 style="
    margin:0;
    color:#4F46E5;
    font-size:52px;
    font-weight:800;
    ">
    StudyPal
    </h1>

    <p style="
    margin:4px 0 0 0;
    color:#64748B;
    font-size:18px;
    ">
    Your AI Learning Companion
    </p>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="
background:linear-gradient(135deg,#7C3AED,#4F46E5);
padding:18px 28px;
border-radius:22px;
color:white;
margin-top:10px;
margin-bottom:22px;
box-shadow:0 10px 30px rgba(79,70,229,.25);
">

<div style="
display:inline-block;
padding:6px 14px;
border-radius:20px;
background:rgba(255,255,255,.15);
font-size:13px;
font-weight:600;
margin-bottom:14px;
">
✨ Powered by Gemini AI
</div>

<h2 style="
margin:0;
font-size:34px;
font-weight:800;
color:white;
">
Learn Smarter with StudyPal 🚀
</h2>

<p style="
margin-top:12px;
font-size:18px;
line-height:1.7;
color:#F3F4F6;
">
Generate explanations, quizzes, study notes, interview questions and
AI-powered answer evaluation—all in one place.
</p>

</div>
""", unsafe_allow_html=True)

# ======================================================
# Learning Workspace
# ======================================================

st.markdown("""
<h2 style="
color:#1E293B;
margin-bottom:5px;
">
📚 Learning Workspace
</h2>

<p style="
color:#64748B;
margin-top:0;
">
Choose a topic and let StudyPal generate personalized learning content.
</p>
""", unsafe_allow_html=True)





with st.container():

   
    topic = st.text_input(
        "📖 Topic",
        placeholder="Example: Python, DBMS, Machine Learning"
    )

    col1, col2 = st.columns(2)

    with col1:

        difficulty = st.selectbox(
            "📈 Difficulty",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

    with col2:

     option = st.selectbox(
        "🎯 Activity",
        [
            "Explain Concept",
            "Real-Life Example",
            "Generate Quiz",
            "Generate Study Notes",
            "Interview Questions",
            "Generate Study Plan",
            "Evaluate My Answer"
        ]
    )

if option == "Generate Study Plan":

    days = st.slider(
        "📅 Days until Exam",
        min_value=1,
        max_value=30,
        value=7
    )

elif option == "Evaluate My Answer":

    question = st.text_input("❓ Question")

    user_answer = st.text_area(
        "✍️ Your Answer",
        height=180
    )
# ======================================================
# Generate Button
# ======================================================



generate = st.button(
    "✨ Generate Learning Content",
    use_container_width=True
)
st.markdown("</div>", unsafe_allow_html=True)
# ======================================================
# AI Generation
# ======================================================

if generate:

    if topic.strip() == "":

        st.warning("Please enter a topic.")

    else:

        if option == "Explain Concept":

            prompt = f"""
Explain {topic} for a {difficulty} learner.

Include:

- Definition
- Simple Explanation
- Advantages
- Applications
- Summary

Use headings and bullet points.
"""

        elif option == "Real-Life Example":

            prompt = f"""
Give 3 simple real-life examples of {topic}.

Explain each example in an easy way.
"""

        elif option == "Generate Quiz":

            prompt = f"""
Create 5 multiple choice questions on {topic}.

For every question provide:

Question

A)

B)

C)

D)

Correct Answer
"""

        elif option == "Generate Study Notes":

            prompt = f"""
Generate professional study notes on {topic}.

Include:

Definition

Key Concepts

Advantages

Applications

Important Points

Summary

Use bullet points.
"""

        elif option == "Interview Questions":

            prompt = f"""
Generate 10 interview questions on {topic}.

Provide detailed answers for every question.
"""
        elif option == "Generate Study Plan":

         prompt = f"""
You are an expert study coach.

Create a {days}-day study plan for learning {topic}.

For each day include:

📚 Topics to study

📝 Practice tasks

⏰ Estimated study time

🎯 Goal of the day

Keep it motivating and beginner friendly.

Use Markdown headings and bullet points.
"""

        elif option == "Evaluate My Answer":

            prompt = f"""
You are an experienced teacher.

Question:

{question}

Student Answer:

{user_answer}

Evaluate using:

Accuracy

Completeness

Concept Coverage

Depth

Give output exactly like this:

⭐ Score : __ /10

✅ Correct Points

❌ Missing Points

⚠ Mistakes

💡 Suggestions
"""

        start = time.time()

        progress = st.progress(0)

        for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

        response = model.generate_content(prompt)

        progress.empty()

          

        end = time.time()

        generation_time = round(end - start,2)

        # =====================================
        # Update Dashboard
        # =====================================

        if topic not in st.session_state.history:

            st.session_state.history.insert(0,topic)

        st.session_state.history = st.session_state.history[:5]

        st.session_state.responses += 1

        st.session_state.last_topic = topic

        # =====================================
        # Response
        # =====================================

        st.markdown("<br>", unsafe_allow_html=True)

        st.toast("✨ Content generated successfully!")

        st.success("Your personalized learning content is ready!")
        st.markdown("""
        <h2 style="
        color:#1E293B;
        font-size:32px;
        font-weight:700;
        margin-bottom:15px;
        ">
        🤖 AI Response
        </h2>
        """, unsafe_allow_html=True)

        with st.expander("📖 View AI Response", expanded=True):
         st.markdown(response.text)

        # =====================================
        # Analytics
        # =====================================

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <h2 style="
        color:#1E293B;
        ">
        📊 Response Analytics
        </h2>
        """, unsafe_allow_html=True)

        words = len(response.text.split())

        characters = len(response.text)

        c1,c2,c3 = st.columns(3)

        with c1:

            st.metric(
                "📝 Words",
                words
            )

        with c2:

            st.metric(
                "📄 Characters",
                characters
            )

        with c3:

            st.metric(
                "⚡ Time",
                f"{generation_time}s"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.download_button(

            "📥 Download Response",

            data=response.text,

            file_name="StudyPal_Response.txt",

            mime="text/plain",

            use_container_width=True

        )

# ======================================================
# Footer
# ======================================================

st.markdown("""
---
<div style="text-align:center;color:#64748B;font-size:15px;">

🎓 <b>StudyPal</b><br>

Built with ❤️ using <b>Streamlit</b> • <b>Google Gemini AI</b> • <b>Python</b>

<br>

© 2026 StudyPal | AI Learning Companion

</div>
""", unsafe_allow_html=True)
