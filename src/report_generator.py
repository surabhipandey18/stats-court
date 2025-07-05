import os
import html

# Get project root
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))

REPORT_PATH = os.path.join(BASE_DIR, "results", "report.html")

def initialize_report_html(file_path=REPORT_PATH):
    """
    Initializes a new HTML report file with header and styles.
    """
    html_header = """
    <html>
    <head>
        <title>Stats Court Report</title>
        <link href="https://fonts.googleapis.com/css?family=Inter:400,600,700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
                background: #181c24;
                color: #f4f6fb;
                margin: 0;
                padding: 0;
            }
            .header {
                background: #232a36;
                color: #4f8cff;
                padding: 24px 0;
                text-align: center;
                font-size: 2.2rem;
                font-weight: 700;
                letter-spacing: 2px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            }
            h1, h2, h3 {
                color: #4f8cff;
                font-weight: 700;
                margin-bottom: 18px;
                font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
            }
            .report-block {
                background: #232a36;
                border-left: 6px solid #4f8cff;
                padding: 20px 28px;
                margin: 32px auto;
                box-shadow: 0 4px 24px rgba(0,0,0,0.18);
                border-radius: 12px;
                max-width: 700px;
            }
            .label {
                font-weight: bold;
                color: #b0b8c1;
            }
            table {
                width: 90%;
                margin: 32px auto 24px auto;
                border-collapse: collapse;
                background: #232a36;
                color: #f4f6fb;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            }
            th, td {
                border: 1px solid #2c3440;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #232a36;
                color: #4f8cff;
            }
            tr:nth-child(even) {
                background-color: #181c24;
            }
            img {
                max-width: 100%;
                margin-top: 18px;
                border: 1px solid #2c3440;
                border-radius: 8px;
                background: #fff;
            }
            hr {
                border: 0;
                border-top: 1px solid #2c3440;
                margin: 36px 0;
            }
        </style>
    </head>
    <footer class="footer">
    <span>&copy; 2025 Made with ❤️ by Surabhi Pandey</span>
    </footer>
    <body>
        <div class="header">Stats Court Report</div>
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_header)
    print(f"Initialized new report at: {file_path}")

def append_to_report_html(
    hypothesis,
    test_name,
    stat,
    p_value,
    conclusion,
    interpretation,
    plot_path=None,
    file_path=REPORT_PATH
):
    """
    Appends a test result block to the HTML report.
    """
    def fmt(value):
        return f"{value:.4f}" if isinstance(value, (float, int)) else str(value)

    # Escape HTML for safety
    hypothesis = html.escape(hypothesis)
    test_name = html.escape(test_name)
    conclusion = html.escape(conclusion)
    interpretation = html.escape(interpretation)

    html_block = f"""
    <div class="report-block">
        <p><span class="label">Hypothesis:</span> <strong>{hypothesis}</strong></p>
        <p><span class="label">Test Used:</span> {test_name}</p>
        <p><span class="label">Test Statistic:</span> {fmt(stat)}</p>
        <p><span class="label">p-value:</span> {fmt(p_value)}</p>
        <p><span class="label">Conclusion:</span> <strong>{conclusion}</strong></p>
        <p><span class="label">Interpretation:</span> {interpretation}</p>
    """

    if plot_path:
        filename = os.path.basename(plot_path)
        html_block += f"""
        <img src="/plots/{filename}" alt="plot" />
        """

    html_block += "</div>\n"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(html_block)

    print("📎 Appended new test with plot to report.")

def insert_summary_table(test_summaries, file_path=REPORT_PATH):
    """
    Inserts a summary table at the top of the HTML report (after <body>).
    Optionally closes the HTML document.
    """
    table_html = """
    <h2>Summary of Tests</h2>
    <table>
        <tr>
            <th>Hypothesis</th>
            <th>Test</th>
            <th>p-value</th>
            <th>Verdict</th>
        </tr>
    """
    for test in test_summaries:
        p_val = f"{test['p-value']:.4f}" if isinstance(test['p-value'], (float, int)) else "-"
        table_html += f"""
        <tr>
            <td>{html.escape(str(test['Hypothesis']))}</td>
            <td>{html.escape(str(test['Test']))}</td>
            <td>{p_val}</td>
            <td><strong>{html.escape(str(test['Verdict']))}</strong></td>
        </tr>
        """
    table_html += "</table><hr/>"

    # Inject summary after <body>
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("Report file not found. Initializing new report.")
        initialize_report_html(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    updated_content = content.replace("<body>", "<body>\n" + table_html, 1)

    # Optionally add closing tags if not present
    if not updated_content.strip().endswith("</body>\n</html>") and not updated_content.strip().endswith("</body></html>"):
        updated_content += "\n</body>\n</html>"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("Summary table added to top of report.")


