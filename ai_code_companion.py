import argparse
import sys
import os


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
    Sends code to the DeepSeek API.
    Placeholder – will be implemented later.
    """
    pass


def save_result(text):
    """
    Saves the AI response to a text file.
    """
    pass


def main():
    """
    Entry point of the application.
    """
    args = parse_arguments()
    code = read_file(args.filepath)

    print("File successfully read.")
    print("Ready for API processing...")


if __name__ == "__main__":
    main()
