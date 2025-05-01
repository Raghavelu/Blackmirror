# Blackmirror
**Blackmirror** is a zero-cost, AI-powered automation system that turns chaotic real-world problems into full digital products (eBooks, toolkits, summaries) — ready to upload and sell.

---

## ⚙️ How It Works

1. Picks a real-world "chaotic" pain point.
2. Uses OpenRouter (free LLMs) to generate insights.
3. Automatically builds:
   - TXT + PDF pitch
   - Full eBook (optional)
   - Toolkit: checklist + worksheet (optional)
   - Gumroad-ready summary file
4. Packages everything into a downloadable `.zip`.

---

## 🔑 Key Features

- Chaos-to-product in one click
- Free OpenRouter LLMs (no API cost)
- Multiple output formats
- Ready for Gumroad upload
- Fully self-hosted (Railway, Fly.io)

---

## Project Structure
Blackmirror/       
├── assets/products/ # Final ZIPs + PDFs         
├── core/ # Generators + logic       
  ├── asset_generator.py            
  ├── chaos_crawler.py               
  ├── deployer.py               
  ├── gpt_processor.py            
  ├── ebook_writer.py            
  ├── toolkit_generator.py            
  ├── upload_summary.py               
  └── product_type_decider.py            
├── data/chaos_logs.json            
├── storage/status.json, model_usage.log            
├── utils/models_fallback.py, status_tracker.py            
├── main.py            
├── config.py         
├── health_check.py         
├── requirements.txt            
├── Procfile            
└── README.md


---

## 🚀 API Endpoints

| Method | Route              | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/`                | Generate a new product bundle        |
| GET    | `/download/latest` | Download the most recent .zip file   |
| GET    | `/health`          | Check model availability             |
| GET    | `/status`          | Check last runtime + generation status |

---

## 🛠 Setup (Railway / Fly.io)

1. Fork + upload project to GitHub
2. Add environment variable:
3. Deploy using Railway or Fly.io
4. Hit `/` to trigger product generation

---

🧩 Built to harvest signal from noise — and turn it into profit.


## License
MIT License



