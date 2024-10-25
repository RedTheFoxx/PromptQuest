from modules.llm_router import LLMConnector
import gradio as gr
import os

# Get Claude
llm_connector = LLMConnector(api_key=os.getenv("OPENROUTER_API_KEY"), site_url="", app_name="PromptQuest")

# Build the interface
pass