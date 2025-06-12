import os

# from typing import Optional
from google.adk.agents import Agent
# from google.adk.agents.callback_context import CallbackContext
from speaker.tools.text_to_speech import text_to_speech
from dotenv import load_dotenv

load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
model_base = os.getenv("MODEL_LITE")

root_agent = Agent(
    model=model_base, # type: ignore
    name="root_agent",
    description=(
        "Helpful assistant."
    ),
    instruction=(
        "Talk to the user. Only if asked for audio,  use the `text_to_speach` tool to return the audio file."
    ),
    tools=[text_to_speech]
)