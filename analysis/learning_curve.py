import matplotlib.pyplot as plt
import pandas as pd

# Load the task record (either synthetic or live)
from load_data import load_task_record



def compute_success_rate(df):
    """ Converts raw data to a dataframe of percent success rate
    at every level of training
    Args:
        df: robot testing data
    Returns:
        The grouped summary
    """
    summary = df.groupby("cumulative_examples_seen")['test_success'].mean()
    return summary


def plot_learning_curve(summary, task_name):
    """ Plots the learning curve for the robot accuracy against cumulative examples seen
    Args:
        summary: dataframe containg the cumulative examples seen
        as x values, and the accuracy percentage as y values
    Returns:
        nothing
    """
    x = summary.index
    y = summary.values
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axhline(.95, color='r', linestyle = '--')
    ax.set_xlabel("Cumulative examples seen")
    ax.set_ylabel("Success Rate")
    ax.set_title("Learning curve")
    ax.grid()
    fig.savefig(f"visualization/learning_curve_{task_name}.png")
    plt.show()

if __name__ == "__main__":
    df = load_task_record("task1")
    print(df.head())
    summary = compute_success_rate(df)
    plot_learning_curve(summary, "task1")