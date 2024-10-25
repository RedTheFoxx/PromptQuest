"""This module is used to provide a LLM to any usage. It currently uses Claude 3.5 Sonnet from Anthropic."""

import requests
from typing import Dict

# CONFIGURATION DU LLM
# ------------------------------------------------------------
DEFAULT_SYSTEM_PROMPT = "You are an assistant and always answer in the user's language. Be concise in your answers."
# ------------------------------------------------------------

class LLMConnector:
    def __init__(self, api_key: str, site_url: str = "", app_name: str = "PromptQuest", system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        self.api_key = api_key
        self.site_url = site_url
        self.app_name = app_name
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.system_prompt = system_prompt

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
        }

    def get_answer(self, prompt: str) -> str:
        """
        Obtain an answer from the LLM for a given prompt
        
        Args:
            prompt (str): The text of the prompt to send
            
        Returns:
            str: The answer from the LLM
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = requests.post(
                url=self.base_url,
                headers=self._get_headers(),
                json={
                    "model": "anthropic/claude-3.5-sonnet",
                    "messages": messages
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error requesting to the API: {str(e)}")
        
    def set_system_prompt(self, prompt: str):
        """
        Set the system prompt for the LLM to use. It is intended to be its default one.
        
        Args:
            prompt (str): The text of the system prompt to send to the LLM
        """
        self.system_prompt = prompt
