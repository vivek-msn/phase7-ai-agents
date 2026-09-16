import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import calculator, get_weather

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Define calculator tool
calculator_tool = types.FunctionDeclaration(
            name="calculator",
            description="Perform basic mathematical calculations.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "a": types.Schema(
                        type="NUMBER",
                        description="First number"
                    ),
                    "b": types.Schema(
                        type="NUMBER",
                        description="Second number"
                    ),
                    "operation": types.Schema(
                        type="STRING",
                        description="Operation: add,substract, multiply, or divide"
                    ),
                },
                required=["a", "b", "operation"],
            ),
        )

# Define weather tool
wheather_tool = types.FunctionDeclaration(
    name="get_weather",
    description="Get weather information for a city.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "city": types.Schema(
                type="STRING",
                description="Name of the city"
            ),
        },
        required=["city"],
    ),
)

# Tool config
tools = types.Tool(
    function_declarations=[
        calculator_tool,
        wheather_tool
    ]
)

# User's question
user_question = "What is 25 multiplied by 40?"

# Start conversation with the user message
contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(text=user_question)
        ]
    )
]

available_tools = {
    "calculator": calculator,
    "get_weather": get_weather
}

# Agent Loop
while True:

    # Ask Gemin wants to use a tool
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[tools]
        ),
    )


    # Check if Gemini wants to use a tool
    if response.function_calls:

        function_call = response.function_calls[0]

        print("Tool requested:", function_call.name)
        print("Arguments:", function_call.args)

        # Map tool names to actual Python functions
        available_tools = {
            "calculator": calculator,
            "get_weather": get_weather
        }

        # Find the requested tool
        tool = available_tools.get(function_call.name)


        if tool is None:
            raise ValueError(
                f"Unknown tool requested: {function_call.name}"
            )

        # Execute the selected tool
        result = tool(**function_call.args)

        print("Tool result:", result)

        # Add Gemini's tool-call response to conversation
        contents.append(response.candidates[0].content)
        
        # Add tool result to cpnversation
        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=function_call.name,
                            response={
                                "result": result
                            }
                        )
                    )
                ]
            )
        )

    else:
        # No more tools needed 
        print("Final Answer:", response.text)
        break