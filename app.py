import html
import streamlit as st

from agents.orchestrator import process_vehicle_query
from utils.config import validate_config

st.set_page_config(
    page_title="Vehicle Service AI Assistant",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Modern Custom CSS Styling
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
            max-width: 1150px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .hero {
            padding: 1.6rem 1.8rem;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 20px 45px rgba(15, 23, 42, 0.06);
            backdrop-filter: blur(14px);
            margin-bottom: 1.2rem;
        }

        .eyebrow {
            display: inline-block;
            margin-bottom: 0.75rem;
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            background: rgba(37, 99, 235, 0.10);
            color: #2563eb;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .hero h1 {
            margin: 0;
            font-size: clamp(2rem, 3.5vw, 2.7rem);
            line-height: 1.1;
            letter-spacing: -0.03em;
            color: #0f172a;
        }

        .hero p {
            margin: 0.75rem 0 0;
            max-width: 780px;
            color: #475569;
            font-size: 1.02rem;
            line-height: 1.6;
        }

        .agent-badge {
            display: inline-block;
            padding: 0.3rem 0.75rem;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 700;
            background: #e0e7ff;
            color: #3730a3;
            margin-bottom: 0.8rem;
        }

        .source-card {
            padding: 0.85rem;
            border-radius: 12px;
            background: #f1f5f9;
            border-left: 4px solid #2563eb;
            margin-bottom: 0.6rem;
            font-size: 0.92rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session State Initialization
if "question" not in st.session_state:
    st.session_state.question = ""
if "query_result" not in st.session_state:
    st.session_state.query_result = None

# Sidebar Vehicle Configuration & Filters
with st.sidebar:
    st.image("https://img.icons8.com/color/96/car-service.png", width=70)
    st.title("Vehicle Specs")

    v_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "SUV / Truck", "EV / Hybrid"])
    v_make = st.text_input("Make / Brand", placeholder="e.g. Toyota, Honda, Yamaha")
    v_model = st.text_input("Model", placeholder="e.g. Corolla, Civic, MT-07")
    v_year = st.number_input("Year", min_value=1990, max_value=2027, value=2020)
    v_mileage = st.number_input("Current Odometer (km)", min_value=0, max_value=500000, value=35000, step=1000)



# Header Hero Section
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Multi-Agent RAG Assistant</div>
        <h1>Vehicle Service & Diagnostic System</h1>
        <p>
            Ask maintenance questions, report mechanical symptoms, or check scheduled service intervals. 
            Our intelligent multi-agent framework routes your query to domain-specific knowledge experts.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sample Prompts
st.markdown("##### 💡 Example Questions")
example_questions = [
    "My motorcycle engine makes a ticking noise on cold startup.",
    "My car has reached 40,000 km. What service items are due?",
    "How much does a full brake pad and rotor replacement cost?",
    "When should I replace engine oil and filter?",
]

cols = st.columns(4)
for col, sample in zip(cols, example_questions):
    if col.button(sample, use_container_width=True, key=f"btn_{sample[:10]}"):
        st.session_state.question = sample

# Main Input Form
with st.form("ask_form", clear_on_submit=False):
    user_query = st.text_area(
        "Type your vehicle question",
        value=st.session_state.question,
        placeholder="e.g. Why is the engine temperature rising during idle traffic?",
        height=100,
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Ask Assistant 🚀")

if submitted:
    if not user_query.strip():
        st.warning("Please enter a question before submitting.")
    else:
        st.session_state.question = user_query.strip()
        vehicle_spec = {
            "type": v_type,
            "make": v_make,
            "model": v_model,
            "year": v_year,
            "mileage": v_mileage
        }
        with st.spinner("Routing query through Multi-Agent pipeline..."):
            res = process_vehicle_query(user_query.strip(), vehicle_spec)
            st.session_state.query_result = res

# Display Multi-Tab Response Breakdown
if st.session_state.query_result:
    res = st.session_state.query_result

    st.markdown("---")
    badge_color = "#2563eb"
    st.markdown(
        f"""
        <div class="agent-badge">
            Routed to: <b>{res['agent_used']}</b> | Intent: <b>{res['intent_category']}</b> (Confidence: {res['confidence'] * 100:.0f}%)
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_answer, tab_sources, tab_trace = st.tabs(["💬 Response & Advice", "📚 Manual Sources", "🔍 Agent Workflow"])

    with tab_answer:
        st.markdown(res["primary_answer"])
        st.caption(f"Targeted for: {v_make or 'Vehicle'} {v_model} ({v_mileage:,} km)")

    with tab_sources:
        snippets = res.get("snippets", [])
        if snippets:
            st.write(f"Retrieved **{len(snippets)}** relevant context snippets from Chroma vector store:")
            for snip in snippets:
                st.markdown(
                    f"""
                    <div class="source-card">
                        <b>Source File:</b> {snip['source']} (Relevance Score: {snip['relevance_score']})<br>
                        <p style="margin-top:0.4rem; color:#334155;">{html.escape(snip['content'])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No specific manual snippets retrieved for this question.")

    with tab_trace:
        st.json({
            "User Query": res["query"],
            "Intent Classified": res["intent_category"],
            "Confidence": res["confidence"],
            "Agent Routing": res["agent_used"],
            "Vehicle Specs Passed": {
                "Make": v_make,
                "Model": v_model,
                "Year": v_year,
                "Mileage": v_mileage
            }
        })
