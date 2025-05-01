import os
import re
from core.deployer import extract_title

def generate_toolkit(insight_text):
    print("[Toolkit Generator] Creating practical resources...")
    
    title = extract_title(insight_text)
    base_path = f"assets/products/{title}_toolkit"
    os.makedirs(base_path, exist_ok=True)
    
    # Dynamic checklist based on content
    checklist_path = f"{base_path}/implementation_checklist.md"
    with open(checklist_path, 'w') as f:
        f.write("# Implementation Checklist\n\n")
        steps = re.findall(r'- (.+?)\n', insight_text)
        for idx, step in enumerate(steps[:10], 1):
            f.write(f"{idx}. [ ] {step}\n")
    
    # Worksheet
    worksheet_path = f"{base_path}/progress_worksheet.csv"
    with open(worksheet_path, 'w') as f:
        f.write("Week,Milestone,Completed\n")
        for week in range(1, 13):
            f.write(f"Week {week},,\n")
    
    print(f"[Toolkit Generator] Created toolkit at {base_path}")
    return [checklist_path, worksheet_path]
