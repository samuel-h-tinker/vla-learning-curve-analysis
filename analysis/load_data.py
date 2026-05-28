"""
load_data.py
 
Loads AIRA training data from either:
  - A local synthetic CSV (USE_SYNTHETIC = True)  — for development/testing
  - The live Google Sheet via CSV export URL       (USE_SYNTHETIC = False) — for real data
 
Switch the flag below depending on what you need.
"""
 
import pandas as pd
 
# --- Toggle this flag ---
USE_SYNTHETIC = True   # True = local CSV | False = live Google Sheet
 
# --- Google Sheets config ---
SHEET_ID = "1o5cmqdg-Nynxv8iFcWNgUupbaXVI71XjsghqAIot6GU"
 
GIDS = {
    "task1":  "0",
    "master": "494851830",
}
 
# --- Local synthetic data paths ---
SYNTHETIC_PATHS = {
    "task1": "data/synthetic_task1.csv",
}
 
def make_sheet_url(gid):
    """Convert a sheet GID to a CSV export URL."""
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
 
def load_task_record(task_key="task1"):
    """
    Load the task attempt record for a given task.
    Returns a pandas DataFrame with one row per attempt.
    """
    if USE_SYNTHETIC:
        path = SYNTHETIC_PATHS[task_key]
        df = pd.read_csv(path)
        print(f"[synthetic] Loaded {len(df)} rows from {path}")
    else:
        url = make_sheet_url(GIDS[task_key])
        df = pd.read_csv(url)
        print(f"[live] Loaded {len(df)} rows from Google Sheet (gid={GIDS[task_key]})")
    return df
 
def load_master_record():
    """
    Load the master record summarizing completed tasks.
    Always reads from the live Google Sheet (no synthetic version needed).
    """
    url = make_sheet_url(GIDS["master"])
    df = pd.read_csv(url)
    print(f"[live] Loaded master record: {len(df)} tasks")
    return df
 
if __name__ == "__main__":
    task_df = load_task_record()
    print("\nTask Record preview:")
    print(task_df.head())
    print(f"\nColumns: {list(task_df.columns)}")
    print(f"Shape:   {task_df.shape}")