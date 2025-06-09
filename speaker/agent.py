import os

from google.adk.agents import Agent
from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv()

model_base = os.getenv("MODEL_BASE")

# speaker_agent = Agent(
#     model=model_base,
#     name="speaker_agent",
#     description="Converts provided text into speech",

# )

def text_to_speach(text: str, filename: str="output", gender: str="NEUTRAL") -> str:
    """Synthesizes speech from the input text and saves it to an audio file.
    Args:
        text[str]: A string to be converted
        gender[str]: The voice gender, [NEUTRAL, MALE, FEMALE]
        filename[str]: The audio file name
    Returns:
        filename_path[str]: The audio file path
    """
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Gender
    if gender == "NEUTRAL":
        gender_voice = texttospeech.SsmlVoiceGender.NEUTRAL
    elif gender == "MALE":
        gender_voice = texttospeech.SsmlVoiceGender.MALE
    elif gender == "FEMALE":
        gender_voice = texttospeech.SsmlVoiceGender.FEMALE

    # Select the language and SSML voice gender (optional)
    gender_voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        ssml_gender=gender_voice,
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": gender_voice, "audio_config": audio_config}
    )

    # filename_path = os.path.dirname

    # The audio content is binary.
    with open(filename+'.mp3', "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{filename}+".mp3"')

    return filename

root_agent = Agent(
    model=model_base,
    name="root_agent",
    description=(
        "Helpful assistant."
    ),
    instruction=(
        "Talk to the user. If asked for audio, use the `text_to_speach` tool to return the audio file."
    ),
    # sub_agents=[speaker_agent]
    tools=[text_to_speach]
)