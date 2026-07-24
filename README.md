# 🤖 Interactive AI Profile Proxy

An intelligent, real-time Telegram AI bot that acts as a 24/7 personal recruiter assistant for **Imandi Satya Sai Manohar**. Built using **Python**, **Groq API (Llama 3.1)**, **python-telegram-bot**, and hosted on **Render**.

---

## 🌟 Try It Live

[![Telegram](https://img.shields.io/badge/Telegram-Chat_with_AI_Proxy-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/My_ProfileAssistant_bot)

Click above or search for **`@My_ProfileAssistant_bot`** on Telegram to ask about my technical skills, projects, education, or work experience!

---

## 🛠️ Key Features

* **Strict Boundary Control:** Configured with deterministic system instructions (`temperature=0.0`) to prevent hallucinations and restrict responses strictly to verified technical domains.
* **Context Awareness:** Maintains rolling conversation memory per user session for natural, context-aware interactions.
* **First-Person Persona:** Responds directly as Imandi Satya Sai Manohar to professional queries.
* **Cloud-Native Deployment:** Runs 24/7 as a containerized service with an integrated HTTP health-check server.

---

## 🏗️ Architecture & Tech Stack

* **Language:** Python 3
* **LLM Engine:** Groq API (`llama-3.1-8b-instant`)
* **Bot Framework:** `python-telegram-bot`
* **Concurrency:** `asyncio` & Python `threading` (HTTP Health Checker)
* **Hosting:** Render Web Service

---

## 🚀 Local Setup & Installation

### 1. Clone the repository
```bash
git clone [https://github.com/Manoharimandi/My-Profile-Assistant.git](https://github.com/Manoharimandi/My-Profile-Assistant.git)
cd My-Profile-Assistant
