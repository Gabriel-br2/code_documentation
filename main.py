#!/usr/bin/env python
import json
from dotenv import load_dotenv
import os

from agent import Agent
from generate_JSON import JSON_gen

class generate_README:
    def __init__(self, verbose=False):
        load_dotenv()
        self.verbose = verbose
        
        base_url=os.getenv("BASE_URL")
        api_key=os.getenv("API_KEY")
        model = os.getenv("MODEL")
        
        self.Agent_gen_README = Agent(base_url, api_key, model)   
        
    def setInitialContext(self, context: str):
        self.Agent_gen_README.context = context
        
    def request(self):
        return self.Agent_gen_README.request_str()

    def generate(self, msg: dict):
        self.Agent_gen_README.payload = "<context>\n"
        self.Agent_gen_README.payload += self.Agent_gen_README.context
        self.Agent_gen_README.payload += "\n</context>\n"
        self.Agent_gen_README.payload += "<json_code>\n"
        self.Agent_gen_README.payload += json.dumps(msg, indent=2)
        self.Agent_gen_README.payload += "\n</json_code>\n"


def main():
    api = generate_README()

    api.setInitialContext(
    """
    You are a specialist in technical documentation and embedded software engineering. Based on the source code and the complete structure of a Git repository (which will be provided in a json file), your task is to generate a README.md file in English, following professional documentation standards for embedded software and hardware projects.

        The README should contain, in separate and well-structured sections, the following topics:

        📖 Project Description — A clear and concise description of the project's purpose.
        ⚙️ System Behavior — A summary of how the system works, including main flows and interactions.
        📂 Code Structure — Organization of the files and modules in the repository.
        🔌 Hardware Interface — Components used and how the system interacts with the hardware (only include if applicable, if not skip to the next topic). 
        📐 Circuit Diagram — Explanation of the circuit and its elements (only include if applicable, if not skip to the next topic).
        🛠️ Configuration Structure — How the system can be configured (e.g., presets, .ini files, constants, etc.).
        📝 Notes — Important considerations for operation, maintenance, or system usage.
        ❌ Common Errors — A list of common errors and their possible causes/solutions.
        🔖 Version — Current version and version history, if applicable.
        👥 Team — Authors, contributors, and their responsibilities.
        💡 Inspirational Phrase — A motivational phrase related to the project's purpose or functionality.

        When writing the section titles and other highlights, enrich them with the use of emojis. Reply only with the readme and nothing else
    """
    )
    current_dir = os.getcwd()
    dirAnalyser = JSON_gen()
    
    json_output = dirAnalyser.save_to_json(current_dir)
    print(json_output)
    
    api.generate(msg=json_output)
    
    print("Processing main README.md")
    response = api.request()
    
    file = "README.md"
    with open(file, "w", encoding="utf-8") as arquivo:
        arquivo.write(response)

    print(f"File {file} created!")

if __name__ == "__main__":
    main()