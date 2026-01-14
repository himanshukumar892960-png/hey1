import requests
import os
import json

class GroqClient:
    def __init__(self, api_key, model=None):
        self.api_key = api_key
        self.model = model or "llama3-8b-8192"
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def get_full_response(self, prompt, file_data=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Groq currently mainly text, but we'll include file prompt if text
        content_text = prompt
        if file_data and file_data.get('isText'):
             content_text += f"\n\n[Attached File Content]:\n{file_data.get('data')}"
        elif file_data:
             content_text += f"\n\n[Attached File: {file_data.get('name')}] (File processing not supported on this tier)"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are GlobleXGPT, an advanced AI assistant. "
                        "Return JSON with 'response' and 'emotion' keys. "
                        "Format response in Markdown. Be helpful and professional."
                    )
                },
                {
                    "role": "user",
                    "content": content_text
                }
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            try:
                json_content = json.loads(content)
                return {
                    "response": json_content.get("response", content),
                    "emotion": json_content.get("emotion", "Neutral")
                }
            except:
                return {"response": content, "emotion": "Neutral"}

        except Exception as e:
            print(f"Groq Error: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Groq Details: {e.response.text}")
            return None

    def get_response(self, prompt):
        res = self.get_full_response(prompt)
        if res: return res.get("response")
        return None
