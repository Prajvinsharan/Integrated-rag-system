# **Integrated RAG System – Local LLMs with Up-to-Date Knowledge**

This project is designed to **bridge the gap between locally run LLMs and real-time web knowledge**. Unlike traditional AI models that rely on outdated static datasets, this **Retrieval-Augmented Generation (RAG) system** dynamically searches the web, extracts relevant information, and enhances LLM responses with fresh, up-to-date context—all while running entirely **on your local machine**.

## **Why This Matters**
Most LLMs are limited to the knowledge they were trained on. This system **eliminates that constraint** by:
✅ **Fetching the latest data from the web** instead of relying on old training sets.  
✅ **Running fully locally**—no need for cloud-based APIs or external dependencies.  
✅ **Combining powerful search & retrieval** with AI-driven answers.  

## **How It Works**
1️⃣ **Finds the Best Sources** – Uses **Google Custom Search API** to locate relevant articles.  
2️⃣ **Extracts Clean Data** – Scrapes text from web pages & PDFs, removing ads and clutter.  
3️⃣ **Processes & Organizes Content** – Chunks and embeds text for fast retrieval.  
4️⃣ **Stores Knowledge Locally** – Saves extracted data in **ChromaDB**, a local vector database.  
5️⃣ **Enhances Your Local LLM** – Uses **retrieved context** to generate accurate, up-to-date answers.  

## **Key Features**
🚀 **Run LLMs with current data** – Keep your AI informed without retraining.  
🔍 **Web-enhanced question answering** – Get **real-time, reliable answers** from local models.  
📂 **Works with documents** – Scrapes and processes PDFs & webpages.  
💾 **Fully Local & Privacy-Friendly** – Your data stays on your machine.  
💡 **Optimized for lightweight models** – Works with **TinyLlama-1.1B-Chat**, but adaptable to others.  

## **Installation**
### **Prerequisites**
Ensure you have the following installed:
- Python 3.8+
- Google Custom Search API Key (for web search)
- Required Python libraries

### **Setup**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/integrated-rag-system.git
   cd integrated-rag-system
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   ```bash
   export GOOGLE_API_KEY="your_google_api_key"
   export GOOGLE_CSE_ID="your_custom_search_engine_id"
   ```

## **Usage**
To **search the web and get an AI-generated answer**:
```bash
python main.py --query "What is thrombosis?"
```

To **query locally stored knowledge without searching the web**:
```bash
python main.py --query "What is thrombosis?" --skip-search
```

## **Under the Hood**
- **Google Search API** – Finds relevant web sources  
- **Playwright & BeautifulSoup** – Extracts clean text from web pages  
- **PyPDF2** – Parses PDFs for additional knowledge  
- **ChromaDB** – Stores and retrieves contextual information locally  
- **SentenceTransformers** – Finds the most relevant data using embeddings  
- **TinyLlama-1.1B-Chat** – Provides AI-generated answers with context-aware retrieval  

## **Who Is This For?**
✔️ Developers who want to **enhance their LLMs with real-time data**  
✔️ Researchers who need **accurate, up-to-date insights**  
✔️ Privacy-conscious users who prefer **local AI processing**  


### **Contribute**
1. **Fork the repository**
2. **Create a feature branch**
3. **Submit a pull request**

---
⭐ **If you find this project useful, don't forget to give it a star!** ⭐
