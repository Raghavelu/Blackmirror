import random

def decide_product_type():
    # 25% chance for toolkit, 75% for ebook only
    return "both" if random.random() < 0.25 else "ebook"
