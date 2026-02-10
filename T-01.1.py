import random

def motivational_insult(name: str) -> str:
    compliments = [
        "Du bist überraschend kompetent",
        "Ich hätte nicht gedacht, dass du das schaffst",
        "Respekt, das war fast beeindruckend",
        "Nicht schlecht für heute",
        "Du hast eindeutig Potenzial"
    ]
    return f"{name}, {random.choice(compliments)}."
