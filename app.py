import streamlit as st
import whisper
import tempfile
import os
import requests

# Configuração da página e aumento do limite de upload via código
st.set_page_config(page_title="Resumo de Bolso", page_icon="🎒")

st.title("🎒 Resumo de Bolso")
st.write("Transforme o áudio das suas aulas em resumos estruturados com IA local.")

transcription = None

# ==========================================
# UPLOAD DE ARQUIVO (MP3, MP4, etc)
# ==========================================
st.subheader("Faça o upload da sua aula")
uploaded_file = st.file_uploader("Formatos aceitos: MP3, WAV, M4A, MP4", type=["mp3", "wav", "m4a", "mp4"])

if uploaded_file is not None:
    if st.button("Gerar Resumo da Aula"):
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
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=500)
            response.raise_for_status()
            resumo = response.json().get("response", "")
            
            st.divider()
            st.subheader("📝 Resumo Gerado pela IA")
            st.markdown(resumo)
        except Exception as e:
            st.error("Erro ao conectar com o Ollama. Verifique se 'ollama serve' está rodando no terminal.")