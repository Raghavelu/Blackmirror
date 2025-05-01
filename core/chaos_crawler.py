import random

def collect_chaos():
    chaos_samples = [
        "Remote teams struggle with asynchronous communication",
        "New founders fail to validate ideas before building",
        "Content creators experience audience burnout",
        "Freelancers undervalue their services consistently",
        "Startups scale prematurely before product-market fit",
        "Managers misuse OKRs, leading to team confusion",
        "SaaS companies struggle with churn reduction",
        "Solopreneurs fail to systemize their operations",
        "E-commerce stores have high cart abandonment rates.",
        "Tech professionals experience skill obsolescence."
    ]
    
    selected_chaos = random.choice(chaos_samples)
    print(f"[Chaos Crawler] Selected chaos: {selected_chaos}")
    return selected_chaos
