from utils.models_fallback import smart_generate
from core.utils import sanitize_text

def validate_insights(insights):
    required = {'Title', 'Description', 'Target Audience', 'Key Benefits', 'Format'}
    return all(f"{section}:" in insights for section in required)

def generate_insights(chaos_text):
    print("[GPT Processor] Generating product concept...")
    
    system_prompt = """Create a complete digital product specification. STRICT FORMAT:
Title: [Product Name]
Description: [2-3 paragraph overview]
Target Audience: [Specific demographic]
Key Benefits: 
- Benefit 1
- Benefit 2 
Core Features:
- Feature 1
- Feature 2
Format: [eBook/Video Course/Toolkit]
Recommended Price: [$X-X range]"""

    for _ in range(3):
        insights = smart_generate(system_prompt, chaos_text)
        if validate_insights(insights):
            return sanitize_text(insights)
        print("[GPT Processor] Retrying...")
    
    raise ValueError("Failed to generate valid insights after 3 attempts")
