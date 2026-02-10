import argparse
import sys
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def handle_exceptions(message):
    """
    Central error handling function.
    """
    print(f"Error: {message}")
    sys.exit(1)


def parse_arguments():
    """
    Reads CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="AI-Code-Companion: Generates documentation for Python files using AI."
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the Python (.py) file to analyze"
    )
    return parser.parse_args()


def read_file(path):
    """
    Reads a Python file as UTF-8 and returns its content.
    """
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


def get_ai_response(code):
    """
    Sends code to the DeepSeek API and returns the generated documentation.
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyze the following Python code.\n\n"
                        "For each function, generate a short English documentation containing only:\n"
                        "- Function name\n"
                        "- Purpose\n"
                        "- Parameters (name and description)\n"
                        "- Return value\n\n"
                        "Do NOT include examples, code blocks, markdown formatting or additional explanations.\n"
                        "Use plain text only."
                    )
                },
                {
                    "role": "user",
                    "content": code
                }
            ]
        )

        print("API response received.")
        print(response.choices[0].message.content.strip())
        return response.choices[0].message.content.strip()

    except Exception as e:
        error_message = str(e)

        if "401" in error_message or "authentication" in error_message.lower():
            handle_exceptions(
                "Authentication failed. The API key is missing, invalid or expired."
            )

        handle_exceptions(f"API error: {error_message}")


def save_result(text):
    """
    Saves the AI response to a text file.
    """
    try:
        with open("dokumentation.txt", "w", encoding="utf-8") as file:
            file.write(text)
    except Exception as e:
        handle_exceptions(f"Could not save documentation: {str(e)}")


def main():
    """
    Entry point of the application.
    """
    args = parse_arguments()
    code = read_file(args.filepath)

    print("File successfully read.")

    documentation = get_ai_response(code)
    print("AI response received successfully.")

    save_result(documentation)
    print("Documentation saved to dokumentation.txt")


if __name__ == "__main__":
    main()
