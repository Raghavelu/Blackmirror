# Blackmirror

Blackmirror automates product creation from chaotic ideas, using free AI models.

## Project Structure
- `core/` → Handles chaos crawling, GPT processing, asset generation, and deployment.
- `utils/` → Model fallbacks and health checking tools.
- `assets/products/` → Generated product files (.txt, .pdf, .zip).

## Key Features
- Generates a full product twice a day (auto).
- Health-checks AI models before running.
- Allows manual generation anytime via web interface.
- Download the latest products as a ZIP bundle.

## Endpoints
| Path | Description |
|:-----|:------------|
| `/` | Run Blackmirror manually. |
| `/download/latest` | Download the latest generated product as a ZIP file. |
| `/health` | Run model health check. |

## Setup
1. Deploy to the Railway.
2. Set `OPENROUTER_API_KEY` in environment variables.
3. Set Cron Schedule to run daily at 09:00 UTC.
4. Set Healthcheck Path as `/health`.
5. Use UptimeRobot to trigger again at 21:00 UTC.

## License
MIT License
