import streamlit as st
import pandas as pd
import numpy as np

# Optional: Uncomment if you want OpenAI lead summaries
# import openai

st.set_page_config(page_title="OperatorOS Pipeline Dashboard", layout="wide")

st.title("OperatorOS Pipeline Dashboard 🚀")
st.caption("Built for infinite leverage. Every segment, click, and draft is compounding proof of skill.")

uploaded_file = st.file_uploader("Upload your pipeline_export.csv", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("pipeline_export.csv")

# -------- Sidebar: Operator Filters & Session --------
with st.sidebar:
    st.header("🔍 Smart Filters & Segments")
    min_score = int(df["lead_score"].astype(float).min())
    max_score = int(df["lead_score"].astype(float).max())
    score_range = st.slider("Lead Score", min_score, max_score, (min_score, max_score))
    tag_filter = st.multiselect("Tags", sorted({t.strip() for tags in df["tags"].dropna().astype(str) for t in tags.split(",") if t.strip()}), default=[])
    if "industry" in df.columns:
        industry_filter = st.multiselect("Industry", sorted(set(df["industry"].dropna())), default=[])
    else:
        industry_filter = []
    # Save/load session filters
    if st.button("💾 Save Current Segment"):
        st.session_state["saved_segment"] = {
            "score_range": score_range,
            "tag_filter": tag_filter,
            "industry_filter": industry_filter
        }
        st.success("Segment saved for this session!")
    if st.button("📤 Load Saved Segment") and "saved_segment" in st.session_state:
        seg = st.session_state["saved_segment"]
        score_range = seg.get("score_range", score_range)
        tag_filter = seg.get("tag_filter", tag_filter)
        industry_filter = seg.get("industry_filter", industry_filter)
        st.info("Segment loaded!")
    st.markdown("---")
    st.write("**Operator Power Tips:**")
    st.write("- Save and export your favorite segments.")
    st.write("- Add new enrichment columns and the dashboard will auto-update.")

# -------- Filtered Data --------
filtered_df = df[
    (df["lead_score"].astype(float).between(*score_range)) &
    (df["tags"].astype(str).apply(lambda x: any(tag in x for tag in tag_filter) if tag_filter else True)) &
    (df["industry"].astype(str).apply(lambda x: any(ind in x for ind in industry_filter) if industry_filter else True) if "industry" in df.columns else True)
]

st.success(f"{len(filtered_df)} leads match your filters (out of {len(df)})")

# -------- Interactive Table: Action Buttons --------
def email_button(email):
    return f"[📧](mailto:{email})" if pd.notnull(email) and str(email).strip() else ""

def linkedin_button(url):
    return f"[🔗]({url})" if pd.notnull(url) and str(url).startswith("http") else ""

table_df = filtered_df.copy()
if "contact_email" in table_df.columns:
    table_df["Email"] = table_df["contact_email"].apply(email_button)
if "linkedin_url" in table_df.columns:
    table_df["LinkedIn"] = table_df["linkedin_url"].apply(linkedin_button)

base_cols = ["company_name", "lead_score", "tags", "industry", "Email", "LinkedIn"]
cols_to_show = [col for col in base_cols if col in table_df.columns] + [col for col in table_df.columns if col not in base_cols and col not in ["contact_email", "linkedin_url"]]
st.dataframe(table_df[cols_to_show], use_container_width=True)

# -------- Analytics: Charts & Reports --------
st.markdown("### 📊 Lead Analytics")
st.bar_chart(filtered_df["lead_score"])

if "tags" in filtered_df.columns:
    tag_counts = filtered_df["tags"].astype(str).str.get_dummies(",").sum().sort_values(ascending=False)
    st.markdown("#### 🏷️ Tag Frequency")
    st.bar_chart(tag_counts)

if "industry" in filtered_df.columns:
    st.markdown("#### 🌍 Industry Distribution")
    industry_counts = filtered_df["industry"].value_counts()
    st.pyplot(industry_counts.plot.pie(autopct='%1.1f%%', figsize=(5, 5)).get_figure())

# -------- Export --------
st.markdown("### 📤 Export Tools")
st.download_button("Download Current Segment as CSV", filtered_df.to_csv(index=False), file_name="pipeline_segment.csv")
if st.button("Copy Table to Clipboard (CSV)", type="primary"):
    st.write("Copying is browser dependent; download CSV for best results.")

# -------- Outreach Draft Generator (Quantum!) --------
st.markdown("### ✉️ One-Click Outreach Draft")
selected = st.selectbox("Choose a lead for draft:", filtered_df["company_name"] if not filtered_df.empty else [""])
if selected and not filtered_df.empty:
    lead = filtered_df[filtered_df["company_name"] == selected].iloc[0]
    company = lead.get("company_name", "")
    email = lead.get("contact_email", "")
    tags = lead.get("tags", "")
    st.code(f"""Subject: Quick question for {company}

Hi {email},

I’m reaching out because my system flagged {company} as a top SaaS innovator in [{tags}]. Would you be open to a chat about integration or partnerships?

Best,
[Your Name]
""", language="text")
    # Optional: GPT summary (commented out unless you add your OpenAI key)
    # if st.button("✨ AI Lead Summary"):
    #     openai.api_key = st.secrets["OPENAI_API_KEY"]
    #     completion = openai.ChatCompletion.create(
    #         model="gpt-4",
    #         messages=[{"role": "user", "content": f"Summarize why {company} (tags: {tags}) is a good fit for outreach."}]
    #     )
    #     st.info(completion.choices[0].message.content)

# -------- Operator Enchantments --------
st.markdown("### ⚡ OperatorOS Enchantments")
st.markdown("""
- **Self-healing:** Add any new column to your CSV and the dashboard adapts.
- **Ready for enrichment:** Merge in LinkedIn data, funding, AI scores—dashboard will show all fields.
- **API/Slack/Notion Ready:** Want to push hot leads to Slack, Notion, or Airtable? Just ask.
- **Battle-tested:** Save, reload, or export any segment.
- **Team Proof:** Show this to clients, recruiters, or as a SaaS GTM asset.
""")

st.info("Drop any new CSV to update in real time. Ready for outbound, analytics, or team demo. OperatorOS by [Alex Minnick]—limitless, compounding leverage.")

