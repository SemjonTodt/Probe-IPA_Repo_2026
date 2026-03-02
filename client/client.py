import argparse
import sys
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def handle_exceptions(message):
    """Central error handling function."""
    print(f"Error: {message}")
    sys.exit(1)

def check_backend():
    """Checks if the backend service is running and prints version info."""
    try:
        health_resp = requests.get(f"{BACKEND_URL}/health", timeout=5)
        health_resp.raise_for_status()
        version_resp = requests.get(f"{BACKEND_URL}/version", timeout=5)
        version_resp.raise_for_status()

        health_data = health_resp.json()
        version_data = version_resp.json()
        print(f"[BACKEND] Health: {health_data.get('status', 'unknown')}")
        print(f"[BACKEND] Version: {version_data.get('version', 'unknown')} | Service: {version_data.get('service', '')}")

    except requests.exceptions.RequestException as e:
        handle_exceptions(f"Backend not reachable: {str(e)}")

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
    """Sends the code to the backend service instead of directly calling DeepSeek."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"code": code_text},
            timeout=10
        )

        # Spezifische Handhabung nach Statuscode
        if response.status_code == 503:
            handle_exceptions("The AI service is currently unavailable. Please try again later.")

        if response.status_code == 500:
            handle_exceptions("The AI service can't be established. Please check the backend logs for more details.")

        if response.status_code != 200:
            handle_exceptions(f"Backend returned an error (status code {response.status_code}).")

        data = response.json()
        return data.get("documentation", "")

    except requests.exceptions.ConnectionError:
        handle_exceptions("Cannot reach backend. Is the server running?")
    except requests.exceptions.Timeout:
        handle_exceptions("Backend request timed out. Try again later.")
    except requests.exceptions.RequestException as e:
        handle_exceptions(f"Unexpected error during backend request: {str(e)}")

def save_result(text, filename="dokumentation.txt"):
    """Saves the AI response to a text file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
    except Exception as e:
        handle_exceptions(f"Could not save documentation: {str(e)}")

def main():
    """Entry point of the thin client."""
    # --- Backend checks ---
    check_backend()

    # --- Process CLI input ---
    args = parse_arguments()
    code = read_file(args.filepath)
    print("File successfully read.")

    documentation = get_ai_response_from_service(code)
    print("AI response received successfully.")

    # Output filename dependent on input file
    base_filename = os.path.splitext(os.path.basename(args.filepath))[0]
    save_result(documentation, filename=f"dokumentation_{base_filename}.txt")
    print(f"Documentation saved to dokumentation_{base_filename}.txt")

if __name__ == "__main__":
    main()
