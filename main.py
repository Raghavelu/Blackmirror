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
import time

app = Flask(__name__)

@app.route("/")
def run_blackmirror():
    start_time = time.time()
    set_status("running")
    
    try:
        # 1. Identify Core Problem
        chaos = collect_chaos()
        
        # 2. Generate Product Concept
        insights = generate_insights(chaos)
        
        # 3. Create Base Assets
        txt_path = create_assets(insights)
        
        # 4. Generate Expanded eBook
        ebook_path = write_ebook(insights)
        
        # 5. Conditionally Create Toolkit
        product_type = decide_product_type()
        toolkit_paths = generate_toolkit(insights) if product_type == "both" else []
        
        # 6. Create Platform Summary
        summary_path = generate_upload_summary(insights)
        
        # 7. Bundle Assets
        zip_path = create_zip_bundle(txt_path, ebook_path, toolkit_paths, summary_path)
        
        # 8. Log Generation
        save_log(chaos, insights, txt_path, zip_path, ebook_path, toolkit_paths)
        
        # 9. Finalize
        elapsed = time.time() - start_time
        set_status("idle", f"{elapsed:.1f}s")
        return jsonify({
            "status": "success",
            "bundle": zip_path,
            "components": {
                "ebook": os.path.basename(ebook_path),
                "toolkit": [os.path.basename(p) for p in toolkit_paths]
            }
        })
    
    except Exception as e:
        set_status("error")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/download/latest")
def download_latest():
    zips = sorted([
        f for f in os.listdir('assets/products') 
        if f.endswith('.zip')
    ], key=lambda x: os.path.getctime(os.path.join('assets/products', x)))
    
    if not zips:
        return jsonify({"error": "No bundles available"}), 404
    
    latest = zips[-1]
    return send_file(
        os.path.join('assets/products', latest),
        as_attachment=True,
        download_name=f"blackmirror_{latest}"
    )

@app.route("/status")
def status():
    return jsonify(get_status())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
