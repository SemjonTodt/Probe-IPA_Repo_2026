import argparse
import sys
import os
import requests
from dotenv import load_dotenv

# Load environment variables (falls du z.B. die Backend-URL in .env speicherst)
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def handle_exceptions(message):
    """Central error handling function."""
    print(f"Error: {message}")
    sys.exit(1)

def parse_arguments():
    """Reads CLI arguments."""
    parser = argparse.ArgumentParser(
        description="AI-Code-Companion Thin Client: Generates documentation via backend service."
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the Python (.py) file to analyze"
    )
    return parser.parse_args()

def read_file(path):
    """Reads a Python file as UTF-8 and returns its content."""
    if not os.path.exists(path):
        handle_exceptions("File not found.")
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
    except UnicodeDecodeError:
        handle_exceptions("File encoding is not UTF-8.")
    except Exception as e:
        handle_exceptions(str(e))
    if not content.strip():
        handle_exceptions("The file is empty.")
    return content

def get_ai_response_from_service(code_text):
    """
    Sends the code to the backend service instead of directly calling DeepSeek.
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"code": code_text},
            timeout=10
        )
        response.raise_for_status()  # raises HTTPError for 4xx/5xx
        data = response.json()
        return data.get("documentation", "")
    except requests.exceptions.RequestException as e:
        handle_exceptions(f"Backend request failed: {str(e)}")

def save_result(text, filename="dokumentation.txt"):
    """Saves the AI response to a text file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
    except Exception as e:
        handle_exceptions(f"Could not save documentation: {str(e)}")

def main():
    """Entry point of the thin client."""
    args = parse_arguments()
    code = read_file(args.filepath)
    print("File successfully read.")

    documentation = get_ai_response_from_service(code)
    print("AI response received successfully.")

    # Optional: make the output filename file-specific
    base_filename = os.path.splitext(os.path.basename(args.filepath))[0]
    save_result(documentation, filename=f"dokumentation_{base_filename}.txt")
    print(f"Documentation saved to dokumentation_{base_filename}.txt")

if __name__ == "__main__":
    main()
