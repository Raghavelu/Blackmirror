import random

def collect_chaos():
    chaos_samples = [
        "People struggle to stick to a daily routine.",
        "New entrepreneurs can't find product-market fit.",
        "Content creators burn out from posting too much.",
        "Job seekers don't know how to stand out in tech."
    ]

    selected_chaos = random.choice(chaos_samples)
    print(f"[Chaos Crawler] Selected chaos: {selected_chaos}")
    return selected_chaos
