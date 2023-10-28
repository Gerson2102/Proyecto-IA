import gradio as gr
from APIConnections import DALLE_API, GoogleNaturalLanguageAPI
import json
import tempfile
import os


def get_credentials():
    creds_json_str = os.getenv("GOOGLE_HUGGIN_FACE")

    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp:
        temp.write(creds_json_str)
        temp_filename = temp.name
    return temp_filename


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_credentials()


def text_to_output(text_input):
    response = GoogleNaturalLanguageAPI(text_input)
    images = DALLE_API()
    return response["choices"][0]["message"]["content"], images


iface = gr.Interface(
    fn=text_to_output,
    title="PRESTANDO MIS ALAS",
    description="Esta es una página en la que te puedes desahogar. Escribe acá tus problemas e intentaré ayudarte. Recuerda siempre acudir a una atención profesional.",
    inputs=gr.Textbox(label="Aquí abajo puedes escribir.", placeholder="Desahógate..."),
    outputs=[
        gr.Textbox(label="Acá te responderé :)"),
        gr.Gallery(rows=1, columns=3, height=260),
    ],
    allow_flagging="never",
)

iface.launch()
