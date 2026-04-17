import streamlit as st
import google.generativeai as genai
from datetime import datetime

# -------------------------
# CONFIGURE GEMINI
# -------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="ProposalPal v5",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 ProposalPal - Gemini Powered")

# -------------------------
# HELPERS
# -------------------------
def trim(text, max_chars=4000):
    return text[:max_chars] if text else ""

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
# GENERATION
# -------------------------
def generate_proposal(resume, job_desc, tone, budget):
    today = datetime.today().strftime("%B %d, %Y")

    prompt = f"""
You are ProposalPal, an expert freelance proposal writer.

TASK:
Write a HIGH-CONVERTING freelance proposal.

INPUTS:

Resume:
{trim(resume)}

Job Description:
{trim(job_desc)}

Budget:
{budget if budget else "Not specified"}

Tone:
{tone}

RULES:
- Do NOT repeat job description
- NO generic phrases like "I'm excited"
- First 2 lines must be a strong hook (insight-based)
- Be natural, human, persuasive
- Include 1 realistic past project example
- Focus on outcomes, not tasks

STRUCTURE:

1. Hook (2-3 lines max)

2. Short Introduction (1 line)

3. Understanding of Problem

4. Solution
- Objectives
- Plan
- Milestones (numbered)

5. Timeline
- Start from today: {today}
- Clear milestone dates

6. Pricing
- Align with budget if provided
- Otherwise realistic

7. Payment Schedule

8. Terms

9. Closing CTA (1 strong sentence)
"""

    response = model.generate_content(prompt)
    return response.text

# -------------------------
# BUTTON
# -------------------------
if st.button("🚀 Generate Proposal"):

    if not resume or not job_desc:
        st.warning("Please fill in both Resume and Job Description.")
    else:
        with st.spinner("Generating proposal..."):
            proposal = generate_proposal(resume, job_desc, tone, budget)

        st.markdown("## 📬 Your Proposal")
        st.markdown(proposal)

        st.download_button(
            label="📥 Download Proposal",
            data=proposal,
            file_name=f"proposal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
