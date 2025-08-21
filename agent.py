#!/usr/bin/env python
import os
import json
from tabnanny import verbose

from openai import OpenAI

class Agent:
    def __init__(self, base_url, api_key, model, verbose=False):        
        self.client = OpenAI(base_url=base_url,
                             api_key=api_key)
        
        self.model = model
        self.payload = ""
        self.context = ""
        self.payload = ""
        
        self.verbose = verbose

    def request_str(self) -> str:
        request = self.client.chat.completions.create(
            model=self.model, 
            messages=[{"role": "user", "content": self.payload}],
        )
        
        self.debug_print(request.usage)
        response = request.choices[0].message.content 
        self.debug_print(response)
        self.debug_print("==============================")
        return response
    

    def request_json(self) -> str:
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