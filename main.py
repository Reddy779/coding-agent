import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("I need a Prompt!")
        sys.exit(1)
    verbose_flag = False
    
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
    prompt = sys.argv[1]

    message = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=message
    )


    if response is None or response.usage_metadata is None:
        print("response is malformed")
        return 
    
    print(f"\n{response.text}")
    if verbose_flag:
        print(f"User prompt: {prompt}")
        print(f"Prompt token: {response.usage_metadata.prompt_token_count}")
        print(f"Candidate  token: {response.usage_metadata.candidates_token_count}")

main()
# print(get_files_info("calculator", "pkg"))