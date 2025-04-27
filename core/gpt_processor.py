from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
    api_key=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,
    base_url="https://openrouter.ai/api/v1"
)

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

    chat_completion = client.chat.completions.create(
        model="mistralai/mixtral-8x7b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chaos_text}
        ]
    )

    idea = chat_completion.choices[0].message.content
    return idea
