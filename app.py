import streamlit as st
import whisper
import tempfile
import os
import requests
import re
from youtube_transcript_api import YouTubeTranscriptApi

# Configuração da página e aumento do limite de upload via código
st.set_page_config(page_title="Resumo de Bolso", page_icon="🎒")

st.title("🎒 Resumo de Bolso")
st.write("Transforme o áudio das suas aulas ou vídeos do YouTube em resumos estruturados com IA local.")

# Menu de escolha
opcao = st.radio("Escolha a fonte da aula:", ("Upload de Arquivo (Áudio/Vídeo)", "Link do YouTube"))

transcription = None

# ==========================================
# OPÇÃO 1: UPLOAD DE ARQUIVO (MP3, MP4, etc)
# ==========================================
if opcao == "Upload de Arquivo (Áudio/Vídeo)":
    # Aumentamos a instrução visual para o usuário
    uploaded_file = st.file_uploader("Faça o upload da aula (Formatos aceitos: MP3, WAV, M4A, MP4)", type=["mp3", "wav", "m4a", "mp4"])
    
    if uploaded_file is not None:
        if st.button("Gerar Resumo do Arquivo"):
            # Salva com a extensão original para o Whisper não se perder
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            with st.spinner("Transcrevendo com Whisper... (Isso pode levar alguns minutos dependendo do tamanho)"):
                try:
                    # Usamos o modelo 'base' para equilíbrio entre velocidade e precisão
                    model = whisper.load_model("base")
                    result = model.transcribe(tmp_path)
                    transcription = result["text"]
                    
                    st.success("Transcrição concluída!")
                    with st.expander("Visualizar Transcrição Bruta"):
                        st.write(transcription)
                except Exception as e:
                    st.error(f"Erro na transcrição: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

# ==========================================
# OPÇÃO 2: LINK DO YOUTUBE (Versão Corrigida)
# ==========================================
elif opcao == "Link do YouTube":
    youtube_url = st.text_input("Cole o link do vídeo do YouTube aqui:")
    
    if youtube_url:
        if st.button("Extrair e Resumir"):
            with st.spinner("Buscando legendas no YouTube..."):
                try:
                    # Regex para o ID do vídeo
                    video_id_match = re.search(r"(?:v=|\/|embed\/|youtu.be\/)([0-9A-Za-z_-]{11})", youtube_url)
                    
                    if video_id_match:
                        video_id = video_id_match.group(1)
                        
                        # Tenta pegar a legenda direto (pt-BR, pt ou en)
                        try:
                            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt-BR', 'pt', 'en'])
                        except:
                            # Se o erro persistir, tenta listar todas as legendas disponíveis e pegar a primeira
                            # Note que aqui usamos a classe para buscar a lista primeiro
                            transcript_list_obj = YouTubeTranscriptApi.list_transcripts(video_id)
                            # Pega a primeira legenda (seja automática ou manual)
                            transcript_list = list(transcript_list_obj)[0].fetch()
                            
                        transcription = " ".join([t['text'] for t in transcript_list])
                        
                        st.success("Legendas extraídas com sucesso!")
                        with st.expander("Visualizar Texto das Legendas"):
                            st.write(transcription)
                    else:
                        st.error("Não foi possível identificar o ID do vídeo.")
                except Exception as e:
                    st.error("🚨 Ocorreu um erro ao acessar as legendas.")
                    st.code(str(e))
# ==========================================
# MOTOR DE RESUMO (OLLAMA)
# ==========================================
if transcription:
    with st.spinner("IA local processando o resumo..."):
        prompt = f"""Você é um assistente acadêmico de alto nível. 
        Baseado na transcrição abaixo, gere um resumo estruturado em português:
        
        1. TÓPICOS PRINCIPAIS: (Liste os temas centrais)
        2. CONCEITOS-CHAVE: (Explique brevemente os termos técnicos usados)
        3. PERGUNTAS DE REVISÃO: (Crie 3 perguntas para testar o conhecimento)

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
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            resumo = response.json().get("response", "")
            
            st.divider()
            st.subheader("📝 Resumo Gerado pela IA")
            st.markdown(resumo)
        except Exception as e:
            st.error("Erro ao conectar com o Ollama. Verifique se 'ollama serve' está rodando.")