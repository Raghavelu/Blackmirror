import os
import re
import textwrap
from datetime import datetime
from fpdf import FPDF
from core.deployer import extract_title


def clean_line(line):
    # Remove markdown formatting that causes rendering issues
    line = re.sub(r'\*\*|__|\*|`|~|>|#+', '', line)         # remove bold/italic/code/headers
    line = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 (URL)', line) # convert markdown links
    line = line.replace('\u200b', '')  # zero-width space
    line = re.sub(r'[^\x00-\x7F]+', ' ', line)  # strip problematic unicode
    return line.strip()


def create_assets(insight_text):
    print("[Asset Generator] Creating assets (TXT and PDF)...")

    # Ensure folder exists
    os.makedirs('assets/products', exist_ok=True)

    base_filename = extract_title(insight_text)
    txt_path = f'assets/products/{base_filename}.txt'
    pdf_path = f'assets/products/{base_filename}.pdf'


    # Save TXT
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(insight_text)

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for raw_line in insight_text.split("\n"):
        cleaned = clean_line(raw_line)

        if not cleaned:
            pdf.ln(8)
            continue

        wrapped = textwrap.wrap(cleaned, width=80)
        for wline in wrapped:
            try:
                pdf.cell(0, 10, wline, ln=True)
            except Exception as e:
                print(f"[PDF ERROR] Skipped bad line: {wline[:50]} — {e}")

    pdf.output(pdf_path)
    print(f"[Asset Generator] Saved TXT: {txt_path}")
    print(f"[Asset Generator] Saved PDF: {pdf_path}")

    return txt_path, pdf_path
