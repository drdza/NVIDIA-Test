
import os
import streamlit as st
from openai import OpenAI


api_key= os.getenv("GCP_APY_KEY")

# Configura el cliente de Nvidia API
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# Configura la app de Streamlit
st.title("Chatbot Nvidia NIM")
st.write("Escribe tu consulta y el chatbot te responderá usando el modelo Nvidia.")

# Configuración de chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Eres un asistente de IA."}]

# Entrada del usuario
user_input = st.text_input("Escribe tu mensaje aquí:")

if user_input:
    # Añade el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Realiza la llamada a la API
    completion = client.chat.completions.create(
        model="meta/llama-3.2-3b-instruct",
        messages=st.session_state.messages,
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )
    
    # Construye la respuesta
    bot_response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            bot_response += chunk.choices[0].delta.content
    
    # Añade la respuesta del bot al historial de mensajes
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Mostrar el historial de chat
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**Usuario:** {message['content']}")
    else:
        st.write(f"**Asistente:** {message['content']}")
