from flask import Flask, send_file, jsonify
from core.chaos_crawler import collect_chaos
from core.gpt_processor import generate_insights
from core.asset_generator import create_assets
from core.ebook_writer import write_ebook
from core.toolkit_generator import generate_toolkit
from core.upload_summary import generate_upload_summary
from core.deployer import save_log, create_zip_bundle
from core.product_type_decider import decide_product_type
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

    # Step 1: Collect chaos input
    chaos_data = collect_chaos()

    # Step 2: Generate product insight
    insights = generate_insights(chaos_data)

    # Step 3: Generate TXT & short PDF
    txt_path, pdf_path = create_assets(insights)

    # Step 4: Decide product type (ebook, toolkit, both)
    product_type = decide_product_type()
    print(f"[Decision] Product type: {product_type}")

    ebook_path = None
    toolkit_paths = []
    summary_path = None

    # Step 5: Optional eBook
    if product_type in ["ebook", "both"]:
        ebook_path = write_ebook(insights)

    # Step 6: Optional Toolkit
    if product_type in ["toolkit", "both"]:
        toolkit_paths = generate_toolkit(insights)

    # Step 7: Summary file for upload
    title_line = next((line for line in insights.splitlines() if line.startswith("Title:")), "")
    title = title_line.replace("Title:", "").strip().strip('\"')
    description_line = next((line for line in insights.splitlines() if line.startswith("Description:")), "")
    description = description_line.replace("Description:", "").strip()
    summary_path = generate_upload_summary(title, description)

    # Step 8: Bundle everything
    zip_path = create_zip_bundle(txt_path, pdf_path, insights, ebook_path, toolkit_paths, summary_path)

    # Step 9: Log it
    save_log(chaos_data, insights, txt_path, pdf_path, zip_path)

    # Step 10: Update runtime status
    elapsed = round(time.time() - start, 2)
    set_status("idle", f"{elapsed}s")
    print(f"[TIMER] ✅ Full run completed in {elapsed}s")

    return "✅ Blackmirror: Full Product Generated Successfully."


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
