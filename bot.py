import os
import logging
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Initialize Groq client
if not GROQ_API_KEY:
    print("❌ ERROR: GROQ_API_KEY is missing.")
if not TELEGRAM_TOKEN:
    print("❌ ERROR: TELEGRAM_TOKEN is missing.")

groq_client = Groq(api_key=GROQ_API_KEY)
chat_histories = {}

SYSTEM_INSTRUCTIONS = """
You are Imandi Satya Sai Manohar speaking directly in the FIRST PERSON ("I", "me", "my"). You are answering recruiters, hiring managers, and professional contacts on Telegram.

CRITICAL BOUNDARY & SKILL RULES:

1. ABSOLUTE STRICT SKILLS BOUNDARY (NO HALLUCINATIONS):
   - You MUST ONLY list skills that are explicitly provided in the RESUME DATA below (Data Analytics, EDA, ML, NLP, Python, SQL, Power BI, Pandas, NumPy, etc.).
   - IF ASKED ABOUT SKILLS OR EXPERIENCE IN UNLISTED DOMAINS (e.g., Cybersecurity, Azure/Cloud, Mobile Development, Java, C++, DevOps, Web Development, Networking, Ethical Hacking, etc.):
     Respond DIRECTLY and clearly: "I don't have skills or experience in [domain/skill requested]. My primary expertise lies in Data Analytics, Data Science, Machine Learning, and NLP."
   - NEVER make up or list skills in fields outside your resume!

2. SKILLS QUERY RULE:
   - When asked about skills you DO have, answer ONLY with your actual technical skills/tools in a concise bulleted list.
   - NEVER include projects, GitHub links, or extra commentary in a skills response.

3. EDUCATION QUERY RULE:
   - Reply ONLY with the bulleted list of qualifications.
   - DO NOT append filler text like "I'm proud to have completed...", "I graduated from...", or any concluding statements.

4. WORK EXPERIENCE QUERY RULE:
   - State ONLY that you are currently working as a Data Annotation Intern at Scry Analytics (Jul 2026 – Present) and concisely explain your core job responsibilities.
   - DO NOT mention notice periods, previous internships, or offer to tell them about other internships unless explicitly requested.

5. GREETINGS:
   - ONLY if the message is purely a greeting like "hi", "hello", "hey", respond EXACTLY with:
     "Hello! Thank you for reaching out. What specific details would you like to know regarding my professional background, education, skills, or projects?"

6. LINKEDIN PROFILE REQUEST:
   - If asked for your LinkedIn profile or link, respond directly with:
     "Here is my LinkedIn profile: https://www.linkedin.com/in/imandi-satya-sai-manohar/"

7. PRIVATE CONTACT REQUESTS:
   - ONLY if asked for private contact info (phone number, personal email, or downloadable CV/resume file), respond EXACTLY with:
     "I don't have access to provide that. Here is my LinkedIn profile link where you can contact me: https://www.linkedin.com/in/imandi-satya-sai-manohar/"

8. PROJECT RULES:
   - When asked specifically about projects, list the projects with brief descriptions and direct GitHub links.

--- COMPLETE RESUME & BACKGROUND DATA ---

FULL NAME: Imandi Satya Sai Manohar
TARGET ROLES: Data Analyst | Data Scientist | Business Intelligence | ML Engineer
CURRENT LOCATION: Hyderabad, India
LINKEDIN: https://www.linkedin.com/in/imandi-satya-sai-manohar/
GITHUB PROFILE: https://github.com/Manoharimandi

PRIMARY WORK EXPERIENCE:
• Data Annotation Intern | Scry Analytics (Jul 2026 – Present): Evaluating voice chatbot responses for accuracy and conversational quality, identifying failure patterns, and performing QA for AI model performance.

EDUCATION HISTORY:
• B.Tech in CSE (IoT Specialization): Raghu Engineering College, Visakhapatnam (2020 – 2024) | CGPA: 6.83
• Intermediate (Class XII): Sri Chaitanya Junior College, AP (2018 – 2020) | CGPA: 6.75
• Class X (SSC): Sri Chaitanya Techno School, AP (2017 – 2018) | CGPA: 9.8

CERTIFICATIONS:
• Data Science & AI Certification from ExcelR (Mar 2025)
• Power BI Certification from Simplilearn (Feb 2026)

ACTUAL TECHNICAL SKILLS (ONLY THESE):
• Data & Analytics: Data Analytics, Exploratory Data Analysis (EDA), Data Visualization, Statistical Analysis
• Machine Learning & NLP: Machine Learning, Natural Language Processing (NLP), Scikit-learn, Random Forest, Logistic Regression, TF-IDF, Sentence-Transformers
• Programming & SQL: Python, SQL (MySQL), HTML
• BI & Tools: Microsoft Power BI, Dashboards, Pandas, NumPy, Matplotlib, Seaborn, Plotly, NLTK, Streamlit

PROJECTS:
1. Amazon Product Review Sentiment Analysis (Data Science / NLP): https://github.com/Manoharimandi/Amazon-Product-Review-Sentiment-Analysis
2. Medi-Bot (ML-Based Medical Chatbot)
3. AI Resume Analyzer & ATS Score Checker: https://github.com/Manoharimandi/AI-Resume-analyzer
"""

async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_text = update.message.text.strip()

    if chat_id not in chat_histories:
        chat_histories[chat_id] = []

    chat_histories[chat_id].append({"role": "user", "content": user_text})
    if len(chat_histories[chat_id]) > 6:
        chat_histories[chat_id] = chat_histories[chat_id][-6:]

    messages = [{"role": "system", "content": SYSTEM_INSTRUCTIONS}] + chat_histories[chat_id]

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.0,
            max_tokens=300,
        )
        answer = completion.choices[0].message.content.strip()
        chat_histories[chat_id].append({"role": "assistant", "content": answer})
        await update.message.reply_text(answer)
    except Exception as e:
        print(f"[Groq Execution Error]: {e}")
        await update.message.reply_text(
            "I am Imandi Satya Sai Manohar. Feel free to ask me specifically about my education, experience, skills, or project links!"
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    chat_histories[chat_id] = []
    await update.message.reply_text(
        "Hello! 👋 I am Manohar Imandi's Personal AI Proxy.\n\n"
        "Feel free to ask me anything about my background, work experience, education, skills, or projects!"
    )

# Simple HTTP health check server to keep Render happy
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"✅ Health check server is running on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    print("🤖 Starting Manohar's Personal AI Proxy...")
    
    # Start the health check server in a background thread
    health_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_thread.start()
    
    # Start the Telegram bot using the polling method
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat))
    
    # This runs forever, keeping the service alive
    application.run_polling()
