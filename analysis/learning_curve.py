import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.optimize as opt

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

def fit_logistic(summary):
    """ fits a logistic function to the summary data
    Args:
        summary: a series of the cumulative examples seen and success rate
    Returns:
        xvals: smoothed x values 
        yvals: logistic values at the smoothed x
    """
    x = summary.index
    logistic = lambda t, L, r, t0: L / (1 + np.exp(-r * (t-t0)))
    params, _ = opt.curve_fit(logistic, x, summary.values, p0=[.9, .02, 100])
    t_smooth = np.linspace(x[0], x[-1], 300)
    L, r, t0 = params
    y_smooth = logistic(t_smooth, L, r, t0)
    return t_smooth, y_smooth

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
    ax.plot(x, y, marker = 'o', linestyle = 'none', color = 'blue', label= 'data')

    x_smooth, y_smooth = fit_logistic(summary)
    ax.plot(x_smooth, y_smooth, label= "logistic fitted line", color='green')
    ax.axhline(.95, color='r', linestyle = '--', label='ideal threshold')
    ax.set_xlabel("Cumulative examples seen")
    ax.set_ylabel("Success Rate")
    ax.set_title("Learning curve")
    ax.grid()
    ax.legend()
    fig.savefig(f"visualization/learning_curve_{task_name}.png")
    return fig

if __name__ == "__main__":
    df = load_task_record("task1")
    print(df.head())
    summary = compute_success_rate(df)
    plot_learning_curve(summary, "task1")