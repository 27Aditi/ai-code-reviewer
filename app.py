import streamlit as st
import os
from reviewer import generate_review, fetch_github_pr_diff, parse_diff

st.set_page_config(
    page_title="ReviewPulse AI | Intelligent PR & Code Reviewer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-polish modern UI
st.markdown("""
<style>
    /* Main container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    /* Headers styling */
    h1, h2, h3 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    /* Metrics card */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .badge-primary {
        background-color: #3b82f6;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    /* Code review output container */
    .stMarkdown pre {
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sample diffs for instant demo
SAMPLE_SNIPPET = """def calculate_discount(price, user_role, promo_code):
    # Potential SQL injection and missing validation
    query = f"SELECT discount_percent FROM coupons WHERE code = '{promo_code}'"
    discount = db.execute(query).fetchone()[0]
    
    if user_role == "admin":
        return 0
    elif user_role == "vip":
        return price * (1 - (discount / 100))
    else:
        return price - discount
"""

SAMPLE_DIFF = """diff --git a/services/auth.py b/services/auth.py
index a1b2c3d..e4f5g6h 100644
--- a/services/auth.py
+++ b/services/auth.py
@@ -12,6 +12,12 @@ def authenticate_user(username, password):
-    user = db.users.find_one({"username": username})
-    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
-        return generate_jwt(user['id'])
+    user = db.users.find_one({"username": username})
+    # Bypass password verification for local admin testing
+    if username == "admin":
+        return generate_jwt(user['id'], is_admin=True)
+    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
+        return generate_jwt(user['id'])
     return None
"""

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("⚡ ReviewPulse AI")
    st.caption("Principal Engineer in your browser")
    st.markdown("---")
    
    st.subheader("⚙️ LLM Provider & Settings")
    provider = st.selectbox(
        "AI Provider",
        ["Google Gemini", "OpenAI"],
        index=0,
        help="Select the AI intelligence provider."
    )
    
    if provider == "Google Gemini":
        model = st.selectbox(
            "Gemini Model",
            ["gemini-3.8-flash", "gemini-3.5-flash-lite"],
            index=0
        )
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=os.getenv("GEMINI_API_KEY", ""),
            placeholder="AIzaSy...",
            help="Get your key at https://aistudio.google.com"
        )
    else:
        model = st.selectbox(
            "OpenAI Model",
            ["gpt-4o", "gpt-4o-mini", "o3-mini"],
            index=0
        )
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            placeholder="sk-...",
            help="Get your key at https://platform.openai.com"
        )
        
    st.markdown("---")
    st.subheader("🎯 Review Focus")
    review_focus = st.selectbox(
        "Focus Persona",
        [
            "General (Bugs + Security + Performance)",
            "Strict Security Auditor (OWASP, Injections, Auth)",
            "Performance & Scalability Optimization",
            "Clean Architecture & Refactoring",
            "Junior Dev Mentorship & Explainer"
        ]
    )
    
    st.markdown("---")
    st.subheader("🔑 Optional GitHub Token")
    github_token = st.text_input(
        "GitHub Personal Access Token",
        type="password",
        value=os.getenv("GITHUB_TOKEN", ""),
        help="Optional: Increases rate limit or allows reading private PRs."
    )
    
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:0.8rem; opacity:0.8;">
        Built with ❤️ for developers & engineering teams.<br>
        Ready for <b>Streamlit Cloud</b> deployment.
        </div>
        """,
        unsafe_allow_html=True
    )


# --- MAIN INTERFACE ---
st.markdown("# 🚀 ReviewPulse AI")
st.markdown("### Automated Pull Request Explainer & Senior Engineering Code Reviewer")
st.write(
    "Analyze unified git diffs, raw code, or public GitHub Pull Requests. "
    "Get instant security audits, edge case detection, and ready-to-merge PR summaries."
)

tab1, tab2, tab3 = st.tabs(["🔗 GitHub Pull Request", "📝 Paste Git Diff", "💻 Paste Source Code"])

code_payload = ""
pr_context = ""
metadata_display = None

# TAB 1: GITHUB PR
with tab1:
    pr_url = st.text_input(
        "Enter Public GitHub PR URL",
        placeholder="https://github.com/torvalds/linux/pull/123",
        help="Paste any GitHub Pull Request link to fetch the live diff."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        fetch_btn = st.button("Fetch PR Details", type="secondary")
        
    if fetch_btn:
        if not pr_url:
            st.warning("Please provide a valid GitHub PR URL.")
        else:
            with st.spinner("Fetching PR metadata and git diff from GitHub..."):
                try:
                    pr_info = fetch_github_pr_diff(pr_url, github_token if github_token else None)
                    st.session_state["fetched_pr"] = pr_info
                    st.success(f"Fetched PR #{pr_url.split('/')[-1]}: {pr_info['title']}")
                except Exception as e:
                    st.error(f"Failed to fetch PR: {str(e)}")

    if "fetched_pr" in st.session_state:
        pr_info = st.session_state["fetched_pr"]
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Status", pr_info.get("state", "").upper())
        m2.metric("Changed Files", pr_info.get("changed_files", 0))
        m3.metric("Additions", f"+{pr_info.get('additions', 0)}")
        m4.metric("Deletions", f"-{pr_info.get('deletions', 0)}")
        
        st.markdown(f"**Author:** `{pr_info.get('author')}` | **Title:** {pr_info.get('title')}")
        with st.expander("Show Original PR Description"):
            st.markdown(pr_info.get("body") or "*No description provided by author.*")
            
        code_payload = pr_info.get("diff", "")
        pr_context = f"PR Title: {pr_info.get('title')}\nAuthor: {pr_info.get('author')}\nDescription:\n{pr_info.get('body')}"

# TAB 2: GIT DIFF
with tab2:
    st.caption("Paste a `git diff` output or unified patch.")
    diff_input = st.text_area(
        "Unified Diff",
        height=240,
        value=SAMPLE_DIFF,
        placeholder="diff --git a/app.py b/app.py\n..."
    )
    diff_context = st.text_input("Context / Commit Title", placeholder="e.g. Refactored user authentication logic")
    if tab2:
        if not code_payload:  # Only override if PR tab wasn't the active source
            code_payload = diff_input
            pr_context = diff_context

# TAB 3: RAW CODE
with tab3:
    st.caption("Analyze a standalone function, file, or proposed script.")
    raw_code = st.text_area(
        "Source Code",
        height=240,
        value=SAMPLE_SNIPPET,
        placeholder="def my_function():\n    pass"
    )
    raw_context = st.text_input("Function / Feature Purpose", placeholder="e.g. Discount calculation logic for checkout")
    if tab3:
        if not code_payload:
            code_payload = raw_code
            pr_context = raw_context

st.markdown("---")

# Quick Review Execution Bar
action_col1, action_col2 = st.columns([1, 3])
with action_col1:
    start_review = st.button("🚀 Run Code Review & Explainer", type="primary", use_container_width=True)

with action_col2:
    st.info(f"Using **{provider}** ({model}) | Persona: **{review_focus}**")

if start_review:
    if not api_key:
        st.error(f"⚠️ Please enter your **{provider} API Key** in the sidebar to run the review.")
    elif not code_payload.strip():
        st.warning("⚠️ No code or diff provided. Please select or paste code/diff to review.")
    else:
        with st.spinner("Analyzing code architecture, security vulnerabilities, and logic flaws..."):
            try:
                review_result = generate_review(
                    provider=provider,
                    api_key=api_key,
                    model=model,
                    code_or_diff=code_payload,
                    context=pr_context,
                    review_focus=review_focus
                )
                st.session_state["review_result"] = review_result
            except Exception as e:
                st.error(f"Error executing review: {str(e)}")

# Display Review Results
if "review_result" in st.session_state:
    st.markdown("---")
    st.subheader("📋 Comprehensive Review Report")
    
    # Download report button
    st.download_button(
        label="💾 Download Review as Markdown",
        data=st.session_state["review_result"],
        file_name="pr_code_review.md",
        mime="text/markdown"
    )
    
    st.markdown(st.session_state["review_result"])
