from fpdf import FPDF
from core.deployer import extract_title
import os

def generate_upload_summary(title, description, price="$19"):
    print("[Uploader] Creating upload summary...")
    base = f"assets/products/{title}_summary.txt"
    with open(base, 'w') as f:
        f.write(f"Title: {title}\n")
        f.write(f"Description: {description.strip()}\n")
        f.write(f"Tags: startup, business, product-market fit\n")
        f.write(f"Price: {price}\n")
    return base
