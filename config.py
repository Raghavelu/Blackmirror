import os
from dotenv import load_dotenv
from nixpkgs import pkgs

load_dotenv()  # This loads environment variables from a .env file


DEJAVU_FONT_PATH = f"{pkgs.dejavu_fonts}/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_PATH = os.environ.get('FPDF_FONT_DIR', DEJAVU_FONT_PATH)


# Check if the API key is loaded correctly
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    print("[ERROR] API key is missing. Please check your environment settings.")
else:
    print("[INFO] API key loaded successfully.")


