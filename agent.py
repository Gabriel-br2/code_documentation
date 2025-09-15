#!/usr/bin/env python
from LLM.api import OPENROUNTER_API
from LLM.local import OLLAMA_APP
from openai import OpenAI


class Agent:
    def __init__(self, base_url, api_key, model, source="api", verbose=False):
        self.client = OpenAI(base_url=base_url, api_key=api_key)

        self.model = model
        self.payload = ""
        self.context = ""
        self.payload = ""

        self.verbose = verbose

        self.source = OLLAMA_APP if source == "local" else OPENROUNTER_API
        self.llm = self.source(model)

        print("Using model:", model, "from", source)

    def request_str(self) -> str:
        return self.llm.request(self.payload, format_="")

        # request = self.client.chat.completions.create(
        #    model=self.model,
        #    messages=[{"role": "user",
        #               "content": self.payload}],
        # )
        #
        # self.debug_print(request.usage)
        # response = request.choices[0].message.content
        # self.debug_print(response)
        # self.debug_print("==============================")
        # return response

    def request_json(self) -> str:
        return self.llm.request(self.payload, format_="json")

        # request = self.client.chat.completions.create(
        #    model=self.model,
        #    messages=[{"role": "user",
        #               "content": self.payload}],
        #
        #    response_format={"type": "json_object"},
        # )
        #
        # self.debug_print(request.usage)
        # response = request.choices[0].message.content
        # self.debug_print(response)
        # self.debug_print("==============================")
        # return response

    def debug_print(self, msg):
        if self.verbose:
            print(msg)
