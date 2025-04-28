import os
from datetime import datetime
from fpdf import FPDF
from datetime import datetime


def create_assets(insight_text):
    print("[Asset Generator] Creating assets (TXT and PDF)...")

    # Check if the directory exists before proceeding
    if not os.path.exists('assets/products'):
        print("[ERROR] Directory 'assets/products' does not exist.")
    else:
        print("[INFO] Directory 'assets/products' exists.")

    os.makedirs('assets/products', exist_ok=True)  # Ensures directory exists or creates it

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base_filename = f'product_{timestamp}'
    txt_path = f'assets/products/{base_filename}.txt'
    pdf_path = f'assets/products/{base_filename}.pdf'

    # Save TXT
    with open(txt_path, 'w') as f:
        f.write(insight_text)

    # Save PDF
    pdf = FPDF(encoding="utf-8")
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in insight_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(pdf_path)

    print(f"[Asset Generator] Saved TXT: {txt_path}")
    print(f"[Asset Generator] Saved PDF: {pdf_path}")
    
    return txt_path, pdf_path
