from flask import Flask, send_file, jsonify
from core.chaos_crawler import collect_chaos
from core.gpt_processor import generate_insights
from core.asset_generator import create_assets
from core.deployer import save_log, create_zip_bundle
from utils.status_tracker import set_status, get_status
import os
import subprocess
import time
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def run_blackmirror():
    start = time.time()
    set_status("running")
    print("[INFO] Starting generation...")

    # Step 1: Collect chaos
    chaos_data = collect_chaos()
    print(f"[INFO] Chaos collected: {chaos_data}")
    
    # Step 2: Generate insight
    insights = generate_insights(chaos_data)
    print(f"[INFO] GPT returned insights:\n{insights}")

    # Step 3: Create assets
    txt_path, pdf_path = create_assets(insights)
    print(f"[INFO] Assets created: TXT = {txt_path}, PDF = {pdf_path}")

    # Step 4: Create ZIP
    zip_path = create_zip_bundle(txt_path, pdf_path, insights)
    print(f"[INFO] ZIP bundle created: {zip_path}")

    # Step 5: Save log
    save_log(chaos_data, insights, txt_path, pdf_path, zip_path)

    # Finalize status
    elapsed = round(time.time() - start, 2)
    set_status("idle", f"{elapsed}s")
    print(f"[TIMER] ✅ Full run completed in {elapsed}s")

    return "✅ Blackmirror: Product Generated Successfully."


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
    try:
        result = subprocess.run(["python", "health_check.py"], check=True, capture_output=True, text=True)
        print(result.stdout)
        return jsonify({"status": "OK", "message": "All models working."})
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Health check failed:\n{e.stderr}")
        return jsonify({"status": "FAIL", "details": e.stderr}), 500


@app.route("/status")
def status():
    return jsonify(get_status())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
