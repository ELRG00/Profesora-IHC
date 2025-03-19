# -*- coding: utf-8 -*-
"""Chat Bot IHC.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1J2TKoCDobbHQ7bGxsmLw8TrreLfJ5vUJ
"""

pip install openai==0.28 gradio SpeechRecognition pydub gTTS playsound

import openai
import gradio as gr
import speech_recognition as sr
from pydub import AudioSegment
import io
from gtts import gTTS
import os

# Configura tu clave de API de OpenAI
openai.api_key = "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"

def generar_respuesta(mensaje):
    """Genera una respuesta utilizando la API de OpenAI (gpt-4o) con respuestas más completas."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un profesor experto en Interacción Humano-Computadora (IHC). Tu objetivo es proporcionar respuestas detalladas, precisas y pedagógicas a las preguntas de los estudiantes sobre IHC. Solo habla de la IHC y Adopta un tono amigable y profesional."},
                {"role": "user", "content": f"responde a las siguientes preguntas: {mensaje}"},
            ],
            max_tokens=600,  # Aumenta el número máximo de tokens para respuestas más largas
            temperature=0.7, # Puedes ajustar la temperatura para variar la creatividad de las respuestas (valores más bajos son más deterministas)
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Ocurrió un error: {e}"

def reconocer_voz(audio):
    """Reconoce el texto del audio utilizando SpeechRecognition."""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio) as source:  # audio es un path
            audio_data = recognizer.record(source)
            texto = recognizer.recognize_google(audio_data, language="es-ES")
        return texto
    except Exception as e:
        return f"No se pudo reconocer la voz: {e}"

def texto_a_voz(texto):
    """Convierte texto a voz y guarda el audio en un archivo temporal."""
    tts = gTTS(text=texto, lang='es')
    temp_audio = "respuesta_temp.mp3"
    tts.save(temp_audio)
    return temp_audio

def chatbot(mensaje, audio):
    """Función principal del chatbot, maneja texto y voz."""
    mensaje_voz = ""
    if audio:
        mensaje_voz = reconocer_voz(audio)
        if mensaje:
            mensaje = mensaje + " " + mensaje_voz
        else:
            mensaje = mensaje_voz

    if mensaje:
        respuesta = generar_respuesta(mensaje)
        audio_respuesta = texto_a_voz(respuesta)
        return respuesta, audio_respuesta
    else:
        return "Por favor, introduce un mensaje o habla.", None

# Interfaz Gradio
iface = gr.Interface(
    fn=chatbot,
    inputs=[gr.Textbox(lines=2, placeholder="Escribe tu pregunta aquí..."),
            gr.Audio(sources=["microphone"], type="filepath")],
    outputs=[gr.Textbox(), gr.Audio()],
    title="Profesora de IHC",
    description="Pregúntale cualquier cosa sobre Interacción Humano-Computadora.",
    article="<p>Puedes acceder al Manual de Usuario <a href='https://drive.google.com/file/d/1-GYCA-wwvpCr7l4rR_yt7fw7KCx5UjNk/view?usp=sharing' target='_blank'>aquí</a>.</p>"
)

iface.launch()