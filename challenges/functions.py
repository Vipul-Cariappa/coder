import requests

URL = "https://emkc.org/api/v2/piston/execute"

DATA = {
    "language": "python",
    "version": "3.10.0",
    "files": [
        {
            "name": "test.py",
            "content": "",
        },
        {
            "name": "main.py",
            "content": "",
        },
    ],
}


def run_code(solution, test_case):
    DATA["files"][0]["content"] = test_case
    DATA["files"][1]["content"] = solution
    output = requests.post(URL, json=DATA)

    # print(f"{output = }, {output.content = }, {output.text = }, {output.raw = }")

    return output.json()


def prepare_test_case(test_case):
    return "from main import *\n" + test_case


if __name__ == "__main__":
    run_code("", "")
