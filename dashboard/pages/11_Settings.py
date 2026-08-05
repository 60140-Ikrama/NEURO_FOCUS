"""
Page 11: Configuration Manager Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.manager import ConfigManager
from dashboard.components import render_header

render_header("Platform Settings", "Global Configuration Manager & Parameter Overrides")

cfg_mgr = ConfigManager()

st.markdown("### Research Platform Information")
st.text_input("Platform Name:", cfg_mgr.get("platform.name"), disabled=True)
st.text_input("Version:", cfg_mgr.get("platform.version"), disabled=True)
st.text_input("Laboratory Institution:", cfg_mgr.get("platform.institution"))

st.markdown("---")
st.markdown("### Default Preprocessing Cutoffs")
c1, c2 = st.columns(2)
with c1:
    l_cut = st.number_input("Bandpass Low Cutoff (Hz):", 0.1, 10.0, float(cfg_mgr.get("preprocessing.bandpass.lowcut", 1.0)))
with c2:
    h_cut = st.number_input("Bandpass High Cutoff (Hz):", 10.0, 100.0, float(cfg_mgr.get("preprocessing.bandpass.highcut", 40.0)))

if st.button("Save Settings Configuration"):
    cfg_mgr.set("preprocessing.bandpass.lowcut", l_cut)
    cfg_mgr.set("preprocessing.bandpass.highcut", h_cut)
    cfg_mgr.save()
    st.success("Global research settings updated successfully!")
