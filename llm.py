import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from fetch_data import setup_chroma_db, fetch_and_store_data

def answer_question(query, collection, fetch_if_empty=True):
    # Check if collection has documents
    count = collection.count()
    if count == 0:
        if fetch_if_empty:
            print("⚠️ Database is empty. Automatically fetching data...")
            success = fetch_and_store_data(query, collection)
            if not success:
                return "Could not retrieve information to answer your question."
            count = collection.count()  # Recheck count after fetching
        else:
            return "No documents found in the database to answer your question."
    
    # Load models
    print("🧠 Loading models...")
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')  # For embeddings
    
    tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    llm_model = AutoModelForCausalLM.from_pretrained(
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        torch_dtype=torch.float16,  # Use half-precision to save memory
        device_map="auto"          # Automatically choose best device
    )
    
    # Generate embedding for the question
    question_embedding = sentence_model.encode(query).tolist()
    
    # Query Chroma DB for top 3 similar summaries
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(3, count),  # Make sure we don't request more than we have
        include=["metadatas", "documents"]
    )
    
    # Check if results are found
    if not results['ids'][0]:
        if fetch_if_empty:
            print("⚠️ No relevant results found. Fetching fresh data...")
            success = fetch_and_store_data(query, collection)
            if not success:
                return "Could not retrieve information to answer your question."
            # Try querying again
            return answer_question(query, collection, fetch_if_empty=False)
        return "No relevant information found to answer your question."
    
    # Extract summaries from the query results
    summaries = []
    sources = []
    
    for i, metadata in enumerate(results['metadatas'][0]):
        summary = metadata.get('summary', results['documents'][0][i])
        source = metadata.get('link', 'Unknown source')
        title = metadata.get('title', 'Unknown title')
        
        summaries.append(summary)
        sources.append(f"{title} ({source})")
    
    # Print sources used
    print("\nSources used:")
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source}")
    
    # Create prompt for TinyLlama (using its chat format)
    context = "\n\n".join(summaries)
    prompt = f"""<|system|>
You are a helpful AI assistant. Answer questions based only on the provided context.

<|user|>
Context:
{context}

Question: {query}

<|assistant|>"""
    
    # Tokenize the prompt
    inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=1024).to(llm_model.device)
    attention_mask = (inputs != tokenizer.pad_token_id).long()  # Create attention mask

    # Generate answer using TinyLlama
    print("💭 Generating answer...")
    with torch.no_grad():
        outputs = llm_model.generate(
            inputs,
            attention_mask=attention_mask,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    
    # Decode the output
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract the answer (everything after the last assistant tag)
    try:
        answer = response.split("<|assistant|>")[-1].strip()
    except IndexError:
        answer = response

    return answer

def main():
    parser = argparse.ArgumentParser(description='Query the LLM with auto-scraping capability')
    parser.add_argument('--query', type=str, help='The question to answer')
    parser.add_argument('--no-autofetch', action='store_true', help='Disable auto-fetching of data')
    args = parser.parse_args()
    
    # Set up the database
    client, collection = setup_chroma_db()
    
    # If no query provided, ask for one
    query = args.query if args.query else input("Enter your question: ")
    
    # Answer the question (with auto-fetch if enabled)
    print("\n📝 Generating answer to your question...")
    answer = answer_question(query, collection, fetch_if_empty=not args.no_autofetch)
    
    # Print the answer
    print("\n🤖 Answer:")
    print(answer)
    
    # Print source info
    print("\nSources: Check the output above for the sources used to generate this answer.")

if __name__ == "__main__":
    main()