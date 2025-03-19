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
   git clone https://github.com/Prajvinsharan/integrated-rag-system.git
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



## ** Example Output/Usage**

Below is a sample output from running the script `llm.py` when asked, "Who won the 2025 Champions Trophy final?":

```plaintext
Users\prajv\Downloads\rag> python llm.py
Enter your question: who won the 2025 champions trophy final 

📝 Generating answer to your question...
⚠️ Database is empty. Automatically fetching data...
🔍 Searching for: 'who won the 2025 champions trophy final '
✅ Scraping and preprocessing text from websites... please wait
1. 2025 ICC Champions Trophy - Wikipedia
   Link: https://en.wikipedia.org/wiki/2025_ICC_Champions_Trophy
   Snippet: India became the champions by defeating New Zealand in the final and also became the first team to w...
📄 Scraping: https://en.wikipedia.org/wiki/2025_ICC_Champions_Trophy
✅ Extracted Summary: Ninth edition of the ICC Champions Trophy Cricket tournament The 2025 ICC Champions Trophy was the n...
✅ Summary stored in DB for: 2025 ICC Champions Trophy - Wikipedia
2. ICC Champions Trophy, 2025 schedule, live scores and results ...
   Link: https://www.cricbuzz.com/cricket-series/9325/icc-champions-trophy-2025/matches
   Snippet: ICC Champions Trophy, 2025 Schedule, Match Timings, Venue Details, Upcoming Cricket Matches and Rece...
📄 Scraping: https://www.cricbuzz.com/cricket-series/9325/icc-champions-trophy-2025/matches
✅ Extracted Summary: Team All New Zealand Pakistan Bangladesh India South Africa Afghanistan England Australia Venues All...
✅ Summary stored in DB for: ICC Champions Trophy, 2025 schedule, live scores and results ...
3. ICC Champions Trophy - Wikipedia
   Link: https://en.wikipedia.org/wiki/ICC_Champions_Trophy
   Snippet: India (2002,2013,2025) is the most successful team with three titles, Australia (2006,2009) has won ...
📄 Scraping: https://en.wikipedia.org/wiki/ICC_Champions_Trophy
✅ Extracted Summary: International ODI cricket tournament Cricket tournament The ICC Champions Trophy, formerly known as ...
✅ Summary stored in DB for: ICC Champions Trophy - Wikipedia
4. Official fixtures announced for ICC Men's Champions Trophy 2025
   Link: https://www.icc-cricket.com/tournaments/champions-trophy-2025/news/official-fixtures-announced-for-icc-champions-trophy-2025
   Snippet: Dec 24, 2024 ... The ICC Champions Trophy 2025 fixtures and groupings have been announced by the ICC...
📄 Scraping: https://www.icc-cricket.com/tournaments/champions-trophy-2025/news/official-fixtures-announced-for-icc-champions-trophy-2025
❌ Skipping invalid page: https://www.icc-cricket.com/tournaments/champions-trophy-2025/news/official-fixtures-announced-for-icc-champions-trophy-2025
❌ Failed to scrape https://www.icc-cricket.com/tournaments/champions-trophy-2025/news/official-fixtures-announced-for-icc-champions-trophy-2025
5. ICC Champions Trophy 2025 final: India beat New Zealand by four ...
   Link: https://www.aljazeera.com/sports/2025/3/9/icc-champions-trophy-2025-final-india-beats-new-zealand-by-four-wickets
   Snippet: Mar 9, 2025 ... ICC Champions Trophy 2025 final: India beat New Zealand by four wickets. India overc...
📄 Scraping: https://www.aljazeera.com/sports/2025/3/9/icc-champions-trophy-2025-final-india-beats-new-zealand-by-four-wickets
✅ Extracted Summary: ICC Champions Trophy 2025 final: India beat New Zealand by four wicketsIndia overcome New Zealand’s ...
✅ Summary stored in DB for: ICC Champions Trophy 2025 final: India beat New Zealand by four ...
✅ Preprocessed text saved to 'preprocessed_text.txt'
✅ Successfully added 4 documents to DB
🧠 Loading models...

Sources used:
1. 2025 ICC Champions Trophy - Wikipedia (https://en.wikipedia.org/wiki/2025_ICC_Champions_Trophy)
2. ICC Champions Trophy 2025 final: India beat New Zealand by four ... (https://www.aljazeera.com/sports/2025/3/9/icc-champions-trophy-2025-final-india-beats-new-zealand-by-four-wickets)
3. ICC Champions Trophy - Wikipedia (https://en.wikipedia.org/wiki/ICC_Champions_Trophy)
💭 Generating answer...

🤖 Answer:
Answer: India defeated New Zealand by four wickets in the 2025 Champions Trophy final in Dubai.

Sources: Check the output above for the sources used to generate this answer.



## Why Some Websites Were Not Scraped

In the sample output above, you’ll notice that one website (`https://www.icc-cricket.com/tournaments/champions-trophy-2025/news/official-fixtures-announced-for-icc-champions-trophy-2025`) was skipped, as indicated by the messages "❌ Skipping invalid page" and "❌ Failed to scrape." This happens because the system respects the `robots.txt` file of websites. The `robots.txt` file is a standard used by website owners to instruct web crawlers and scrapers about which parts of the site they are allowed to access. If a website’s `robots.txt` disallows scraping for certain pages or the entire site, the system skips those pages to comply with these restrictions. This ensures ethical scraping practices and adherence to the website’s policies.


⭐ **If you find this project useful, don't forget to give it a star!** ⭐
