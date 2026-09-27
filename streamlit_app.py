# streamlit_app.py - Browser front end for ExcelSwitch (260927HHMM)
# Calls the same functions the MCP server uses.
# Run: streamlit run streamlit_app.py

import streamlit as st
from excel_tools import list_tasks, execute

st.set_page_config(page_title="Excel Switch", layout="wide")
st.title("Excel Switch")
st.caption("Offline Excel automation — same backend as the AI Secretary")

# --- Sidebar: category picker ---
CATEGORIES = ["all", "clean", "transform", "read", "analyze",
              "convert", "deliver", "ops"]
cat = st.sidebar.selectbox("Category", CATEGORIES, index=0)

tasks = list_tasks(cat)
if not tasks:
    st.warning("No tasks in this category.")
    st.stop()

# --- Task picker ---
labels = [f"{t['id']} — {t['name']}: {t['description']}" for t in tasks]
picked_label = st.selectbox("Task", labels, index=0)
picked = tasks[labels.index(picked_label)]

# --- Parameter inputs ---
st.subheader("Parameters")
params = {}
for pname in picked["params"]:
    # Look up the original parameter spec for its type
    params[pname] = st.text_input(pname, value="")

# --- Run button ---
if st.button("▶ Run", type="primary"):
    clean_params = {k: v for k, v in params.items() if v}
    with st.spinner("Running..."):
        result = execute(picked["id"], clean_params)
    st.subheader("Result")
    if result.get("success"):
        st.success("Task completed")
        st.json(result)
    else:
        st.error(result.get("error", "Unknown error"))
        st.json(result)