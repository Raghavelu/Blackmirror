from flask import Flask, send_file, jsonify
from core.chaos_crawler import collect_chaos
from core.gpt_processor import generate_insights
from core.asset_generator import create_assets
from core.deployer import save_log, create_zip_bundle
from utils.models_fallback import FREE_MODELS
import os
import subprocess  

app = Flask(__name__)

@app.route("/")
def run_blackmirror():
    chaos_data = collect_chaos()
    insights = generate_insights(chaos_data)
    txt_path, pdf_path = create_assets(insights)
    create_zip_bundle(txt_path, pdf_path, datetime.now().strftime("%Y%m%d%H%M%S")) 
    save_log(chaos_data, insights, txt_path, pdf_path)
    return "Blackmirror: New Product Generated Successfully."

@app.route("/download/latest")
def download_latest_zip():
    zip_folder = "assets/products/"
    zips = [f for f in os.listdir(zip_folder) if f.endswith('.zip')]
    if not zips:
        return "No ZIP file found."
    latest_zip = sorted(zips)[-1]
    return send_file(os.path.join(zip_folder, latest_zip), as_attachment=True)

@app.route("/health")
def health_check():
    # Run the health check script as a subprocess
    try:
        subprocess.run(["python", "health_check.py"], check=True, capture_output=True)
        return jsonify({"status": "OK", "message": "All models are functioning properly."})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "FAIL", "message": "Health check failed", "details": e.stderr.decode()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
