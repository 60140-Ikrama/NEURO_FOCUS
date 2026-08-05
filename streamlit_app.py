"""
Streamlit Cloud Entrypoint for NeuroLearn Research Suite.
Delegates execution to dashboard/app.py.
"""
import os
import sys
import runpy

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard", "app.py")
    runpy.run_path(app_path, run_name="__main__")
