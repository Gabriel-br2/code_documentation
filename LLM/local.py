import json
import re

import ollama


class OLLAMA_APP:
    def __init__(self, model):
        self.model = model

    def request(self, payload, format_="") -> str:

        msg = dict()
        msg["role"] = "user"
        msg["content"] = f"{payload}"

        res = ollama.chat(model=self.model, messages=[msg], format=format_)

        if format_ == "":
            return res["message"]["content"]

        return json.loads(res["message"]["content"])
