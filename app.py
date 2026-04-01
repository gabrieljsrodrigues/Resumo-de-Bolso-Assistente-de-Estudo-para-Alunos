import streamlit as st
import whisper
import tempfile
import os
import requests
import re
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="Resumo de Bolso", page_icon="🎒")

st.title("🎒 Resumo de Bolso")
st.write("Transforme o áudio das suas aulas ou vídeos do YouTube em resumos estruturados com IA local.")

# Menu de escolha
opcao = st.radio("Escolha a fonte da aula:", ("Upload de Arquivo (Áudio)", "Link do YouTube"))

transcription = None

# ==========================================
# OPÇÃO 1: UPLOAD DE ÁUDIO
# ==========================================
if opcao == "Upload de Arquivo (Áudio)":
    uploaded_file = st.file_uploader("Faça o upload da aula (Áudio ou Vídeo)", type=["mp3", "wav", "m4a", "mp4"])
    
    if uploaded_file is not None:
        if st.button("Gerar Resumo da Aula"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            with st.spinner("Transcrevendo o áudio com Whisper... (Isso pode levar alguns minutos)"):
                try:
                    model = whisper.load_model("base")
                    result = model.transcribe(tmp_path)
                    transcription = result["text"]
                    
                    st.success("Transcrição concluída com sucesso!")
                    with st.expander("Visualizar Transcrição Bruta"):
                        st.write(transcription)
                except Exception as e:
                    st.error(f"Erro na transcrição: {e}")
                finally:
                    os.remove(tmp_path)

# ==========================================
# OPÇÃO 2: LINK DO YOUTUBE
# ==========================================
elif opcao == "Link do YouTube":
    youtube_url = st.text_input("Cole o link do vídeo do YouTube aqui:")
    
    if youtube_url:
        if st.button("Extrair e Resumir"):
            with st.spinner("Extraindo legendas do vídeo..."):
                try:
                    # Expressão regular para capturar o ID do vídeo na URL
                    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
                    
                    if video_id_match:
                        video_id = video_id_match.group(1)
                        # Tenta pegar a legenda em português ou inglês
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
                        transcription = " ".join([t['text'] for t in transcript_list])
                        
                        st.success("Legendas extraídas com sucesso!")
                        with st.expander("Visualizar Texto Extraído"):
                            st.write(transcription)
                    else:
                        st.error("Link do YouTube inválido. Verifique a URL e tente novamente.")
                except Exception as e:
                    st.error("Erro ao extrair legendas. O vídeo pode não ter legendas disponíveis ou está bloqueado.")
                    st.error(f"Detalhes do erro: {e}")

# ==========================================
# GERAÇÃO DO RESUMO COM OLLAMA
# ==========================================
if transcription:
    with st.spinner("Gerando resumo com Ollama (Mistral)..."):
        prompt = f"""Você é um assistente acadêmico. Baseado na seguinte transcrição de aula, crie um resumo estruturado contendo obrigatoriamente:
        1. Tópicos principais
        2. Conceitos-chave
        3. Pontos de revisão (possíveis perguntas para estudo)

        Transcrição:
        {transcription}
        """

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            resumo = response.json().get("response", "")
            
            st.markdown("### 📝 Resumo Estruturado")
            st.markdown(resumo)
        except Exception as e:
            st.error("Erro ao conectar com o Ollama. Certifique-se de que o Ollama está rodando localmente.")
            st.error(f"Detalhes do erro: {e}")