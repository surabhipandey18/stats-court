import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy.stats as stats
from scipy.stats import ttest_ind, pearsonr, spearmanr
from src.utils import save_plot_if_needed

try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))

PLOT_PATH = os.path.join(BASE_DIR, "results", "plots")

def categorical_associations(df, col1, col2, return_all=False, save_path=None):
    contingency = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    if p < 0.05:
        verdict = "Reject H₀"
        interpretation = f"There is no significant association between {col1} and {col2} (p={p:.4f})"
    else:
        verdict = "Fail to Reject H₀"
        interpretation = f"Significant association found between {col1} and {col2} (p={p:.4f})"
    plt.figure(figsize=(10, 6))
    sns.heatmap(contingency, annot=True, fmt='d', cmap='Blues')
    plt.title(f"{col1} vs {col2}")
    save_plot_if_needed(save_path)
    plt.close()
    rel_path = os.path.relpath(save_path, os.path.join(BASE_DIR, "results"))
    if return_all:
        return chi2, p, verdict, interpretation, rel_path

def t_test(df, group_col, target_col, return_all=False, save_path=None):
    groups = df[group_col].dropna().unique()
    if len(groups) != 2:
        raise ValueError("T-test requires exactly 2 groups")
    group1 = df[df[group_col] == groups[0]][target_col].dropna()
    group2 = df[df[group_col] == groups[1]][target_col].dropna()
    t_stat, p = ttest_ind(group1, group2, equal_var=False)
    if p < 0.05:
        verdict = "Reject H₀"
        interpretation = f"Means do not differ significantly between groups of {group_col} on {target_col}"
    else:
        verdict = "Fail to Reject H₀"
        interpretation = f"Significant mean difference found between groups of {group_col} on {target_col}"
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x=group_col, y=target_col)
    plt.title(f"Boxplot of {target_col} by {group_col}")
    save_plot_if_needed(save_path)
    plt.close()
    rel_path = os.path.relpath(save_path, os.path.join(BASE_DIR, "results"))
    if return_all:
        return t_stat, p, verdict, interpretation, rel_path

def correlation_test(df, col1, col2, method="pearson", save_path=None):
    x = df[col1].dropna()
    y = df[col2].dropna()
    idx = x.index.intersection(y.index)
    x, y = x.loc[idx], y.loc[idx]
    if method == "pearson":
        stat, p = pearsonr(x, y)
        desc = "linear"
    else:
        stat, p = spearmanr(x, y)
        desc = "monotonic"
    if p < 0.05:
        verdict = "Reject H₀"
        interpretation = f"No significant {desc} relationship between {col1} and {col2} (p={p:.4f})"
    else:
        verdict = "Fail to Reject H₀"
        interpretation = f"There is significant {desc} relationship between {col1} and {col2} (p={p:.4f})"
    rel_path = None
    if save_path:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=x, y=y)
        plt.title(f"{col1} vs {col2} ({method.title()} Correlation)")
        save_plot_if_needed(save_path)
        plt.close()
        rel_path = os.path.relpath(save_path, os.path.join(BASE_DIR, "results"))
    return stat, p, verdict, interpretation, rel_path




 




