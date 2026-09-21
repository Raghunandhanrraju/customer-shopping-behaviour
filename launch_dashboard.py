"""
Double-clickable Python launcher for Customer Behavior Dashboard.
Automatically starts Streamlit server and opens http://localhost:8501 in default browser.
"""

import os
import sys
import time
import webbrowser
import subprocess

def main():
    print("=" * 65)
    print("CUSTOMER SHOPPING BEHAVIOR ANALYSIS - DASHBOARD LAUNCHER")
    print("=" * 65)
    
    # Check data files
    if not os.path.exists("cleaned_customer_shopping_behavior.csv"):
        print("[*] Running ETL pipeline to prepare data...")
        import data_pipeline
        data_pipeline.main()
    else:
        print("[*] Data files and SQLite database verified.")

    url = "http://localhost:8501"
    print(f"[*] Opening browser at {url} ...")
    webbrowser.open(url)

    print(f"[*] Launching Streamlit server on localhost...")
    print("=" * 65)
    print(f"Dashboard running at: {url}")
    print("Press Ctrl+C to stop the dashboard server.")
    print("=" * 65)

    cmd = [sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.headless", "true"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[*] Dashboard server stopped successfully.")

if __name__ == "__main__":
    main()
