# Stats Court

Stats Court is a modern, user-friendly web application for statistical analysis and automated report generation. Upload your data, select statistical tests, and get beautiful, downloadable HTML reports — all in a stylish dark theme.

---

## Features

- CSV Upload: Upload your dataset and preview it instantly.
- Test Selection: Choose from Chi-square, T-test, and Correlation tests.
- Smart Column Detection: Only valid columns are shown for each test.
- Automated Reporting: Generates a professional HTML report with summary tables and results.
- Modern Dark Theme: Clean, responsive UI with Inter font.
- Authorship Footer: Your name and copyright.
- Shareable: Deployed on Render for easy access and sharing.

---

## 🔗 Live Demo

Try the live app:  
https://statscourtroom.onrender.com/

---

## Getting Started

### 1. Clone the Repository

    git clone https://github.com/your-username/stats-court.git
    cd stats-court

### 2. Install Dependencies

    pip install -r requirements.txt

### 3. Run Locally

    python app.py

Visit http://localhost:5050 in your browser.

---

## Deployment (Render)

1. Push your code to GitHub.
2. Create a new Web Service on https://render.com/
3. Set:
   - Build Command:  
     pip install -r requirements.txt
   - Start Command:  
     gunicorn app:app --bind 0.0.0.0:$PORT
4. Deploy and share your public URL:  
   https://statscourtroom.onrender.com/

---

## Project Structure

    stats-court/
    ├── app.py                  # Main Flask app
    ├── requirements.txt        # Dependencies
    ├── templates/              # HTML templates
    ├── static/                 # CSS, JS, etc.
    ├── uploads/                # Uploaded files
    ├── results/                # Generated reports
    └── README.md               # Project documentation



