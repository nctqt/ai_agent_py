import os, argparse, sys
from dotenv import load_dotenv

from functions.call_functions import available_functions
from functions.call_function import call_function
import prompts

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
    messages = [
        {"role": "system", "content": prompts.system_prompt},
        {"role": "user","content": prompt},
        ]


    for x in range(20):
        response = client.chat.completions.create(
            model=model, 
            messages=messages, 
            temperature=0,
            tools=available_functions,
        )

        if response.usage is None:
            raise RuntimeError("usage data missing")
        p_tokens = response.usage.prompt_tokens
        c_tokens = response.usage.completion_tokens 

        if args.verbose: 
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {p_tokens}")
            print(f"Response tokens: {c_tokens}")

        message = response.choices[0].message.content
        history = response.choices[0].message
        messages.append(history)
        
        if response.choices[0].message.tool_calls is not None:
            for tool_call in response.choices[0].message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
            if result_message["content"] == "":
                return f'Error: response content is empty'
            if args.verbose:
                print(f"-> {result_message['content']}")
        else:
            print(f"Response: {message}")
            return
        if x == 19:
            print(f'Error: maximum iterations reached')
            sys.exit(1) 

if __name__ == "__main__":
    main()