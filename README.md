# Resumo de Bolso: Assistente de Estudo para Alunos

**Integrantes:**
* André Cizotti - RA: 10409439
* Gabriel Rodrigues - RA: 10409071
* Giulia Araki - RA: 10408954

**Descrição:**
Projeto desenvolvido para a disciplina de Inteligência Artificial da FCI (Mackenzie) para mitigar a sobrecarga cognitiva de estudantes através da geração de resumos estruturados a partir de arquivos de áudio de aulas. Utiliza processamento 100% local (Edge AI) para garantir a privacidade dos dados acadêmicos e a propriedade intelectual de professores e alunos.

**Status:** Produto Mínimo Viável (MVP) Concluído.

---

## 🛠️ Tecnologias Utilizadas
- **Streamlit:** Interface web ágil e interativa.
- **Whisper (OpenAI):** Modelo de Speech-to-Text de alta fidelidade para transcrição automatizada.
- **Ollama (Llama 3.2 1B):** Modelo de Linguagem de Grande Escala (LLM) local otimizado para eficiência de memória RAM e sumarização estruturada.

---

## 🚀 Como executar o projeto localmente

### 1. Pré-requisitos
- Python 3.9+ instalado.
- [FFmpeg](https://ffmpeg.org/) instalado no sistema (obrigatório para o processamento de áudio do Whisper).
- [Ollama](https://ollama.com/) instalado e em execução.

### 2. Baixando o modelo LLM
Abra o terminal e execute o comando abaixo para baixar o modelo Llama 3.2 de 1 bilhão de parâmetros (modelo leve otimizado para o projeto):
```bash
ollama pull llama3.2:1b