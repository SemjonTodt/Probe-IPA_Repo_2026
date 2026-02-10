def coffee_to_code_ratio(coffee_cups: int) -> str:
    if coffee_cups <= 0:
        return "Kein Kaffee, kein Code. Physik."
    elif coffee_cups < 2:
        return "Code vorhanden, aber mit emotionaler Instabilität."
    elif coffee_cups < 5:
        return "Solider Code. Wahrscheinlich sogar lesbar."
    else:
        return "Du bist jetzt eins mit dem Code. Bitte blinke seltener."
