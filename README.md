# SHL Product Recommender

A full-stack AI-powered product recommendation system that suggests SHL assessments based on user queries.

## 🔗 Live Demo

🌐 Frontend: [https://shl-frontend-two.vercel.app](https://shl-frontend-two.vercel.app)  
🔌 API Health Check: [https://shl-assignment-r7vz.onrender.com/health](https://shl-assignment-r7vz.onrender.com/health)

---

## 🚀 API Endpoints

| Endpoint     | Method | Description                                  | Link                                                                  |
|--------------|--------|----------------------------------------------|-----------------------------------------------------------------------|
| `/recommend` | POST   | Returns assessment recommendations           | https://shl-assignment-r7vz.onrender.com/recommend                    |
| `/health`    | GET    | Health check for the backend                 | https://shl-assignment-r7vz.onrender.com/health                       |

---

## 🧠 Approach

The goal was to build an AI-powered product recommendation tool that intelligently suggests SHL assessments based on a user's hiring or evaluation needs. The solution is designed to be scalable, fast, and human-like in its understanding of natural language queries.

### 📌 Step-by-Step Approach

1. **Data Collection (Web Scraping)**  
   - Scraped SHL's official product catalog from: `https://www.shl.com/solutions/products/product-catalog/`
   - Captured details like:
     - Product Name
     - URL
     - Remote Testing Support
     - Adaptive IRT Support
     - Test Types (Cognitive, Personality, etc.)
     - Completion Time (scraped from individual product detail pages)
     - Description (scraped from detail pages for context)

2. **Preprocessing**
   - Cleaned and standardized fields (e.g., boolean fields converted to "Yes"/"No")
   - Combined relevant fields into a single `combined_text` column for semantic embedding

3. **Vectorization**
   - Used OpenAI embeddings (`text-embedding-ada-002`) via Langchain
   - Stored the embeddings using FAISS for fast similarity-based retrieval

4. **Recommendation Engine**
   - **Simple Mode**: Uses FAISS to return top k similar documents
   - **LLM-Enhanced Mode**: Sends the query and context to GPT-4 using Langchain’s `ChatOpenAI`, and prompts the model to return a clean JSON with structured product recommendations

---

## 🔍 Scraping Details

- **Libraries Used**: `requests`, `BeautifulSoup`, `concurrent.futures`, `re`
- **Pagination**: Crawled through multiple pages of both pre-packaged and individual assessment types using pagination query parameters.
- **Parallelism**: Used `ThreadPoolExecutor` to scrape product detail pages (for duration and description) concurrently for faster execution.
- **Regex Matching**: Duration extracted using pattern recognition from raw page text (e.g., "Completion time is approximately 40 minutes").
- **Export**: All scraped data saved as `product_catalog.csv` which is then used for embedding and recommendation.

---

## 📦 Backend

### 🛠 Tech Stack

- **FastAPI** for API development  
- **Langchain + OpenAI** for LLM-enhanced recommendations  
- **FAISS** for semantic search  
- **Pandas** for data handling  
- **BeautifulSoup** for scraping SHL's product catalog

### 📁 Features

- Scrapes SHL's full assessment catalog
- Extracts metadata like duration, description, remote/adaptive support, etc.
- Stores vector embeddings using FAISS
- Supports both:
  - Simple similarity-based search
  - LLM-enhanced natural language recommendations


## 💻 Frontend

### 🛠 Tech Stack

- **React** with **Vite**  
- **TailwindCSS** for styling  
- **Axios** for API integration  
- **Deployed via Vercel**

### 🧠 Features

- Input bar for natural language queries
- Displays recommended assessments in a clean UI
- Shows description, duration, test types, remote/adaptive support, and direct URLs

---

## 📂 Repositories

- 🔧 Backend: This is the backend repo
- 🖥 Frontend: [github.com/1aryantyagi/SHL_frontend](https://github.com/1aryantyagi/SHL_frontend)

---

## 📌 Example Query

> “I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.”

🔎 Output:
- JSON response with top recommended assessments matching the query  
- Includes structured data: URL, description, duration, test types, etc.

---

## 🧪 Local Setup

```bash
# Clone frontend
git clone https://github.com/1aryantyagi/SHL_frontend
cd SHL_frontend
npm install
npm run dev
```


---
## 🤝 Contributions

Feel free to fork and improve. Suggestions and PRs are welcome!
