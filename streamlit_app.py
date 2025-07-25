import streamlit as st
import pandas as pd
import json
from io import StringIO

# -----------------------------
# Default keyword dictionaries
# -----------------------------
DEFAULT_DICTIONARIES = {
    "urgency_marketing": [
        "limited", "limited time", "limited run", "limited edition", "order now",
        "last chance", "hurry", "while supplies last", "before they're gone",
        "selling out", "selling fast", "act now", "don't wait", "today only",
        "expires soon", "final hours", "almost gone"
    ],
    "exclusive_marketing": [
        "exclusive", "exclusively", "exclusive offer", "exclusive deal",
        "members only", "vip", "special access", "invitation only",
        "premium", "privileged", "limited access", "select customers",
        "insider", "private sale", "early access"
    ]
}

st.set_page_config(
    page_title="Marketing Statement Classifier",
    page_icon="📣",
    layout="centered",
)

st.title("📣 Marketing Statement Classifier")
st.markdown(
    """
    Upload a CSV file containing a **`Statement`** column, then fine-tune the keyword dictionaries to classify each
    statement into one or more marketing categories.
    """
)

# ------------------------------------------------------------------
# Sidebar – step 1: dataset upload
# ------------------------------------------------------------------
with st.sidebar:
    st.header("1️⃣ Upload dataset")
    csv_file = st.file_uploader("CSV file (must include a 'Statement' column)", type=["csv"])

    st.header("2️⃣ Configure dictionaries")
    st.caption("Edit the JSON below to add, remove, or rename categories and keywords.")

    # Display dictionaries as pretty-printed JSON for editing
    dict_json = st.text_area(
        "Dictionaries (JSON)",
        value=json.dumps(DEFAULT_DICTIONARIES, indent=2),
        height=300,
    )

    if st.button("Apply changes"):
        try:
            user_dict = json.loads(dict_json)
            # Convert lists to sets for faster lookup
            DICTIONARIES = {k: set(map(str.lower, v)) for k, v in user_dict.items()}
            st.success("Dictionaries updated!")
        except Exception as e:
            st.error(f"❌ Invalid JSON: {e}")
            DICTIONARIES = {k: set(v) for k, v in DEFAULT_DICTIONARIES.items()}
    else:
        DICTIONARIES = {k: set(v) for k, v in DEFAULT_DICTIONARIES.items()}

# ------------------------------------------------------------------
# Main app – process and display results
# ------------------------------------------------------------------
if csv_file is None:
    st.info("⬅️ Upload a CSV file to get started.")
    st.stop()

# Read CSV i
