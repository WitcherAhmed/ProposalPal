import streamlit as st
from langchain_ollama import OllamaLLM
from datetime import datetime

model = OllamaLLM(model="llama3")


st.set_page_config(
    page_title="ProposalPal v3",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 ProposalPal v3 - Smart Freelance Proposals")


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


def analyze_job(job_desc):
    analysis_prompt = f"""
You are an expert freelance strategist.

Analyze this job and extract:

1. What the client REALLY wants
2. Hidden challenges (technical + business)
3. Most critical tools/skills required
4. How a freelancer can stand out

Be concise, insightful, and practical.

Job Description:
{job_desc}
"""
    return model.invoke(analysis_prompt)


def generate_proposal(resume, job_desc, analysis, tone, budget):
    today = datetime.today().strftime("%B %d, %Y")

    proposal_prompt = f"""
You are ProposalPal, an elite freelance proposal writer.

Job Analysis:
{analysis}

Freelancer Resume:
{resume}

Job Description:
{job_desc}

Client Budget:
{budget if budget else "Not specified"}

TONE: {tone}

STRICT RULES:

- DO NOT repeat or rephrase the job description
- NEVER say "I analyzed the job description"
- Speak like a real freelancer, not AI
- Be direct, confident, and natural
- The first 2 lines MUST grab attention immediately
- Avoid phrases like "I'm excited" or "I believe"
- Show clear differentiation using skills/tools
- Focus on outcomes, not tasks

PRICING RULES:
- If budget exists → align within or slightly below it
- If no budget → estimate realistic mid-range pricing
- NEVER output unrealistic numbers

TIMELINE RULE:
- Must be continuous (no gaps)
- Start from today: {today}

STRUCTURE:

1. Catchy Headline (max 3 lines, strong hook)

2. Personal Introduction (1 line, human, credible)

3. Understanding the Problem
- Identify real challenges (NOT repeating job post)

4. Proposed Solution
- Objectives
- Clear execution plan
- Milestones with numbered tasks
- Measurable outcomes

5. Timeline
- Table format:
Milestone | Start Date | End Date

6. Pricing
- Cost per milestone
- Total cost
- Justify briefly

7. Payment Schedule
- Each payment within 1 week after milestone approval

8. Terms and Conditions
- Revisions
- Confidentiality
- Copyright
- Dispute handling
- Cancellation fee (30%)

ENDING:
- Strong, natural call to action (1 sentence max)

Make it sharp, persuasive, and client-focused.
"""

    return model.invoke(proposal_prompt)


if st.button("🚀 Generate Winning Proposal"):

    if not resume or not job_desc:
        st.warning("Please fill in both Resume and Job Description.")
    else:
        with st.spinner("🧠 Analyzing job..."):
            analysis = analyze_job(job_desc)

        st.markdown("### 🧠 Job Insight")
        st.markdown(analysis)

        with st.spinner("✍️ Writing proposal..."):
            proposal = generate_proposal(resume, job_desc, analysis, tone, budget)

        st.markdown("## 📬 Your Proposal")
        st.markdown(proposal)

        st.download_button(
            label="📥 Download Proposal",
            data=proposal,
            file_name=f"proposal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
