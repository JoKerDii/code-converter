def save_cpp_code_to_file(cpp_code):
    code = cpp_code.replace("```cpp", "").replace("```", "")
    with open("optimized.cpp", "w") as f:
        f.write(code)
