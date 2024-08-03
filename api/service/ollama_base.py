from api.config import settings
import api.models
import api.schemas
import requests

class OllamaBase:
    def __init__(self,  models: str, stream: bool = False):
        self.ollama_url = settings.ollama_url
        self.headers = {
            "Content-Type": "application/json",
        }
        self.prompt = {
            "model": models,
            "stream": stream,
            "prompt": "A software developer is",
        }
        

    def post(self, endpoint, data):
        response = requests.post(f"{self.ollama_url}/{endpoint}", headers=self.headers, json=data)
        if response.status_code != 200:
            raise Exception(response.text)
        

        return response.json()

    def pull(self, endpoint, model):
        data = {
            "name": model,
        }
        response = requests.post(f"{self.ollama_url}/{endpoint}", headers=self.headers, json=data)

        if response.status_code != 200:
            raise Exception(response.text)
        

        return response.json()
    
    def get(self):
        response = requests.get(f"{self.ollama_url}", headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.text)
        

        return response.text
