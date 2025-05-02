from fpdf import FPDF
from core.deployer import extract_title
from utils.models_fallback import smart_generate
from core.utils import sanitize_text
import os
import textwrap

# Font configuration - Railway compatible
FONT_URL = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")

def _ensure_font():
    """Download font if missing (Railway ephemeral storage fix)"""
    if not os.path.exists(FONT_PATH):
        os.makedirs(os.path.dirname(FONT_PATH), exist_ok=True)
        response = requests.get(FONT_URL)
        with open(FONT_PATH, 'wb') as f:
            f.write(response.content)

# Call once at startup
_ensure_font()

def generate_ebook_content(insight_text):
    system_prompt = """Expand into an 80-100 page eBook with:
1. Title Page
2. Table of Contents
3. 10 Chapters
4. Case Studies
5. Worksheets
6. Resource Appendix"""
    return smart_generate(system_prompt, insight_text)

def validate_pdf(path):
    try:
        with open(path, 'rb') as f:
            header = f.read(4)
            f.seek(-1024, 2)
            return header == b'%PDF' and b'%%EOF' in f.read()
    except Exception as e:
        print(f"PDF Validation Error: {str(e)}")
        return False

def write_ebook(insight_text):
    try:
        print("[eBook Writer] Starting generation...")
        title = sanitize_text(extract_title(insight_text))
        filename = f"assets/products/{title}_ebook.pdf"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Generate and sanitize content FIRST
        raw_content = generate_ebook_content(insight_text)
        clean_content = sanitize_text(raw_content)
        
        if not clean_content:
            raise ValueError("Empty content generated")

        # PDF Generation
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=25)
        effective_width = pdf.w - 2*pdf.l_margin
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)  # Add UTF-8 font
        pdf.set_font('DejaVu', '', 12)  # Use Unicode font

        def safe_add(text, font_size=12, style=''):
            """Universal safe text addition"""
            text = sanitize_text(str(text))
            pdf.set_font('Arial', style, font_size)
            
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                wrapped = textwrap.wrap(para, width=int(effective_width/4.5))
                for line in wrapped:
                    try:
                        pdf.multi_cell(effective_width, 10, line)
                    except:
                        line = line.encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(effective_width, 10, line)
                pdf.ln(4)

        # Title Page
        pdf.add_page()
        safe_add(title, 24, 'B')
        pdf.ln(30)
        safe_add(f"Generated: {os.path.basename(filename)}", 14)

        # Table of Contents
        pdf.add_page()
        safe_add("Table of Contents", 16, 'B')
        chapters = [line for line in clean_content.split('\n') if line.startswith('Chapter')]
        for idx, chapter in enumerate(chapters[:10]):
            safe_add(f"{idx+1}. {chapter[8:].strip()}", 12)

        # Main Content
        sections = clean_content.split('\n\n')
        for section in sections:
            if section.startswith('Chapter'):
                pdf.add_page()
                safe_add(section.strip(), 16, 'B')
            else:
                safe_add(section, 12)

        # Finalize PDF
        pdf.output(filename)
        
        # Modified validation to check text content instead of binary
        with open(filename, 'rb') as f:
            content = f.read()
            try:
                decoded_content = content.decode('utf-8', 'strict')
            except UnicodeDecodeError:
                decoded_content = content.decode('latin-1', 'replace')
            
            if '\x9c' in decoded_content:
                cleaned_content = decoded_content.replace('\x9c', '')
                with open(filename, 'w', encoding='utf-8') as f_out:
                    f_out.write(cleaned_content)
                print("[Warning] Repaired invalid character in PDF text layer")

        if not validate_pdf(filename):
            raise ValueError("PDF failed structural validation")
            
        print(f"[eBook Writer] Generated {filename} ({pdf.page_no()} pages)")
        return filename

    except Exception as e:
        print(f"[CRITICAL ERROR] eBook Generation Failed: {str(e)}")
        raise
