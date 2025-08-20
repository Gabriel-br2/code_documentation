#!/usr/bin/env python
import json
from dotenv import load_dotenv
import os

from openai import OpenAI

class LLMApi_summary:
    def __init__(self, verbose):
        load_dotenv()
        
        self.verbose = verbose
        self.client = OpenAI(base_url=os.getenv("BASE_URL"),
                             api_key=os.getenv("API_KEY"))
        
        self.model = os.getenv("MODEL")
        self.api_extra_headers = ""

    def setInitialContext(self, context: str):
        self.context = context

    def getReturnJsonPattern(self) -> dict:
        root = dict()
        
        root["main_points"] = "The main points and general purpose of the file."
        root["structure"] = "The main structure, such as important classes and functions."
        root["functions"] = "A brief explanation of what each main function does."
        
        return root

    def generate(self, msg: dict):
        self.payload = "<context>\n"
        self.payload += self.context
        self.payload += "\nFollow the bellow json to answer:\n"
        self.payload += json.dumps(self.getReturnJsonPattern(), indent=2)
        self.payload += "\n</context>\n"
        self.payload += "<file>\n"
        self.payload += json.dumps(msg, indent=2)
        self.payload += "\n</file>\n"

    def request(self) -> str:
        request = self.client.chat.completions.create(
            model=self.model, 
            messages=[{"role": "user", "content": self.payload}],
            response_format={"type": "json_object"},
        )
        
        self.debug_print(request.usage)
        response = request.choices[0].message.content 
        self.debug_print(response)
        self.debug_print("==============================")
        return response
    
    def debug_print(self, msg):
        if self.verbose:
            print(msg)

def main():
    api = LLMApi_summary()

    api.setInitialContext(
        "You are acting as a code review expert. Analyze the following Python code file and provide a clear and concise summary. I want it to be short, very summarized"
    )

    with open("configpy.py", "r", encoding="utf-8", errors="ignore") as f:
        content_full = f.read()
                        
    api.generate(msg=content_full)

    print(api.request())


if __name__ == "__main__":
    main()