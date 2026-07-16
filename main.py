import os, argparse
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("api key missing")

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
    )

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


def main():
    model = "openrouter/free"
    prompt = args.user_prompt
    messages = [{"role": "user","content": prompt,}]

    response = client.chat.completions.create(model=model, messages=messages)

    if response.usage is None:
        raise RuntimeError("usage data missing")
    p_tokens = response.usage.prompt_tokens
    c_tokens = response.usage.completion_tokens 

    if args.verbose: 
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {p_tokens}")
        print(f"Response tokens: {c_tokens}")
    print(f"Response: {response.choices[0].message.content}")

if __name__ == "__main__":
    main()