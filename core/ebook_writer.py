from fpdf import FPDF
from core.deployer import extract_title
from core.utils import sanitize_text
import os
import textwrap
import subprocess
import logging
import glob
from config import FONT_PATH

# Configure logging
logger = logging.getLogger(__name__)

# Replace wildcard path with Nix store reference
FONT_DIR = "${pkgs.dejavu_fonts}/share/fonts/truetype/dejavu"
FONT_PATH = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# Dynamic font path resolution for Nix
def get_font_path():
    nix_font_dirs = glob.glob("/nix/store/*-dejavu-fonts-*/share/fonts/truetype/dejavu")
    print(f"Found Nix font directories: {nix_font_dirs}")
    if nix_font_dirs:
        return os.path.join(nix_font_dirs[0], "DejaVuSans.ttf")
    
    # Fallback to system paths
    system_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/local/share/fonts/dejavu/DejaVuSans.ttf"
    ]
    for path in system_paths:
        if os.path.exists(path):
            return path
    
    raise RuntimeError("DejaVu Sans font not found in any standard locations")

FONT_PATH = get_font_path()

def validate_font_installation():
    """Robust font validation with detailed error reporting"""
    if not os.path.exists(FONT_PATH):
        available = []
        if os.path.exists(os.path.dirname(FONT_PATH)):
            available = os.listdir(os.path.dirname(FONT_PATH))
        
        raise RuntimeError(
            f"Critical Font Error: DejaVu Sans not found at {FONT_PATH}\n"
            f"Available files in font directory: {available if available else 'Directory missing'}"
        )
    
    print(f"[Font Validation] Using font at: {FONT_PATH}")

def generate_ebook_content(insight_text):
    """Generate expanded eBook content using AI model"""
    system_prompt = """Create a comprehensive 80-100 page eBook with:
1. Title Page
2. Table of Contents
3. 10 Chapters with Sub-sections
4. Case Studies
5. Practical Worksheets
6. Resource Appendix"""
    
    from utils.models_fallback import smart_generate
    return smart_generate(system_prompt, insight_text)

def validate_pdf_structure(path):
    """Validate PDF file integrity"""
    try:
        with open(path, 'rb') as f:
            header = f.read(4)
            f.seek(-1024, 2)
            trailer = f.read(1024)
            
            valid_header = header == b'%PDF'
            valid_eof = b'%%EOF' in trailer
            
            if not valid_header:
                logger.error(f"Invalid PDF header: {header}")
            if not valid_eof:
                logger.error("Missing PDF EOF marker")
                
            return valid_header and valid_eof
    except Exception as e:
        logger.error(f"PDF validation failed: {str(e)}")
        return False

def create_pdf_document(title, content, output_path):
    """Core PDF generation with font handling"""
    validate_font_installation()
    
    pdf = FPDF()
    pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
    pdf.set_font('DejaVu', '', 12)
    pdf.set_auto_page_break(auto=True, margin=25)
    effective_width = pdf.w - 2 * pdf.l_margin

    def safe_add(text, font_size=12, style=''):
        """Robust text addition with wrapping and sanitization"""
        try:
            pdf.set_font('DejaVu', style, font_size)
            clean_text = sanitize_text(str(text))
            
            paragraphs = clean_text.split('\n\n')
            for para in paragraphs:
                wrapped = textwrap.wrap(para, width=int(effective_width/4.5))  # ~80 chars/line
                for line in wrapped:
                    pdf.multi_cell(effective_width, 10, line)
                pdf.ln(4)
        except Exception as e:
            logger.error(f"Failed to add text: {str(e)}")
            raise

    # Build PDF structure
    pdf.add_page()
    safe_add(title, 24, 'B')
    pdf.ln(30)
    safe_add(f"Generated: {os.path.basename(output_path)}", 14)

    pdf.add_page()
    safe_add("Table of Contents", 16, 'B')
    chapters = [line for line in content.split('\n') if line.startswith('Chapter')]
    for idx, chapter in enumerate(chapters[:10]):
        safe_add(f"{idx+1}. {chapter[8:].strip()}", 12)

    sections = content.split('\n\n')
    for section in sections:
        if section.startswith('Chapter'):
            pdf.add_page()
            safe_add(section.strip(), 16, 'B')
        else:
            safe_add(section, 12)

    pdf.output(output_path)
    return output_path

def write_ebook(insight_text):
    """Main eBook generation entry point"""
    try:
        logger.info("Starting eBook generation...")
        
        # Sanitize and validate input
        raw_content = generate_ebook_content(insight_text)
        clean_content = sanitize_text(raw_content)
        if not clean_content.strip():
            raise ValueError("Generated content is empty")
            
        # Create output filename
        title = sanitize_text(extract_title(insight_text))
        filename = f"assets/products/{title}_ebook.pdf"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Generate PDF
        output_path = create_pdf_document(title, clean_content, filename)
        
        # Final validation
        if not validate_pdf_structure(output_path):
            raise ValueError("PDF failed structural validation")
            
        logger.info(f"Successfully generated {output_path}")
        return output_path

    except Exception as e:
        logger.critical(f"eBook generation failed: {str(e)}")
        raise RuntimeError(f"PDF generation error: {str(e)}") from e
