# Resumo de Bolso: Assistente de Estudo para Alunos

**Integrantes:**
* André Cizotti - RA: 10409439
* Gabriel Rodrigues - RA: 10409071
* Giulia Araki - RA: 10408954

**Descrição:**
Projeto desenvolvido para a disciplina de Inteligência Artificial da UPM (Mackenzie) para mitigar a sobrecarga cognitiva de estudantes através da geração de resumos estruturados a partir de aulas em áudio. Utiliza processamento 100% local para garantir a privacidade dos dados acadêmicos.

**Status:** Fase de Análise Exploratória (N1).


## Tecnologias Utilizadas
- **Streamlit:** Interface web.
- **Whisper (OpenAI):** Transcrição de áudio para texto (Speech-to-Text).
- **Ollama (Mistral / Llama):** LLM local para sumarização abstrativa estruturada.

## Como executar o projeto localmente

### 1. Pré-requisitos
- Python 3.9+ instalado.
- [FFmpeg](https://ffmpeg.org/) instalado na máquina (obrigatório para o Whisper funcionar).
- [Ollama](https://ollama.com/) instalado e rodando.

### 2. Baixando o modelo LLM
Abra o terminal e execute o Ollama para baixar o modelo Mistral (ou Llama):
```bash
ollama run mistral