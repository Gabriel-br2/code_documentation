#!/usr/bin/env python
import json
from dotenv import load_dotenv
import os

from agent import Agent
from generate_JSON import JSON_gen

class README_gen:
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