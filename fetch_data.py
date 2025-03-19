import os
import requests
from playwright.sync_api import sync_playwright
from readability import Document
from bs4 import BeautifulSoup
import PyPDF2
import re
import time
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
import argparse

# Google Search API credentials (replace with your own)
API_KEY = "AIzaSyDr3qaIpGj0wCtvvL2r7T2bZervAd2vy_k"  # Replace with your actual API key
SEARCH_ENGINE_ID = "f26a96103e50049ec"  # Replace with your actual search engine ID

def google_search(query):
    print(f"🔍 Searching for: '{query}'")
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Google API request failed: {response.status_code} - {response.text}")
        return []
    data = response.json()
    if not data.get("items"):
        print("❌ No results found. Printing raw response:")
        print(data)
        return []
    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet", "")
        })
    return results

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    text = re.sub(r'http[s]?://[^\s]+', '', text)  # Remove URLs
    text = re.sub(r'(Share:|Click to copy citation|Page last reviewed)', '', text)  # Remove specific noise
    return text

def scrape_text(url, snippet=None):
    print(f"📄 Scraping: {url}")
    if url.lower().endswith('.pdf'):
        try:
            response = requests.get(url)
            with open('temp.pdf', 'wb') as f:
                f.write(response.content)
            with open('temp.pdf', 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''.join([page.extract_text() or "" for page in reader.pages])
            os.remove('temp.pdf')
            return clean_text(text)
        except Exception as e:
            print(f"❌ Failed to process PDF: {e}")
            return ""

    # Handle HTML with Playwright and readability
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            try:
                page.wait_for_selector('article, main, #content', timeout=10000)
            except:
                pass  # Continue even if selector not found
            content = page.content()
            browser.close()
        except Exception as e:
            print(f"❌ Failed to load page {url}: {e}")
            browser.close()
            return ""

        # Skip non-content pages (e.g., 404 or 403 errors)
        if "not found" in content.lower() or "forbidden" in content.lower() or len(content) < 500:
            print(f"❌ Skipping invalid page: {url}")
            return ""

        # Extract main content using readability
        doc = Document(content)
        main_content = doc.summary()
        soup = BeautifulSoup(main_content, 'html.parser')
        text = soup.get_text()

        # If snippet is provided and found in text, extract surrounding context
        if snippet and snippet in text:
            start = text.find(snippet)
            text = text[max(0, start - 500):start + len(snippet) + 500]

        return clean_text(text)

def extract_key_sentences(text, query, max_sentences=5):
    if not text:
        return ""
        
    sentences = re.split(r'(?<=[.!?]) +', text)
    query_keywords = set(query.lower().split())
    key_sentences = []

    for sentence in sentences:
        sentence_words = set(sentence.lower().split())
        if query_keywords & sentence_words:
            key_sentences.append(sentence)
        if len(key_sentences) >= max_sentences:
            break
            
    # If we didn't find any key sentences, just return the first few sentences
    if not key_sentences and sentences:
        key_sentences = sentences[:min(max_sentences, len(sentences))]

    return ' '.join(key_sentences)

def setup_chroma_db():
    # Set up Chroma
    settings = Settings(persist_directory="./chroma_data")
    client = chromadb.Client(settings)
    
    # Make sure to delete and recreate if needed
    try:
        collection = client.get_or_create_collection("summaries")
    except:
        # If there's an error, try recreating the collection
        try:
            client.delete_collection("summaries")
        except:
            pass
        collection = client.create_collection("summaries")
    
    return client, collection

def store_summary_in_chroma_db(collection, summary, link, title):
    # Make sure summary is not empty
    if not summary.strip():
        print(f"❌ Empty summary for {link}, skipping")
        return False
    
    try:
        # Initialize Sentence Transformer model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Generate embedding
        embedding = model.encode(summary).tolist()
        unique_id = str(uuid.uuid4())
        
        # Add to collection
        collection.add(
            ids=[unique_id],
            metadatas=[{"link": link, "summary": summary, "title": title}],
            embeddings=[embedding],
            documents=[summary]  # Make sure to include document text too
        )
        print(f"✅ Summary stored in DB for: {title}")
        return True
    except Exception as e:
        print(f"❌ Failed to store in Chroma DB: {e}")
        return False

def fetch_and_store_data(query, collection=None):
    # Setup DB if not provided
    if collection is None:
        _, collection = setup_chroma_db()
        
    results = google_search(query)
    if not results:
        return False

    print("✅ Scraping and preprocessing text from websites... please wait")
    all_text = ""
    success_count = 0
    
    for i, result in enumerate(results[:5]):  # Limit to top 5 results
        print(f"{i+1}. {result['title']}")
        print(f"   Link: {result['link']}")
        print(f"   Snippet: {result['snippet'][:100]}...")
        
        # Scrape full text
        text = scrape_text(result['link'], snippet=result['snippet'])
        if text:
            summary = extract_key_sentences(text, query)
            print(f"✅ Extracted Summary: {summary[:100]}...")  # Show only first 100 chars
            all_text += f"\n--- Scraped from {result['link']} ---\n{summary}\n"
            success = store_summary_in_chroma_db(collection, summary, result['link'], result['title'])
            if success:
                success_count += 1
        else:
            print(f"❌ Failed to scrape {result['link']}")
        time.sleep(1)  # Delay to avoid rate limiting

    # Save Preprocessed Text to File
    if all_text.strip():
        with open("preprocessed_text.txt", "w", encoding="utf-8") as f:
            f.write(all_text)
        print(f"✅ Preprocessed text saved to 'preprocessed_text.txt'")
        print(f"✅ Successfully added {success_count} documents to DB")
        return success_count > 0
    else:
        print("❌ No valid text was extracted.")
        return False

def main():
    parser = argparse.ArgumentParser(description='Search, scrape, and summarize web content')
    parser.add_argument('--query', type=str, help='The query to search for')
    args = parser.parse_args()
    
    # Set up the database
    client, collection = setup_chroma_db()
    
    # If no query provided, ask for one
    query = args.query if args.query else input("Enter your search query: ")
    
    # Fetch and store data
    success = fetch_and_store_data(query, collection)
    
    if success:
        print("\n✅ Done! Data has been processed and stored in the database.")
    else:
        print("\n❌ Failed to retrieve and store data.")

if __name__ == "__main__":
    main()