import io
import sys
import subprocess
from file_io import save_cpp_code_to_file


def run_python_code(code):
    try:
        output = io.StringIO()
        sys.stdout = output
        exec(code)
    finally:
        sys.stdout = sys.__stdout__
    return output.getvalue()


def run_cpp_code(code):
    save_cpp_code_to_file(code)
    try:
        compile_cmd = [
            "clang++",
            "-Ofast",
            "-std=c++17",
            "-march=armv8.5-a",
            "-mtune=apple-m1",
            "-mcpu=apple-m1",
            "-o",
            "optimized",
            "optimized.cpp",
        ]
        compile_result = subprocess.run(
            compile_cmd, check=True, text=True, capture_output=True
        )
        run_cmd = ["./optimized"]
        run_result = subprocess.run(run_cmd, check=True, text=True, capture_output=True)
        return run_result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred:\n{e.stderr}"
