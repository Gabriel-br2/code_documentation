#!/usr/bin/env python
import os
import json
from agent import Agent
from dotenv import load_dotenv

class code_summary:
    def __init__(self, verbose):
        load_dotenv()
        self.verbose = verbose
        
        base_url = os.getenv("BASE_URL")
        api_key  = os.getenv("API_KEY")
        model    = os.getenv("MODEL")
        
        self.Agent_summary_gen = Agent(base_url, api_key, model)        

    def setInitialContext(self, context: str):
        self.Agent_summary_gen.context = context

    def getReturnJsonPattern(self) -> dict:
        root = dict()
        
        root["main_points"] = "The main points and general purpose of the file."
        root["structure"] = "The main structure, such as important classes and functions."
        root["functions"] = "A brief explanation of what each main function does."
        
        return root

    def request(self):
        return self.Agent_summary_gen.request_json()

    def generate(self, msg: dict):
        self.Agent_summary_gen.payload = "<context>\n"
        self.Agent_summary_gen.payload += self.Agent_summary_gen.context
        self.Agent_summary_gen.payload += "\nFollow the bellow json to answer:\n"
        self.Agent_summary_gen.payload += json.dumps(self.getReturnJsonPattern(), indent=2)
        self.Agent_summary_gen.payload += "\n</context>\n"
        self.Agent_summary_gen.payload += "<file>\n"
        self.Agent_summary_gen.payload += json.dumps(msg, indent=2)
        self.Agent_summary_gen.payload += "\n</file>\n"