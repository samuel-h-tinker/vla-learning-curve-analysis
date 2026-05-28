"""
generate_synthetic_data.py
 
Generates synthetic learning curve data for the tube_to_vortexer task,
matching the Google Sheets schema exactly. Used for development and testing
before real training data is available.
 
Output: data/synthetic_task1.csv
"""
 
import numpy as np
import pandas as pd
import os
 
# Random seed for reproducibility
np.random.seed(42)
 
# --- Configuration ---
TASK_NAME = "tube_to_vortexer"
TRAINING_VOLUMES = [10, 25, 50, 75, 100, 150, 200, 250]  # cumulative examples seen
ATTEMPTS_PER_VOLUME = 18                                   # test attempts at each volume (~150 total rows)
FAILURE_TYPES = ["dropped", "missed_target", "timeout", "grip_failure"]
 
# --- Logistic curve parameters ---
# Success probability follows: P = L / (1 + exp(-k * (x - x0)))
# Calibrated so P(10) ≈ 0.15 and P(250) ≈ 0.80, ceiling at L = 0.85
L  = 0.85   # maximum achievable success rate
k  = 0.018  # steepness of the learning curve
x0 = 96     # inflection point (examples seen where P = L/2)
 
def success_probability(examples_seen):
    """Return success probability at a given training volume."""
    return L / (1 + np.exp(-k * (examples_seen - x0)))
 
# --- Generate rows ---
rows = []
trial_id = 1
 
for volume in TRAINING_VOLUMES:
    p_success = success_probability(volume)
 
    for attempt in range(1, ATTEMPTS_PER_VOLUME + 1):
        success = int(np.random.random() < p_success)
 
        # failure_type is empty on success, random category on failure
        if success == 1:
            failure_type = ""
        else:
            failure_type = np.random.choice(FAILURE_TYPES)
 
        # attempt duration: normally distributed around 8s, clipped to positive
        duration = round(max(1.0, np.random.normal(loc=8.0, scale=1.5)), 2)
 
        rows.append({
            "trial_id":                trial_id,
            "task":                    TASK_NAME,
            "cumulative_examples_seen": volume,
            "test_attempt":            attempt,
            "test_success":            success,
            "failure_type":            failure_type,
            "in_distribution":         "yes",
            "attempt_duration":        duration,
        })
 
        trial_id += 1
 
# --- Save to CSV ---
df = pd.DataFrame(rows)
 
os.makedirs("data", exist_ok=True)
output_path = "data/synthetic_task1.csv"
df.to_csv(output_path, index=False)
 
print(f"Generated {len(df)} rows -> {output_path}")
print(f"\nSuccess rate by training volume:")
summary = df.groupby("cumulative_examples_seen")["test_success"].mean().round(2)
print(summary.to_string())
 
