# 🏛️ AI Software Architect 
BY:
Riya Phagna 
MCA

**Design scalable system architectures in seconds using AI.**

Turn a simple project idea into a complete software blueprint — architecture, tech stack, APIs, database schema, and development roadmap.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.1%2B-1C3C3C?style=flat-square)](https://langchain.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Groq](https://img.shields.io/badge/Groq-Free%20API-orange?style=flat-square)](https://console.groq.com)

</div>

---

## 📌 What Is This?

**AI Software Architect** is a Generative AI-powered web application that helps developers, students, and startups automatically generate complete software architecture plans from a simple text description.

Instead of spending hours designing system architecture manually, you describe your idea in plain English and the AI instantly produces a structured, professional blueprint.

### Who Is It For?

- 🎓 **Students** learning system design and software architecture
- 🚀 **Startups** quickly planning new applications
- 👨‍💻 **Developers** who need a structured starting point for projects
- 🏢 **Teams** that want to accelerate the planning phase

---

## ✨ Features

| Feature | Description |
|---|---|
| 📋 **Project Overview** | Summary, project type, scale, and key challenges |
| 🛠️ **Technology Stack** | Frontend, backend, database, and cloud recommendations |
| 🏗️ **System Architecture** | Components, data flow diagram, scalability notes |
| 🗄️ **Database Schema** | Tables, columns, data types, and relationships |
| 🔌 **API Design** | REST endpoints with methods, paths, auth requirements |
| 🗺️ **Development Roadmap** | Phased plan with tasks, milestones, and deliverables |
| 🔐 **Security Plan** | Key security considerations and team structure |
| 📊 **Complexity Metrics** | Team size, duration estimate, and complexity rating |
| ⬇️ **Export** | Download as JSON or Markdown report |

---

## 🖥️ Demo

```
Input:
  "Build a food delivery mobile application with real-time GPS
   tracking, multiple restaurant support, and in-app payments."

Output:
  ✅ Tech Stack    → React Native + Node.js + PostgreSQL + Redis + AWS
  ✅ Architecture  → Microservices with API Gateway
  ✅ Database      → 6 tables: Users, Restaurants, Orders, Payments...
  ✅ API Endpoints → 12 endpoints: /login, /orders, /track/{id}...
  ✅ Roadmap       → 5 phases over 4-6 months
  ✅ Security      → JWT auth, rate limiting, data encryption...
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-software-architect.git
cd ai-software-architect
```

### 2. Create a virtual environment

```bash
# Create
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **SSL Error on Windows?** Use this instead:
> ```bash
> pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
> ```

### 4. Set up your API key

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your key:

```env
# For Groq (Free)
GROQ_API_KEY=gsk_your_key_here

# For OpenAI (Paid)
OPENAI_API_KEY=sk_your_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501** 🎉

---

## 🔑 Getting a Free API Key (Groq)

Groq provides **free API access** to LLaMA 3 models — no credit card required.

1. Go to 👉 **https://console.groq.com**
2. Sign up with your Google account
3. Navigate to **API Keys** → **Create API Key**
4. Give it any name → click **Submit**
5. Copy the key (starts with `gsk_...`) — shown only once!
6. Paste it in the app sidebar under **API Key**

> **OpenAI alternative:** Get a key at https://platform.openai.com (requires payment after free trial)

---

## 📁 Project Structure

```
ai-software-architect/
│
├── app.py              ← Main Streamlit UI (entry point)
├── architect.py        ← LangChain + AI generation logic
├── prompts.py          ← AI prompt templates
│
├── requirements.txt    ← Python dependencies
├── .env.example        ← Environment variable template
├── .gitignore          ← Git ignore rules
└── README.md           ← This file
```

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **UI** | Streamlit | Web interface |
| **AI Framework** | LangChain Core | Prompt chaining |
| **AI Model (Free)** | Groq + LLaMA 3.3 70B | Architecture generation |
| **AI Model (Paid)** | OpenAI GPT-4o | Architecture generation |
| **Language** | Python 3.9+ | Backend logic |
| **Config** | python-dotenv | Environment management |

---

## 📦 Dependencies

```
streamlit>=1.32.0
langchain-core>=0.1.0
langchain-openai>=0.0.5
langchain-groq>=0.1.0
openai>=1.0.0
python-dotenv>=1.0.0
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

| Setting | Where | Description |
|---|---|---|
| `GROQ_API_KEY` | `.env` file | Free Groq API key |
| `OPENAI_API_KEY` | `.env` file | OpenAI API key |
| AI Provider | App sidebar | Switch between Groq / OpenAI |
| Model | App sidebar | Select specific model |

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: langchain_openai` | Package not installed | `pip install langchain-openai` |
| `ModuleNotFoundError: langchain_groq` | Package not installed | `pip install langchain-groq` |
| `ModuleNotFoundError: langchain.prompts` | Old LangChain version | Use `langchain_core.prompts` (already fixed in v3) |
| `SSL Certificate Error` | Network firewall | Add `--trusted-host pypi.org --trusted-host files.pythonhosted.org` to pip commands |
| `Invalid API Key 401` | Wrong key pasted | Double-check your key in the sidebar |
| `No such file: requirements.txt` | Wrong directory | `cd` into the project folder first |
| Port already in use | Another app on 8501 | `streamlit run app.py --server.port 8502` |

---

## 🗺️ How It Works

```
User Input (project idea)
        ↓
LangChain Prompt Template
        ↓
Groq / OpenAI API (LLM)
        ↓
Structured JSON Response
        ↓
Streamlit UI (7 tabbed sections)
        ↓
Export: JSON / Markdown Report
```

1. The user types a project idea in plain English
2. LangChain builds a detailed prompt using a system + user template
3. The prompt is sent to the AI model (Groq or OpenAI)
4. The AI responds with a structured JSON blueprint
5. Streamlit parses and renders the results in a professional UI

---

## 🔮 Future Enhancements

- [ ] Automatic architecture diagram generation (Mermaid / Draw.io)
- [ ] Cloud cost estimation (AWS / GCP / Azure pricing)
- [ ] Security vulnerability analysis
- [ ] GitHub repository auto-scaffolding
- [ ] PDF export of the architecture report
- [ ] Refine architecture with follow-up prompts
- [ ] Team collaboration and sharing

## output
<img width="1905" height="874" alt="image" src="https://github.com/user-attachments/assets/6e36dbd2-a2ea-49db-b23d-836ad7b1480b" />

<img width="1914" height="846" alt="image" src="https://github.com/user-attachments/assets/479faa9e-560b-4187-81ae-e250f5a337c0" />
<img width="1876" height="853" alt="image" src="https://github.com/user-attachments/assets/dade1dbd-0cdf-496b-a596-24afa80e7d6c" />
<img width="1898" height="809" alt="image" src="https://github.com/user-attachments/assets/f527399b-88a6-4938-9fcd-6a967c759d51" />
<img width="1891" height="833" alt="image" src="https://github.com/user-attachments/assets/ed730551-2334-4be8-bf1d-1d2c02bc8dc6" />
<img width="1912" height="843" alt="image" src="https://github.com/user-attachments/assets/8f9b2c44-e1f3-429e-9f36-fd380c977c3e" />
<img width="1896" height="812" alt="image" src="https://github.com/user-attachments/assets/d9a40e60-4cf2-41b6-9bb6-625b0b1dc796" />
<img width="1911" height="838" alt="image" src="https://github.com/user-attachments/assets/eca450ee-6bb7-4780-8479-2b064e973f71" />
<img width="1920" height="820" alt="image" src="https://github.com/user-attachments/assets/16796732-5350-4cd4-8b73-4defa88b6918" />







</div>
