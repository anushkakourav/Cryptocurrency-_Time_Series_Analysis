# =========================================================
# charts.py
# Common chart helper utilities
# =========================================================

import matplotlib.pyplot as plt
import seaborn as sns

# Set global plotting style
def set_plot_style():
    """
    Apply a consistent visual style to all matplotlib/seaborn charts.
    """
    sns.set_theme(style="darkgrid")
    plt.rcParams["figure.figsize"] = (10, 5)
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 11
    plt.rcParams["legend.fontsize"] = 10


def format_axes(ax, title=None, xlabel=None, ylabel=None):
    """
    Apply common formatting to matplotlib axes.
    """
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    ax.grid(True, alpha=0.3)


def show_plot():
    """
    Safely render matplotlib plot in Streamlit.
    """
    plt.tight_layout()
    plt.show()
