from utils.models_fallback import smart_generate
from utils.utils import sanitize_text

def validate_insights(insights):
    required = {'Title', 'Description', 'Target Audience', 'Key Benefits', 'Format'}
    return all(f"{section}:" in insights for section in required)

def generate_insights(chaos_text):
    print("[GPT Processor] Generating product concept...")
    
    system_prompt = """Create a complete digital product specification from the given problem. STRICT FORMAT:
    
Title: [Catchy Product Name]
Description: [2-3 paragraph overview]
Target Audience: [Specific demographic/psychographic]
Key Benefits: 
- Benefit 1
- Benefit 2 
- Benefit 3
Core Features:
- Feature 1
- Feature 2
Format: [eBook/Video Course/Toolkit Bundle]
Recommended Price: [$X-X range]"""

    insights = smart_generate(system_prompt, chaos_text)
    return sanitize_text(insights)

    for _ in range(3):  # Retry up to 3 times
        insights = smart_generate(system_prompt, chaos_text)
        if validate_insights(insights):
            return insights
        print("[GPT Processor] Retrying due to invalid format...")
    
    raise ValueError("Failed to generate properly formatted insights after 3 attempts")
