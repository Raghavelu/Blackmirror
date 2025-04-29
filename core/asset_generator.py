import os
from datetime import datetime
from fpdf import FPDF
import textwrap


def create_assets(insight_text):
    print("[Asset Generator] Creating assets (TXT and PDF)...")

    # Ensure output folder exists
    os.makedirs('assets/products', exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base_filename = f'product_{timestamp}'
    txt_path = f'assets/products/{base_filename}.txt'
    pdf_path = f'assets/products/{base_filename}.pdf'

    # Save as TXT
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(insight_text)

    # Save as PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Wrap long lines safely for PDF rendering
    for line in insight_text.split("\n"):
        line = line.strip()
        if not line:
            pdf.ln(10)
            continue
        wrapped = textwrap.wrap(line, width=90)  # wrap to max 90 characters per line
        for wline in wrapped:
            try:
                pdf.multi_cell(0, 10, wline)
            except Exception as e:
                print(f"[PDF ERROR] Could not render line: {wline[:50]}... — {e}")

    pdf.output(pdf_path)
    print(f"[Asset Generator] Saved TXT: {txt_path}")
    print(f"[Asset Generator] Saved PDF: {pdf_path}")

    return txt_path, pdf_path
