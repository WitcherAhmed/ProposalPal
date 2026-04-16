import streamlit as st
from groq import Groq
from datetime import datetime

# -------------------------
# GROQ CLIENT
# -------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="ProposalPal v4",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 ProposalPal v4 - Stable Freelance Proposal Generator")

# -------------------------
# HELPERS
# -------------------------
def trim(text, max_chars=2500):
    return text[:max_chars] if text else ""

def call_groq(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a world-class freelance proposal writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

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
# GENERATION PROMPT
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
- Focus on outcomes, not tasks

STRUCTURE:

1. Hook (2-3 lines max, must be strong insight)

2. Short Introduction (1 line, credible, human)

3. Understanding of Problem (real challenges, not repetition)

4. Solution
- Objectives
- Plan
- Milestones (numbered tasks)

5. Timeline
- Must start from today: {today}
- Show clear milestone dates

6. Pricing
- Align with budget if provided
- Otherwise realistic freelance pricing
- Break per milestone + total

7. Payment Schedule
- Tied to milestones

8. Terms
- revisions, confidentiality, copyright, cancellation

9. Closing CTA (1 strong sentence)
"""

    return call_groq(prompt)

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
