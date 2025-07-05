import os
import sys
from flask import Flask, request, render_template, send_file, redirect, url_for, send_from_directory
import pandas as pd
from werkzeug.utils import secure_filename

# ---- Path Config ----
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Add src to path
sys.path.append(BASE_DIR)

# ---- Internal Imports ----
from src.test_runner import run_tests_from_config

RESULT_PATH = os.path.join(BASE_DIR, 'results', 'report.html')
uploaded_data = {}

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        file = request.files.get("csv_file")
        if not file:
            error = "Missing file"
        else:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                df = pd.read_csv(filepath)
                uploaded_data['df'] = df
                uploaded_data['df_preview'] = df.head().to_html(classes="preview-table", index=False)
                return redirect(url_for("select_test"))
            except Exception as e:
                error = f"Error reading CSV: {e}"
    return render_template("index.html", error=error, df_html=uploaded_data.get('df_preview'))

@app.route("/select-test", methods=["GET", "POST"])
def select_test():
    df = uploaded_data.get("df")
    df_preview = uploaded_data.get("df_preview")
    error = None

    if df is None:
        return redirect(url_for("index"))

    # Extract columns
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    num_cols = df.select_dtypes(include="number").columns.tolist()
    binary_cols = [col for col in cat_cols if df[col].nunique() == 2]

    if request.method == "POST":
        test_type = request.form.get("test_type")
        config = []

        if test_type == "chi2":
            col1 = request.form.get("col1")
            col2 = request.form.get("col2")
            if not col1 or not col2:
                error = "Please select both categorical columns for Chi-square test."
            else:
                config = [{
                    "type": "chi2",
                    "col1": col1,
                    "col2": col2,
                    "hypothesis": f"There is an association between {col1} and {col2}"
                }]

        elif test_type == "ttest":
            num_col = request.form.get("num_col")
            cat_col = request.form.get("cat_col")
            if not num_col or not cat_col:
                error = "Please select both a numerical and a binary categorical column for T-test."
            elif df[cat_col].nunique() != 2:
                error = "Selected categorical column must have exactly two unique values for T-test."
            else:
                config = [{
                    "type": "ttest",
                    "num": num_col,
                    "cat": cat_col,
                    "hypothesis": f"Mean of {num_col} is different across {cat_col}"
                }]

        elif test_type == "correlation":
            corr1 = request.form.get("corr1")
            corr2 = request.form.get("corr2")
            method = request.form.get("method", "pearson")
            if not corr1 or not corr2:
                error = "Please select two numerical columns for correlation."
            else:
                config = [{
                    "type": "correlation",
                    "col1": corr1,
                    "col2": corr2,
                    "method": method,
                    "hypothesis": f"{corr1} is correlated with {corr2}"
                }]
        else:
            error = "Please select a test type."

        if config and not error:
            run_tests_from_config(df, config)
            return redirect(url_for("view_report"))

    return render_template("select_test.html",
                          df_html=df_preview,
                          cat_cols=cat_cols,
                          num_cols=num_cols,
                          binary_cols=binary_cols,
                          error=error)

@app.route('/plots/<path:filename>')
def serve_plot(filename):
    return send_from_directory(os.path.join('results', 'plots'), filename)

@app.route("/report")
def view_report():
    return send_file(RESULT_PATH)

@app.route("/download")
def download_report():
    return send_file(RESULT_PATH, as_attachment=True, download_name="report.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5050)


