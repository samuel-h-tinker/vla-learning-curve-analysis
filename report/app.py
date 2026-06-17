"""
app.py

Streamlit interface for the AIRA learning-curve analysis.
Lets you toggle between local synthetic data and the live Google Sheet
and see the learning curve update on each switch.

Run from the repo root:
    streamlit run web-app-interface/app.py
"""

import sys
import os

# load_data.py and learning_curve.py live in ../analysis, not in this folder.
# Add that folder to the import path so `import load_data` can find them.
# Computed from __file__ so it resolves no matter where you launch from.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "analysis"))

import streamlit as st
import load_data
from learning_curve import compute_success_rate, plot_learning_curve

st.title("AIRA Learning Curve")

# Radio returns the selected string; map it to the boolean the loader reads.
source = st.radio("Data source", ["Synthetic Data", "Live Google Sheet"])
load_data.USE_SYNTHETIC = (source == "Synthetic Data")

# Wrap the load + plot so a network or sharing hiccup on the live sheet
# shows a clean message instead of a red traceback mid-demo.
try:
    df = load_data.load_task_record("task1")
    summary = compute_success_rate(df)
    fig = plot_learning_curve(summary, "task1")
    st.pyplot(fig)
except Exception as e:
    st.error(f"Couldn't load or plot the data: {e}")