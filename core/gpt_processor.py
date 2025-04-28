from utils.models_fallback import smart_generate

def generate_insights(chaos_text):
    print("[GPT Processor] Generating product idea...")

    system_prompt = (
        "You are an expert product creator. Given a chaotic problem, output a FULL product ready to sell. "
        "Format:\n\n"
        "Title: <Title>\n"
        "Description: <Description>\n"
        "Target Audience: <Audience>\n"
        "Key Benefits: <Benefits>\n"
        "Format: <eBook, Guide, Course, etc.>"
    )

    # Call the smart fallback function
    idea = smart_generate(system_prompt, chaos_text)

    return idea
