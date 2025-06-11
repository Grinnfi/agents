import os
from google.cloud import storage
from google.cloud import texttospeech

from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")

def audio_to_storage(text: str,
                    file_name: str= str(datetime.now()),
                    voice: str = "pt-BR-Standard-A",
                    language_code: str="pt-BR",
                    speaking_rate: float=1.0,
                    pitch: float=0.0
                    ) -> str:

    # Initialize clients
    text_to_speech_client = texttospeech.TextToSpeechLongAudioSynthesizeClient()
    storage_client = storage.Client()
    
    # Select the language, voice name and SSML voice gender (optional for gender if name is specific)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    audio_bucket = os.getenv("GOOGLE_CLOUD_AUDIO_BUCKET")
    file_path = f"{audio_bucket}/{file_name}"
    output_gcs_uri = "gs://"+file_path
 
    # Synthesize long audio request saves straight into the bucket
    request = texttospeech.SynthesizeLongAudioRequest(
        parent=f"projects/{project_id}/locations/{location}",
        input=texttospeech.SynthesisInput(text=text),
        voice=voice_params,
        audio_config=audio_config,
        output_gcs_uri=output_gcs_uri,
    )

    # Start the long audio synthesis operation
    operation = text_to_speech_client.synthesize_long_audio(request=request)

    print(f"Long audio synthesis operation started: {operation.operation.name}")
    print("Waiting for operation to complete...")

    # Wait for the operation to complete
    result = operation.result()

    print(f"Audio synthesized and saved to: {output_gcs_uri}")

    autenticated_url = "https://storage.cloud.google.com/"+file_path
    print(f"Audio can be acessed via: {autenticated_url}")

    return output_gcs_uri

# audio_to_storage("teste 3",file_name="teste3",voice="pt-BR-Standard-B" ,pitch=0.2, speaking_rate=1.7)

def audio_to_local(text: str,
                    file_name: str= str(datetime.now()),
                    voice: str = "pt-BR-Standard-A",
                    language_code: str="pt-BR",
                    speaking_rate: float=1.0,
                    pitch: float=0.0
                    ) -> str:
    
    # Select the language, voice name and SSML voice gender (optional for gender if name is specific)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice_params, "audio_config": audio_config}
    )
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'audios',
                             file_name+'.wav')

    # Save locally
    with open(file_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{file_path}')

    return file_path