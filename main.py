#!/usr/bin/env python
import json
from dotenv import load_dotenv
import os

from openai import OpenAI

from generate_JSON import DirectoryAnalyzer

class LLMApi_generate_README:
    def __init__(self, verbose=False):
        load_dotenv()
        
        self.verbose = verbose
        self.client = OpenAI(base_url=os.getenv("BASE_URL"), 
                             api_key=os.getenv("API_KEY"))
        
        self.model = os.getenv("MODEL")
        self.dirAnalyser = DirectoryAnalyzer(self.verbose)

    def setInitialContext(self, context: str):
        self.context = context

    def generate(self, msg: dict):
        self.payload = "<context>\n"
        self.payload += self.context
        self.payload += "\n</context>\n"
        self.payload += "<json_code>\n"
        self.payload += json.dumps(msg, indent=2)
        self.payload += "\n</json_code>\n"

    def request(self) -> str:
        request = self.client.chat.completions.create(
            model=self.model, 
            messages=[{"role": "user", "content": self.payload}],
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
    api = LLMApi_generate_README()

    api.setInitialContext(
    """
    You are a specialist in technical documentation and embedded software engineering. Based on the source code and the complete structure of a Git repository (which will be provided in a json file), your task is to generate a README.md file in English, following professional documentation standards for embedded software and hardware projects.

        The README should contain, in separate and well-structured sections, the following topics:

        📖 Project Description — A clear and concise description of the project's purpose.
        ⚙️ System Behavior — A summary of how the system works, including main flows and interactions.
        📂 Code Structure — Organization of the files and modules in the repository.
        🔌 Hardware Interface (if applicable) — Components used and how the system interacts with the hardware.
        📐 Circuit Diagram (if applicable) — Explanation of the circuit and its elements.
        🛠️ Configuration Structure — How the system can be configured (e.g., presets, .ini files, constants, etc.).
        📝 Notes — Important considerations for operation, maintenance, or system usage.
        📊 Flowchart — A description (or pseudo-textual diagram) of the code's logical flow.
        ❌ Common Errors — A list of common errors and their possible causes/solutions.
        🔖 Version — Current version and version history, if applicable.
        👥 Team — Authors, contributors, and their responsibilities.
        💡 Inspirational Phrase — A motivational phrase related to the project's purpose or functionality.

        When writing the section titles and other highlights, enrich them with the use of emojis.
    """
    )
    current_dir = os.getcwd()
    json_output = api.dirAnalyser.save_to_json(current_dir)
    
    api.generate(msg=json_output)
    response = api.request()
    
    file = "README.md"
    with open(file, "w", encoding="utf-8") as arquivo:
        arquivo.write(response)

    print(f"File {file} created!")

if __name__ == "__main__":
    main()