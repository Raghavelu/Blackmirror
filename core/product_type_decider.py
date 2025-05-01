from fpdf import FPDF
from core.deployer import extract_title
import os
import random

def decide_product_type():
    return random.choice(["ebook", "toolkit", "both"])
