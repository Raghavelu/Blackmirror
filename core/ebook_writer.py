from fpdf import FPDF
from core.deployer import extract_title
import os

def write_ebook(insight_text):
    print("[eBook Writer] Generating full eBook PDF...")

    title = extract_title(insight_text)
    filename = f"assets/products/{title}_ebook.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    lines = insight_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(8)
        else:
            try:
                pdf.multi_cell(0, 10, line)
            except Exception as e:
                print(f"[PDF ERROR] Could not render line: {line} — {e}")

    pdf.output(filename)
    print(f"[eBook Writer] eBook saved to {filename}")
    return filename
