from flask import Flask, send_file, jsonify
from core.chaos_crawler import collect_chaos
from core.gpt_processor import generate_insights
from core.asset_generator import create_assets
from core.deployer import save_log, create_zip_bundle
from utils.models_fallback import FREE_MODELS
import os
import subprocess  
import datetime


app = Flask(__name__)

import time

@app.route("/")
def run_blackmirror():
    start_time = time.time()
    print("[INFO] Starting generation...")

    t0 = time.time()
    chaos_data = collect_chaos()
    t1 = time.time()
    print(f"[TIMER] Chaos collected in {t1 - t0:.2f}s")

    t2 = time.time()
    insights = generate_insights(chaos_data)
    t3 = time.time()
    print(f"[TIMER] GPT processing in {t3 - t2:.2f}s")

    t4 = time.time()
    txt_path, pdf_path = create_assets(insights)
    t5 = time.time()
    print(f"[TIMER] Asset creation in {t5 - t4:.2f}s")

    zip_path = create_zip_bundle(txt_path, pdf_path, insights)
    t6 = time.time()
    print(f"[TIMER] ZIP creation in {t6 - t5:.2f}s")

    save_log(chaos_data, insights, txt_path, pdf_path, zip_path)
    total_time = time.time() - start_time
    print(f"[TIMER] ✅ Full run completed in {total_time:.2f}s")

    return "Blackmirror: New Product Generated Successfully."


@app.route("/download/latest")
def download_latest_zip():
    zip_folder = "assets/products/"
    zips = [f for f in os.listdir(zip_folder) if f.endswith('.zip')]
    if not zips:
        return "No ZIP file found."
    latest_zip = sorted(zips)[-1]
    return send_file(os.path.join(zip_folder, latest_zip), as_attachment=True)

@app.route("/download/all")
def download_all_zips():
    zip_folder = "assets/products/"
    all_zip_files = [f for f in os.listdir(zip_folder) if f.endswith('.zip')]

    if not all_zip_files:
        return "No ZIP files found to bundle."

    temp_bundle = os.path.join(zip_folder, "all_products_bundle.zip")

    # Create a new bundle of all zip files
    import zipfile
    with zipfile.ZipFile(temp_bundle, 'w') as bundle:
        for zip_name in all_zip_files:
            bundle.write(os.path.join(zip_folder, zip_name), arcname=zip_name)

    return send_file(temp_bundle, as_attachment=True)


@app.route("/health")
def health_check():
    try:
        # Run the health check script and capture the output
        result = subprocess.run(["python", "health_check.py"], check=True, capture_output=True, text=True)
        print(result.stdout)  # Print the output of the health check
        return jsonify({"status": "OK", "message": "All models are functioning properly."})
    except subprocess.CalledProcessError as e:
        print(f"Health check failed with error: {e.stderr.decode()}")  # Print the error if it fails
        return jsonify({"status": "FAIL", "message": "Health check failed", "details": e.stderr.decode()}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)  # Set debug=True


# Global runtime tracker
generation_status = {"status": "idle", "last_runtime": None}

@app.route("/status")
def get_status():
    return jsonify(generation_status)
