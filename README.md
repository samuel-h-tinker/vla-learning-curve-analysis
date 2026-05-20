# vla-learning-curve-analysis
Measuring how many training examples a Vision-Action-Language model needs to reliably execute physical lab tasks. Built for AIRA: a robotics startup automating wet lab workflows at University of Washington and Stanford.


# VLA Learning Curve Analysis

**How many training examples does a Vision-Language-Action model need to reliably execute a physical lab task?**

This project measures the learning curve of [AIRA](https://github.com/), a Vision-Language-Action (VLA) model paired with a collaborative robot arm designed to automate wet-lab workflows. The goal is to produce a data-driven answer to a question that currently has none: how much training data does it actually take for a VLA system to reach reliable task performance — and does that number vary predictably by task type?

*Conducted in collaboration with AIRA | Samuel Tinker, University of Washington*

---

## Background

AIRA connects a trained Vision-Language Model to a commercial collaborative robot, enabling researchers to automate physical lab protocols using natural language instructions. Before deploying AIRA at scale, the team needs to understand its training data requirements — both to plan data collection and to predict costs for new task categories.

The plan is to train incrementally and observe where performance stabilizes.

---

## Research Questions

1. **Learning curve per task** — How does success rate change as a function of training examples seen? Where does it plateau?
2. **Cross-task learning rate** — Does AIRA learn new tasks faster after training on prior tasks? Is transfer stronger within task categories?
3. **Task complexity classification** — Can tasks be grouped by how much data they require? What predicts which bucket a task falls into?
4. **Failure pattern analysis** — What types of errors dominate early in training versus late? Does the error profile shift as the model improves?

---

## Data

Data is collected by the AIRA engineering team during live training runs and recorded in a shared Google Sheet. Each row represents a single attempt at a task.

**Task Record** (one row per attempt)

| Column | Description |
|---|---|
| `trial_id` | Unique identifier for each attempt |
| `task` | Task name |
| `examples_seen` | Number of training examples seen before this attempt |
| `attempt` | Attempt number within the trial |
| `success` | Binary outcome (1 = success, 0 = failure) |
| `failure_type` | Categorical: Procedural Deviation, Instrumental Precision, Mechanical Error, Aseptic Technique |
| `notes` | Free text |

**Master Record** (one row per completed task)

| Column | Description |
|---|---|
| `task_id` | Unique task identifier |
| `task_name` | Human-readable task name |
| `task_category` | Categorical grouping (e.g., Liquid Handling, Cell Culture) |
| `threshold` | Success rate defined as reliable performance |
| `examples_to_threshold` | Primary outcome: how many examples to reach threshold |
| `notes` | Free text |

---

## Methods

Training runs are conducted incrementally. Starting from a small example count, batches of examples are added and the model is evaluated after each batch. Success rate is plotted against cumulative examples seen, and a threshold is defined as the point where additional examples produce diminishing returns.

**Tools:** Python, pandas, matplotlib / plotly, Google Sheets API (CSV export)

**Planned statistical approaches:**
- Curve fitting to model the learning trajectory
- Threshold detection via rolling success rate
- Cross-task comparison using examples-to-threshold as the primary outcome
- Failure category breakdown by training stage

---

## Deliverables

- [ ] Learning curve plots per task
- [ ] Cross-task learning rate comparison
- [ ] Task complexity classification
- [ ] Failure pattern analysis by training stage
- [ ] Streamlit dashboard *(stretch)*

---

## Status

**Active — data collection in progress.**
Analysis scripts are in development. Results and visualizations will be added as training data becomes available.

---

## Repository Structure

```
vla-learning-curve-analysis/
├── data/               # Raw and processed data exports
├── analysis/           # Python scripts for each deliverable
├── visuals/            # Output plots and figures
├── report/             # Written summary of findings
└── README.md
```

---

## Contact

Samuel Tinker — University of Washington
[LinkedIn](https://linkedin.com) · [GitHub](https://github.com)
