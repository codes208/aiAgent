import os
import sys
import argparse
from call_functions import available_functions, call_function
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")         
    if not api_key:
        raise Exception("No GEMINI key found!")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(20):
        response, function_responses = generate_content(client, messages, args.verbose)

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if not response.function_calls:
            break

        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))

    else:
        print("Error: maximum iterations reached without a final response.")
        sys.exit(1)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
              )
            )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        print(f"Response:\n{response.text}")
        return response, []

    function_responses = []
    for call in response.function_calls:
        result = call_function(call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")

        function_responses.append(result.parts[0])

    return response, function_responses

if __name__ == "__main__":
    main()


