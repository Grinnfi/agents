import os

# from typing import Optional
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from dotenv import load_dotenv
from utils.tts import audio_to_storage

load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
model_base = os.getenv("MODEL_LITE")

def text_to_speach(text: str) -> str:
    """Synthesizes speech from the input text and returns the file path.
    Args:
        text[str]: A string to be converted
    Returns:
        file_path[str]: The audio file path
    """
    return (audio_to_storage(text))


root_agent = Agent(
    model=model_base, # type: ignore
    name="root_agent",
    description=(
        "Helpful assistant."
    ),
    instruction=(
        "Talk to the user. Only if asked for audio,  use the `text_to_speach` tool to return the audio file."
    ),
    tools=[text_to_speach]
)