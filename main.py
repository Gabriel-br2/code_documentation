#!/usr/bin/env python
import os
from generate_README import README_gen
from generate_JSON import JSON_gen


def main():
    api = README_gen()

    api.setInitialContext(
    """
    You are a specialist in technical documentation and embedded software engineering. Based on the source code and the complete structure of a Git repository (which will be provided in a json file), your task is to generate a README.md file in English, following professional documentation standards for embedded software and hardware projects.

        The README should contain, in separate and well-structured sections, the following topics:

        📖 Project Description — A clear and concise description of the project's purpose.
        ⚙️ System Behavior — A summary of how the system works, including main flows and interactions.
        💻 Software Interface — An example of how software should be implemented by calling its classes and functions (only include if applicable, if not skip to the next topic).
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
    dirAnalyser = JSON_gen(current_dir)
    
    api.generate(msg=dirAnalyser.json_output)
    
    print("Processing main README.md")
    response = api.request()
    
    file_name = "README.md"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(response)

    print(f"File {file_name} created!")

if __name__ == "__main__":
    main()