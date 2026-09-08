import argparse
import os
import sys
import json

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    messages = [{"role": "user", "content": args.p}]
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    chat = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "Read",
                    "description": "Read and return the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The path to the file to read",
                            }
                        },
                        "required": ["file_path"],
                    },
                },
            }
        ],
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # TODO: Uncomment the following line to pass the first stage
    # print(chat.choices[0].message.tool_calls[0].function.name)

    tool_call_present = chat.choices[0].message.tool_calls
    print("Messages: c", messages)
    while tool_call_present:
        argument = json.loads(chat.choices[0].message.tool_calls[0].function.arguments)
        messages.append(
            {
                "role": "tool",
                "content": open(argument["file_path"]).read(),
                "tool_call_id": chat.choices[0].message.tool_calls[0].id,
            }
        )
        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "Read",
                        "description": "Read and return the contents of a file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "The path to the file to read",
                                }
                            },
                            "required": ["file_path"],
                        },
                    },
                }
            ],
            # tool_choice="auto",
        )
        tool_call_present = chat.choices[0].message.tool_calls
        print("tool call present: ", tool_call_present)
        print("chat.choices[0].message.content: ", chat.choices[0].message.content)
    print("final chat.choices[0].message.content: ", chat.choices[0].message.content)


if __name__ == "__main__":
    main()
