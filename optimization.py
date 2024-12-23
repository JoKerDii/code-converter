from openai import OpenAI
import anthropic
from prompts import create_message_prompt, create_cpp_conversion_prompt
from file_io import save_cpp_code_to_file
from config import OPENAI_MODEL, CLAUDE_MODEL

openai = OpenAI()
claude = anthropic.Anthropic()


def optimize_with_gpt(python_code):
    stream = openai.chat.completions.create(
        model=OPENAI_MODEL, messages=create_message_prompt(python_code), stream=True
    )
    reply = ""
    for chunk in stream:
        fragment = chunk.choices[0].delta.content or ""
        reply += fragment
        print(fragment, end="", flush=True)
    save_cpp_code_to_file(reply)


def optimize_with_claude(python_code):
    result = claude.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=2000,
        system=system_message,
        messages=[
            {"role": "user", "content": create_cpp_conversion_prompt(python_code)}
        ],
    )
    reply = ""
    with result as stream:
        for text in stream.text_stream:
            reply += text
            print(text, end="", flush=True)
    save_cpp_code_to_file(reply)


def stream_gpt_output(python_code):
    stream = openai.chat.completions.create(
        model=OPENAI_MODEL, messages=create_message_prompt(python_code), stream=True
    )
    reply = ""
    for chunk in stream:
        fragment = chunk.choices[0].delta.content or ""
        reply += fragment
        yield reply.replace("```cpp\n", "").replace("```", "")


def stream_claude_output(python_code):
    result = claude.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=2000,
        system=system_message,
        messages=[
            {"role": "user", "content": create_cpp_conversion_prompt(python_code)}
        ],
    )
    reply = ""
    with result as stream:
        for text in stream.text_stream:
            reply += text
            yield reply.replace("```cpp\n", "").replace("```", "")


def optimize_code(python_code, model):
    if model == "GPT":
        result = stream_gpt_output(python_code)
    elif model == "Claude":
        result = stream_claude_output(python_code)
    else:
        raise ValueError("Unknown model")
    for stream_so_far in result:
        yield stream_so_far
