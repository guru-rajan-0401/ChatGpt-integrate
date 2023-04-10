import openai,config
import gradio as gr
from pydub import AudioSegment

openai.api_key =config.OPENAI_API_KEY

messages=[{"role": "system", "content": "You are a helpful assistant."}]

def transcribe(audio):
    global messages
    print(audio)
    audio_file = AudioSegment.from_file(audio)
    audio_file.export("temp.wav", format="wav")
    with open("temp.wav", "rb") as f:
     transcript = openai.Audio.transcribe("whisper-1", f)
    messages.append({"role": "user", "content": transcript["text"]})
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)
    system_message = response["choices"][0]["message"]["content"]
    messages.append({"role":"assistant","content":system_message})    

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ui.launch()