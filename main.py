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
        # Generation pipeline
        chaos = collect_chaos()
        insights = generate_insights(chaos)
        txt_path = create_assets(insights)
        ebook_path = write_ebook(insights)
        product_type = decide_product_type()
        toolkit_paths = generate_toolkit(insights) if product_type == "both" else []
        summary_path = generate_upload_summary(insights)
        zip_path = create_zip_bundle(txt_path, ebook_path, toolkit_paths, summary_path)
        
        # Logging and response
        save_log(chaos, insights, txt_path, zip_path, ebook_path, toolkit_paths)
        elapsed = time.time() - start_time
        set_status("idle", f"{elapsed:.1f}s")
        
        return jsonify({
            "status": "success",
            "bundle": os.path.basename(zip_path),
            "pages": open(ebook_path).read().count('\x0c')  # Count PDF pages
        })
    
    except Exception as e:
        set_status("error")
        print(f"CRITICAL ERROR: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Generation failed",
            "error": str(e)[:100]
        }), 500

# ... keep other routes the same ...

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
