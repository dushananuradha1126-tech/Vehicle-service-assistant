import html

import streamlit as st

from utils.groq_client import ask_groq


st.set_page_config(
    page_title="Vehicle Service Assistant",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.12), transparent 26%),
                linear-gradient(180deg, #f8fbff 0%, #eef4fb 58%, #f7fafc 100%);
        }

        .block-container {
            max-width: 1100px;
            padding-top: 1.8rem;
            padding-bottom: 2rem;
        }

        .hero {
            padding: 1.5rem 1.6rem;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
            backdrop-filter: blur(14px);
        }

        .eyebrow {
            display: inline-block;
            margin-bottom: 0.85rem;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(15, 118, 110, 0.10);
            color: #0f766e;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .hero h1 {
            margin: 0;
            font-size: clamp(2rem, 4vw, 3rem);
            line-height: 1.05;
            letter-spacing: -0.04em;
            color: #0f172a;
        }

        .hero p {
            margin: 0.85rem 0 0;
            max-width: 760px;
            color: #475569;
            font-size: 1.02rem;
            line-height: 1.65;
        }

        .steps {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin-top: 1rem;
        }

        .step-card {
            padding: 1rem 1rem 1.05rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(15, 23, 42, 0.08);
        }

        .step-card .num {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.8rem;
            height: 1.8rem;
            border-radius: 999px;
            background: linear-gradient(135deg, #2563eb, #0f766e);
            color: white;
            font-size: 0.9rem;
            font-weight: 700;
            margin-bottom: 0.65rem;
        }

        .step-card h3 {
            margin: 0 0 0.35rem;
            font-size: 1rem;
            color: #0f172a;
        }

        .step-card p {
            margin: 0;
            color: #64748b;
            font-size: 0.95rem;
            line-height: 1.55;
        }

        .section-label {
            margin: 1.35rem 0 0.6rem;
            color: #64748b;
            font-size: 0.84rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .example-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
        }

        .example-btn {
            width: 100%;
            padding: 0.95rem 1rem;
            border-radius: 16px;
            border: 1px solid rgba(37, 99, 235, 0.14);
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.08), rgba(15, 118, 110, 0.08));
            color: #0f172a;
            font-weight: 600;
            text-align: left;
        }

        .answer-box {
            margin-top: 1rem;
            padding: 1.1rem 1.15rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        }

        .answer-title {
            margin: 0 0 0.75rem;
            font-size: 0.95rem;
            font-weight: 700;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .answer-content {
            color: #0f172a;
            font-size: 1rem;
            line-height: 1.7;
            white-space: pre-wrap;
        }

        .answer-content p,
        .answer-content li,
        .answer-content strong,
        .answer-content em {
            color: #0f172a;
        }

        .hint {
            color: #64748b;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""


with st.sidebar:
    st.markdown("### How to use")
    st.write("1. Type your vehicle question.")
    st.write("2. Click **Get Answer**.")
    st.write("3. Read the practical steps below.")

    st.markdown("### Good questions")
    st.write("• What service do I need at 5000 km?")
    st.write("• Why is the check engine light on?")
    st.write("• When should I change engine oil?")

    st.markdown("### Tips")
    st.caption("Include the vehicle type, mileage, and any warning lights for better answers.")


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Vehicle service assistant</div>
        <h1>A simple way to get help with maintenance and repairs.</h1>
        <p>
            Ask one clear question about your car or motorcycle and get a direct answer.
            The page is kept simple so it is easy to understand and use.
        </p>
        <div class="steps">
            <div class="step-card">
                <div class="num">1</div>
                <h3>Write your question</h3>
                <p>Tell us the problem, mileage, or warning light you see.</p>
            </div>
            <div class="step-card">
                <div class="num">2</div>
                <h3>Choose an example</h3>
                <p>Use a sample prompt if you are not sure what to ask.</p>
            </div>
            <div class="step-card">
                <div class="num">3</div>
                <h3>Get a clear answer</h3>
                <p>Receive a practical response you can act on right away.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-label">Example questions</div>', unsafe_allow_html=True)

example_questions = [
    "My motorcycle has travelled 5000 km. What service should I do?",
    "Why is my check engine light on?",
    "How often should I change engine oil?",
]

cols = st.columns(3)
for col, sample in zip(cols, example_questions):
    if col.button(sample, use_container_width=True, key=f"sample_{sample}"):
        st.session_state.question = sample

st.markdown('<div class="section-label">Ask your question</div>', unsafe_allow_html=True)

with st.form("ask_form", clear_on_submit=False):
    question = st.text_area(
        "Type your question here",
        value=st.session_state.question,
        placeholder="Example: My car makes a noise when I brake. What should I check?",
        height=130,
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("Get Answer")

if submitted:
    if not question.strip():
        st.warning("Please type a question before clicking Get Answer.")
    else:
        st.session_state.question = question.strip()
        with st.spinner("Thinking..."):
            try:
                st.session_state.answer = ask_groq(question.strip())
            except Exception as exc:
                st.session_state.answer = f"Error: {exc}"


if st.session_state.answer:
    answer_text = html.escape(st.session_state.answer).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="answer-box">
            <div class="answer-title">Answer</div>
            <div class="answer-content">{answer_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("If you want a more accurate answer, add the vehicle model, mileage, and symptoms.")
else:
    st.info("Type a question or click one of the examples above to begin.")
