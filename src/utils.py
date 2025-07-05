import matplotlib.pyplot as plt
import seaborn as sns
import os

try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))

RESULT_PATH = os.path.join(BASE_DIR, "results", "report.html")
PLOT_PATH = os.path.join(BASE_DIR, "results", "plots")

def save_plot_if_needed(filename, show=False):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.tight_layout()
    plt.savefig(filename)
    if show:
        plt.show()
