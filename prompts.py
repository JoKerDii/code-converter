from config import system_message


def create_cpp_conversion_prompt(python_code):
    user_prompt = "Rewrite this Python code in C++ with the fastest possible implementation that produces identical output in the least time. "
    user_prompt += "Respond only with C++ code; do not explain your work other than a few comments. "
    user_prompt += "Pay attention to number types to ensure no int overflows. Remember to #include all necessary C++ packages such as iomanip.\n\n"
    user_prompt += python_code
    return user_prompt


def create_message_prompt(python_code):
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": create_cpp_conversion_prompt(python_code)},
    ]
