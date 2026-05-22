import json
import os

from openai import OpenAI
from tools import tools, tool_functions

API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL")

if not API_KEY or not BASE_URL:
    raise RuntimeError("Missing API_KEY or BASE_URL environment variable.")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Tweak the prompt below to change the AI's persona
SYSTEM_PROMPT = """
Respond as a hyper-enthusiastic sponge. Start with: 'I'm ready! I'm ready!' and treat the query like Krabby Patty.

When the user asks about weather, you MUST use the get_weather tool.
Do not answer weather questions directly.
"""


# Stores the chat history to maintain conversation context
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print(f"[Persona] {SYSTEM_PROMPT}")
print("Type a message to start chatting, or enter 'q' to quit.\n")

while True:

    user_input = input("You: ")
    if user_input.strip() == "q":
        break

    # Store user message to maintain conversation context
    messages.append({"role": "user", "content": user_input})

    # Send full chat history to the model.
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools
    )

    # Extract the model's response and append it to the conversation history
    assistant_message = response.choices[0].message

    # Tool calling
    if assistant_message.tool_calls:

        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:

            args = json.loads(tool_call.function.arguments)

            func = tool_functions[tool_call.function.name]

            result = func(**args)

            print(f"[Tool Call] " f"{tool_call.function.name}({args}) " f"=> {result}")

            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages, tools=tools
            )

            assistant_message = response.choices[0].message

    # Store assistant response
    messages.append({"role": "assistant", "content": assistant_message.content})

    print(f"AI: {assistant_message.content}\n")
    print("========================================\n")
