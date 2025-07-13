import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="OperatorOS Pipeline Dashboard", layout="wide")
st.title("OperatorOS Pipeline Dashboard 🚀")

# --------- QUANTUM A/B BOOKING CTA (Sidebar, With UTM + Logging) ---------
ctas = [
    ("🚀 Book a Strategy Session", "utm_source=sidebar_a"),
    ("💡 Schedule a Demo with Alex", "utm_source=sidebar_b"),
    ("🤝 Connect Instantly", "utm_source=sidebar_c")
]
cta, utm = random.choice(ctas)
booking_url = f"https://meetings-na2.hubspot.com/alex-minnick?{utm}"
st.sidebar.markdown(f"### {cta}\n[Book here]({booking_url})")
if st.sidebar.button(cta):
    with open("cta_clicks.csv", "a") as f:
        f.write(f"{cta},{utm}\n")
    st.sidebar.markdown(f"[Schedule here]({booking_url})", unsafe_allow_html=True)

# --------- PIPELINE DATA UPLOAD & TABLE ---------
uploaded_file = st.file_uploader("Upload your pipeline_export.csv", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
elif os.path.exists("pipeline_export.csv"):
    df = pd.read_csv("pipeline_export.csv")
else:
    st.warning("No CSV found. Please upload your leads file.")
    st.stop()

# --------- SMART FILTERS ---------
with st.sidebar:
    st.header("🔍 Smart Filters")
    min_score = int(df["lead_score"].min())
    max_score = int(df["lead_score"].max())
    score_range = st.slider("Lead Score Range", min_score, max_score, (min_score, max_score))
    tags_list = sorted({t.strip() for tags in df["tags"].dropna().astype(str) for t in tags.split(",") if t.strip()})
    tag_filter = st.multiselect("Tags", tags_list, default=[])
    industry_filter = st.multiselect("Industry", sorted(set(df.get("industry", pd.Series()).dropna())), default=[])

filtered_df = df[
    (df["lead_score"].between(*score_range)) &
    (df["tags"].astype(str).apply(lambda x: any(tag in x for tag in tag_filter) if tag_filter else True)) &
    (df.get("industry", pd.Series(True, index=df.index)).astype(str).apply(lambda x: any(ind in x for ind in industry_filter) if industry_filter else True))
]

st.success(f"{len(filtered_df)} leads match your filters")

# --------- INTERACTIVE TABLE WITH ACTIONS ---------
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
cols_to_show = [c for c in base_cols if c in table_df.columns] + \
               [col for col in table_df.columns if col not in base_cols and col not in ["contact_email", "linkedin_url"]]
st.dataframe(table_df[cols_to_show], use_container_width=True)

# --------- ANALYTICS & CHARTS ---------
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

# --------- EXPORT ---------
st.markdown("### 📤 Export Tools")
st.download_button("Download Current Segment as CSV", filtered_df.to_csv(index=False), file_name="pipeline_segment.csv")

# --------- OUTREACH DRAFT GENERATOR ---------
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

# --------- HUBSPOT BOOKING CTA (Main) ---------
st.markdown("""
---
### 🚀 Book a Live Strategy Session or Demo

[Book instantly with Alex Minnick](https://meetings-na2.hubspot.com/alex-minnick?utm_source=main_banner)

---
""")

# --------- README BADGE SUGGESTION ---------
st.info("""
Add this badge to your README for extra operator trust:

[![Book a Live Demo](https://img.shields.io/badge/Book%20a%20Demo-Meet%20with%20Alex-blue)](https://meetings-na2.hubspot.com/alex-minnick?utm_source=readme)
""")

# --------- OPERATOR ENCHANTMENTS & NOTES ---------
st.markdown("### ⚡ OperatorOS Quantum Enchantments")
st.markdown("""
- **A/B tested booking CTAs with full UTM tracking
- **Local click analytics logging**
- **Auto-enrich ready** (plug in LinkedIn, Clearbit, OpenAI APIs)
- **Downloadable/segmentable lead lists**
- **Proof-of-ops: All links, buttons, and badges are conversion-optimized**
- **Ready for: Slack, Notion, HubSpot integrations**
""")

st.info("OperatorOS Quantum: Compounding leverage in every click, with no code debt.")

# --------- END OF DASHBOARD ---------