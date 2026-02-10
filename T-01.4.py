import random

def decision_maker(*options):
    if not options:
        raise ValueError("Ich kann nicht aus nichts wählen. So funktioniert das Universum nicht.")
    return random.choice(options)
