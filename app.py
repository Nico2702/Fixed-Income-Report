import os
from flask import Flask, send_from_directory, render_template_string, abort

app = Flask(__name__)

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NaroIX Report Library</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: Inter, Segoe UI, Arial, sans-serif;
            background: #f7f8fc;
            color: #1f2a44;
            padding: 48px 24px;
        }
        .container { max-width: 860px; margin: 0 auto; }
        h1 { font-size: 28px; margin-bottom: 6px; }
        .subtitle { color: #5A73D8; font-weight: 600; font-size: 15px; margin-bottom: 32px; }
        .report-list { display: flex; flex-direction: column; gap: 12px; }
        .report-card {
            background: white;
            border: 1px solid #C2C2C2;
            border-radius: 14px;
            padding: 18px 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 16px rgba(15,23,42,0.05);
            transition: box-shadow 0.15s;
        }
        .report-card:hover { box-shadow: 0 6px 24px rgba(15,23,42,0.10); }
        .report-name { font-weight: 600; font-size: 15px; }
        .report-meta { font-size: 13px; color: #6b7a99; margin-top: 3px; }
        .btn {
            background: #5A73D8;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 18px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            white-space: nowrap;
        }
        .btn:hover { background: #4C61BF; }
        .empty { color: #6b7a99; font-size: 15px; margin-top: 24px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>NaroIX Report Library</h1>
        <div class="subtitle">Index Backtest Reports</div>
        <div class="report-list">
            {% if reports %}
                {% for r in reports %}
                <div class="report-card">
                    <div>
                        <div class="report-name">{{ r.display }}</div>
                        <div class="report-meta">{{ r.filename }}</div>
                    </div>
                    <a class="btn" href="/reports/{{ r.filename }}" target="_blank">Open Report</a>
                </div>
                {% endfor %}
            {% else %}
                <div class="empty">No reports found. Add HTML files to the <code>reports/</code> folder.</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

def get_display_name(filename):
    """Convert filename to readable display name."""
    name = filename.replace(".html", "").replace("_", " ").replace("-", " ")
    return name.title()


@app.route("/")
def index():
    reports = []
    if os.path.isdir(REPORTS_DIR):
        for f in sorted(os.listdir(REPORTS_DIR)):
            if f.endswith(".html"):
                reports.append({
                    "filename": f,
                    "display": get_display_name(f),
                })
    return render_template_string(INDEX_TEMPLATE, reports=reports)


@app.route("/reports/<path:filename>")
def serve_report(filename):
    if not filename.endswith(".html"):
        abort(404)
    return send_from_directory(REPORTS_DIR, filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
