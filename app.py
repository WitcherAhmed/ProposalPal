import streamlit as st
from groq import Groq
from datetime import datetime

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Page config
st.set_page_config(
    page_title="ProposalPal v3",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 ProposalPal - Freelance Proposal Generator")

# -------------------------
# INPUTS
# -------------------------
resume = st.text_area("📄 Paste Your Resume", height=200)
job_desc = st.text_area("💼 Paste Job Description", height=200)

col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox(
        "Tone",
        ["Professional", "Friendly", "Confident", "Persuasive"]
    )

with col2:
    budget = st.text_input(
        "💰 Client Budget (optional)",
        placeholder="e.g. $200 - $500"
    )

# -------------------------
# FUNCTION: CALL GROQ
# -------------------------
def call_groq(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-versatile",  # powerful + free tier
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# -------------------------
# STEP 1: ANALYSIS
# -------------------------
def analyze_job(job_desc):
    analysis_prompt = f"""
Analyze this freelance job:

1. What the client REALLY wants
2. Hidden challenges
3. Key skills/tools
4. How to stand out

Job:
{job_desc}
"""
    return call_groq(analysis_prompt)

# -------------------------
# STEP 2: PROPOSAL
# -------------------------
def generate_proposal(resume, job_desc, analysis, tone, budget):
    today = datetime.today().strftime("%B %d, %Y")

    proposal_prompt = f"""
You are an elite freelance proposal writer.

Job Analysis:
{analysis}

Resume:
{resume}

Job:
{job_desc}

Budget:
{budget if budget else "Not specified"}

Tone: {tone}

RULES:
- No generic phrases
- No repeating job description
- Strong hook in first 2 lines
- Include 1 real or realistic project example
- Be natural and persuasive

Write a full structured proposal with:
- Hook
- Intro
- Problem understanding
- Solution
- Timeline (real dates)
- Pricing (aligned with budget)
- Payment schedule
- Terms
- Call to action
"""

    return call_groq(proposal_prompt)

# -------------------------
# BUTTON
# -------------------------
if st.button("🚀 Generate Proposal"):

    if not resume or not job_desc:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Analyzing job..."):
            analysis = analyze_job(job_desc)

        st.markdown("### 🧠 Job Insights")
        st.markdown(analysis)

        with st.spinner("Writing proposal..."):
            proposal = generate_proposal(resume, job_desc, analysis, tone, budget)

        st.markdown("## 📬 Proposal")
        st.markdown(proposal)

        st.download_button(
            label="📥 Download",
            data=proposal,
            file_name=f"proposal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
