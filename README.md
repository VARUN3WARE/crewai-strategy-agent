# 🔍 CrewAI Research Assistant

A powerful AI-powered research assistant built with **CrewAI**, **Exa**, and **Streamlit**, designed to help you research any topic using collaborative AI agents.

> ⚠️ **Note:** Image generation is currently **not available** due to the lack of OpenAI credits. The feature will be implemented in the future once access is restored.

![CrewAI Logo](https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg)

---

## 🌟 Features

- 🤖 Multi-model LLM support (OpenAI, GROQ, and Ollama)
- 🔍 Live AI-powered research using Exa search
- 📊 Real-time agent process tracking
- 📝 Auto-structured research reports
- 🎯 Topic-focused research and analysis via agents
- 🔒 API key input and configuration through sidebar
- 📱 Clean and responsive UI built with Streamlit

---
## 🧠 AI Creative Agent Workflow

This project builds a multi-agent system using CrewAI to simulate a full creative strategy pipeline.

---

### 🔍 1. Market Trend Analyst  
**Task:** Analyzes market trends, consumer behavior, and industry insights  
**Functions:** `create_market_analyst`, `create_analyst_task`, `run_analyst`

---

### 🎯 2. Brand Values Strategist  
**Task:** Extracts brand identity, mission, and values  
**Functions:** `create_brand_strategist`, `create_brand_strategist_task`, `run_brand_strategist`

---

### 🧠 3. Creative Strategy Synthesizer  
**Task:** Synthesizes market + brand data to guide campaign direction  
**Functions:** `create_strategy_synthesizer`, `create_strategy_synthesis_task`, `run_creative_strategy_synthesis`

---

### 🎨 4. Campaign Ideator Agent  
**Task:** Generates final campaign idea based on all insights  
**Functions:** `create_campaign_ideator`, `create_campaign_task`, `run_campaign_agent`

---

### 🔗 Flow Summary

```text
Market Trends ➡️ Brand Values ➡️ Creative Strategy ➡️ Final Campaign
```

## 📚 Code Organization

- **`streamlit_app.py`**  
  Main app interface: handles UI, research flow, and result display.

- **`src/components/agents.py`**  
  Configures LLMs, sets up CrewAI agents and tasks, integrates Exa.

- **`src/components/sidebar.py`**  
  Manages API key inputs, model selection (OpenAI, GROQ, Ollama).  
  ⚠️ *Image generation options are present but currently inactive.*

- **`src/utils/output_handler.py`**  
  Handles real-time agent output formatting and display.

---

## 🛠️ Project Structure
```
├── LICENSE
├── output
│   ├── analysts_report.md
│   ├── brand_report.md
│   ├── campaign_strategy_report.md
│   ├── final_creative_strategy.md
│   └── research_report.md
├── README.md
├── requirements.txt
├── src
│   ├── components
│   │   ├── agents.py
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   └── task.py
│   ├── __init__.py
│   └── utils
│       ├── output_handler.py
└── streamlit_app.py
```

---

## 📋 Requirements

- Python >=3.10 and <3.13
- Streamlit
- Exa API key
- (Optional) OpenAI or GROQ API key

---

## 🚀 Getting Started

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
2. **set and activate virtual env:**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
3. **install the req:**
```bash
pip install -r requirements.txt
```
4. **start the app:**
```bash
streamlit run streamlit_app.py
```
## 🔑 API Keys Setup
The app requires the following API keys (entered via the sidebar):

OpenAI API Key (optional)

GROQ API Key (optional) 

Exa API Key (required) 

You can test the app with Ollama locally without cloud LLMs as well.

## 🚫 Missing Feature Notice
Image generation support is currently disabled due to API limitations.
A future version will include prompt-to-image functionality once OpenAI API access is restored.

## 🤝 Contributing
Contributions are welcome!
Please submit a pull request or open an issue for any suggestions or improvements.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments
CrewAI – Agent framework

Exa – Search integration

Streamlit – Frontend framework