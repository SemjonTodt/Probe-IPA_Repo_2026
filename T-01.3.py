import time

def dramatic_pause(text: str, delay: float = 0.4) -> None:
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print(" … 🎭")
