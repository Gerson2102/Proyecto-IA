from google.cloud import language_v2
import requests
import json
from PIL import Image
from io import BytesIO
import random
import openai
import os

openai.api_key = "YOUR_OPENAI_KEY"


# Esta función analiza el texto y se determinan las emociones encontradas en el texto
def GoogleNaturalLanguageAPI(user_text_input):
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=user_text_input, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    # Emoción claramente positiva
    if float(sentiment.score) >= 0.6 and float(sentiment.magnitude) > 1.0:
        response = ChatGPT_API(
            user_text_input,
            "Toma en cuenta que, esta persona tiene emociones positivas: ",
        )
        return response
    # Emoción claramente neutral
    elif (
        float(sentiment.score) < 0.6
        and float(sentiment.score) > 0.0
        and float(sentiment.magnitude) <= 1.0
    ):
        response = ChatGPT_API(
            user_text_input,
            "Toma en cuenta que, esta persona tiene emociones neutrales: ",
        )
        return response
    # Emoción claramente negativa
    elif float(sentiment.score) < 0.0 and float(sentiment.magnitude) <= 4.0:
        response = ChatGPT_API(
            user_text_input,
            "Toma en cuenta que, esta persona tiene emociones negativas: ",
        )
        return response
    # Emociones mixtas
    else:
        response = ChatGPT_API(
            user_text_input, "Toma en cuenta que, esta persona tiene emociones mixtas: "
        )
        return response


# Esta funcón realiza la petición a Chat-GPT para que genere un texto motivacional en su respuesta
def ChatGPT_API(input_text, emotions):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Tu eres un psicólogo con mucha sabiduría que le encanta aconsejar a las personas que necesiten ayuda.",
            },
            {
                "role": "user",
                "content": "Quiero que generes un texto motivacional a partir del siguiente texto. "
                + emotions
                + "\n"
                + input_text,
            },
        ],
    )
    return response


# Esta función genera solicitudes al API de DALL-E con oraciones estbalecidas como positivas
def DALLE_API():
    sentences_for_images = [
        "Una pareja bailando bajo la lluvia.",
        "Una pareja viendo la puesta de sol juntos en la montaña.",
        "Un perro jugando con una pelota en un parque soleado.",
        "Una persona disfrutando de un día soleado en un campo de flores.",
        "Niños jugando y chapoteando en charcos después de la lluvia.",
        "Una persona leyendo un libro con una taza de café caliente en una acogedora cafetería.",
        "Amigos brindando y celebrando un logro importante con sonrisas enormes.",
        "Una persona disfrutando de un paseo en bicicleta en un hermoso paisaje campestre.",
        "Un grupo de personas bailando y cantando en un concierto en vivo.",
    ]
    responses = []
    for i in range(0, 3):
        random_index = random.randint(0, len(sentences_for_images) - 1)

        url = "https://api.openai.com/v1/images/generations"

        custom_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + openai.api_key,
        }

        reqBody = {
            "prompt": sentences_for_images[random_index],
            "n": 1,
            "size": "256x256",
        }

        res = requests.post(
            url,
            data=json.dumps(reqBody),
            headers=custom_headers,
        )
        responses.append(res)
    images = []
    for response in responses:
        json_response = json.loads(response.text)
        print(json_response)
        image_urls = [item["url"] for item in json_response["data"]]
        images += load_images(image_urls)
    return images


# Función para cargar las imágenes desde las URLs
def load_images(image_urls):
    images = []
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        images.append(img)
    return images
