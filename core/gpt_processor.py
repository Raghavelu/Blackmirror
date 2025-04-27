from config import OPENROUTER_API_KEY
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    },
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
