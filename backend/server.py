from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Code Analysis Service")

# Initialize DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Request model
class CodeRequest(BaseModel):
    code: str


@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    """
    Receives Python code and returns AI-generated documentation.
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code is empty.")

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
                        "Do NOT include examples, code blocks, markdown formatting "
                        "or additional explanations.\n"
                        "Use plain text only."
                    )
                },
                {
                    "role": "user",
                    "content": request.code
                }
            ]
        )

        documentation = response.choices[0].message.content.strip()
        return {"documentation": documentation}

    except Exception as e:
        error_message = str(e)

        if "401" in error_message or "authentication" in error_message.lower():
            raise HTTPException(
                status_code=401,
                detail="Authentication failed. API key is missing or invalid."
            )

        raise HTTPException(status_code=500, detail=f"AI service error: {error_message}")

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint to verify the server is running.
    """
    return {"status": "ok"}

@app.get("/version")
async def get_version():
    return {"version": "1.0.0", "service": "AI Code Analysis Service"}
