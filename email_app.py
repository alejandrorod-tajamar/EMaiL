import streamlit as st
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

# Cargar variables de entorno
load_dotenv(override=True)

# Configurar API de Azure OpenAI
client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-15-preview"
)

# Título de la app
st.title("EM:red[AI]L APP :email:🤖")
st.write("Welcome to the **email** _summarization_ and _answering_ web app!")

# Entrada de texto
txt = st.text_area("Text to analyze", placeholder="Enter your email here...")
st.write(f"The content of the email is {len(txt)} characters long.")

# Función para llamar al modelo
def call_gpt_model(prompt, task):
    model="gpt-4o-mini"  # Modelo desplegado en Azure

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can generate summaries and answers from email contents. You also adjust to the language, tone and length of the original email."},
            {"role": "user", "content": f"Task: Generate a{task} for this email:\n\n{prompt}"},
        ],
        max_tokens=300,
        temperature=0.7
    )
    
    return response.choices[0].message.content

# Botones y lógica
left, right = st.columns(2)

# Botón de resumen
if left.button("Generate Summary", icon="📝"):
    with st.spinner("Generating summary..."):
        summary_result = call_gpt_model(txt, " summary")
    left.markdown(summary_result)

# Botón de respuesta
if right.button("Generate Answer", icon="💡"):
    with st.spinner("Generating answer..."):
        answer_result = call_gpt_model(txt, "n answer")
    right.markdown(answer_result)
