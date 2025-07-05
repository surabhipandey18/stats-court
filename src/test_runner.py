import sys
import os
import numpy as np

# Ensure src modules can be found
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from src.hypothesis_tests import categorical_associations, t_test, correlation_test
from src.report_generator import append_to_report_html, initialize_report_html, insert_summary_table
from src.utils import save_plot_if_needed, RESULT_PATH

# Determine base and plot directories
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))

PLOT_PATH = os.path.join(BASE_DIR, "results", "plots")
os.makedirs(PLOT_PATH, exist_ok=True)  # Ensure plot directory exists

def run_tests_from_config(df, config_list):
    """
    Runs statistical tests on the DataFrame `df` according to `config_list` instructions.
    Generates plots, appends results to an HTML report, and inserts a summary table.
    """
    initialize_report_html()
    summaries = []

    for test in config_list:
        print(f"Running test: {test}")
        try:
            test_type = test.get("type")
            if not test_type:
                print("Test config missing 'type'. Skipping.")
                continue

            # --- Chi-square Test ---
            if test_type == "chi2":
                col1 = test.get("col1")
                col2 = test.get("col2")
                if not col1 or not col2:
                    print("Chi2 test config missing columns. Skipping.")
                    continue
                filename = f"chi2_{col1}_vs_{col2}.png".replace(" ", "_")
                full_plot_path = os.path.join(PLOT_PATH, filename)
                stat, p, verdict, interpretation, _ = categorical_associations(
                    df, col1, col2, return_all=True, save_path=full_plot_path
                )
                append_to_report_html(
                    hypothesis=f"There is an association between {col1} and {col2}",
                    test_name="Chi-square Test",
                    stat=stat, p_value=p, conclusion=verdict,
                    interpretation=interpretation, plot_path=full_plot_path
                )
                print(f"✅ chi2 test report appended")
                summaries.append({
                    "Hypothesis": f"There is an association between {col1} and {col2}",
                    "Test": "Chi-square",
                    "p-value": p,
                    "Verdict": verdict
                })

            # --- T-test ---
            elif test_type == "ttest":
                num_col = test.get("num")
                cat_col = test.get("cat")
                if not num_col or not cat_col:
                    print("T-test config missing columns. Skipping.")
                    continue
                filename = f"ttest_{num_col}_by_{cat_col}.png".replace(" ", "_")
                full_plot_path = os.path.join(PLOT_PATH, filename)
                stat, p, verdict, interpretation, _ = t_test(
                    df, cat_col, num_col, return_all=True, save_path=full_plot_path
                )
                append_to_report_html(
                    hypothesis=f"There is a difference in the mean of {num_col} across {cat_col}",
                    test_name="T-test",
                    stat=stat, p_value=p, conclusion=verdict,
                    interpretation=interpretation, plot_path=full_plot_path
                )
                print(f"✅ ttest report appended")
                summaries.append({
                    "Hypothesis": f"There is a difference in the mean of {num_col} across {cat_col}",
                    "Test": "T-test",
                    "p-value": p,
                    "Verdict": verdict
                })

            # --- Correlation Test ---
            elif test_type == "correlation":
                col1 = test.get("col1")
                col2 = test.get("col2")
                method = test.get("method", "pearson")
                if not col1 or not col2:
                    print("Correlation test config missing columns. Skipping.")
                    continue
                filename = f"correlation_{col1}_vs_{col2}_{method}.png".replace(" ", "_")
                full_plot_path = os.path.join(PLOT_PATH, filename)
                stat, p, verdict, interpretation, _ = correlation_test(
                    df, col1, col2, method=method, save_path=full_plot_path
                )
                append_to_report_html(
                    hypothesis=f"There is a correlation between {col1} and {col2}",
                    test_name=f"{method.title()} Correlation",
                    stat=stat, p_value=p, conclusion=verdict,
                    interpretation=interpretation, plot_path=full_plot_path
                )
                print(f"✅ correlation test report appended")
                summaries.append({
                    "Hypothesis": f"There is a correlation between {col1} and {col2}",
                    "Test": f"{method.title()} Correlation",
                    "p-value": p,
                    "Verdict": verdict
                })
            else:
                print(f"Unknown test type '{test_type}'. Skipping.")

        except Exception as e:
            print(f"Error in test {test}:\n   {e}")

    insert_summary_table(summaries)










