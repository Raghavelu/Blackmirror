from fpdf import FPDF
from core.deployer import extract_title
import os


def generate_toolkit(insight_text):
    print("[Toolkit Generator] Creating checklist + worksheet...")

    title = extract_title(insight_text)
    base = f"assets/products/{title}"

    checklist_path = f"{base}_checklist.txt"
    with open(checklist_path, 'w') as f:
        f.write("Checklist:\n")
        f.write("- [ ] Validate customer pain points\n")
        f.write("- [ ] Create MVP\n")
        f.write("- [ ] Interview users\n")
        f.write("- [ ] Measure fit and traction\n")

    worksheet_path = f"{base}_worksheet.csv"
    with open(worksheet_path, 'w') as f:
        f.write("Metric,Value\n")
        f.write("Customer Interviews,\n")
        f.write("Trial Signups,\n")
        f.write("Conversion Rate,\n")

    print("[Toolkit Generator] Toolkit assets created.")
    return [checklist_path, worksheet_path]
