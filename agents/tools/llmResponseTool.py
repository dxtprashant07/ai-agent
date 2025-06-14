import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMResponseTool:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
        
    def format_creative_prompt(self, task):
        if 'poem' in task.lower():
            return "Create a short poem with the following requirements: " + task
        return task
        
    def generate_response(self, prompt):
        if not self.api_key:
            return "HuggingFace API key not found. Please set HUGGINGFACE_API_KEY in your .env file."
            
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            formatted_prompt = self.format_creative_prompt(prompt)
            
            response = requests.post(
                self.api_url, 
                headers=headers,
                json={"inputs": formatted_prompt}
            )
            
            # Log raw response for debugging
            print("Raw API Response:", response.text)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                    return result[0]["generated_text"].strip()
                return "The API response did not contain generated text. Please try again."
            elif response.status_code == 403:
                return "Please accept the model terms at huggingface.co before using."
            else:
                return f"Error {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"