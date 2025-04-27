from core.chaos_crawler import collect_chaos
from core.gpt_processor import generate_insights
from core.asset_generator import create_assets
from core.deployer import save_log

def main():
    chaos_data = collect_chaos()
    insights = generate_insights(chaos_data)
    txt_path, pdf_path = create_assets(insights)
    save_log(chaos_data, insights, txt_path, pdf_path)

if __name__ == "__main__":
    main()
