import os
import json
import pandas as pd
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.schema import Document, AIMessage
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class ProductRecommender:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0)
        self.db = None
        self.df = pd.read_csv(csv_path)
        
        self._preprocess_data()
        self._create_vector_db()
        
    def _preprocess_data(self):
        """Combine all columns except URL into text column"""
        text_columns = [col for col in self.df.columns if col != 'url']
        
        self.df['combined_text'] = self.df[text_columns].apply(
            lambda row: ' '.join(row.values.astype(str)), axis=1
        )
        
        bool_columns = ['adaptive_irt', 'remote_testing']
        for col in bool_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].replace({1: 'Yes', 0: 'No'})


    def _create_vector_db(self):
        """Create vector database with metadata"""
        documents = [
            Document(
                page_content=row['combined_text'],
                metadata={
                    'url': row['url'],
                    'adaptive_irt': row.get('adaptive_irt', 'No'),
                    'description': row['description'],
                    'duration': row['duration'],
                    'remote_testing': row.get('remote_testing', 'No'),
                    'test_type': row['test_type']
                }
            ) for _, row in self.df.iterrows()
        ]
        self.db = FAISS.from_documents(documents, self.embeddings)
        
    def _format_output(self, docs):
        """Convert documents to specified JSON format"""
        results = []
        for doc in docs:
            meta = doc.metadata
            results.append({
                "url": meta['url'],
                "adaptive_support": meta['adaptive_irt'],
                "description": meta['description'],
                "duration": int(meta['duration']),
                "remote_support": meta['remote_testing'],
                "test_type": self._parse_test_types(meta['test_type'])
            })
        return {"recommended_assessments": results}
    
    def _parse_test_types(self, test_type_str):
        """Convert test type string to list"""
        if isinstance(test_type_str, str):
            return [t.strip() for t in test_type_str.split(',')]
        return []
        
    def llm_enhanced_recommendation(self, query, k=5):
        """LLM-powered recommendation with natural language processing"""
        prompt_template = PromptTemplate(
            input_variables=["context", "query"],
            template=(
                """
                Given the following user query and product context, format the response as JSON:

                Query: {query}

                Context: {context}

                Format response with:
                - 'recommended_assessments' array
                - Each entry should have: url, adaptive_support, description, duration, remote_support, test_type
                - duration as integer
                - test_type as array
                - adaptive_support and remote_support as 'Yes'/'No'
                """
            )
        )
        
        context_docs = self.db.similarity_search(query, k=k)
        context = "\n\n".join([d.page_content for d in context_docs])
        
        chain = prompt_template | self.llm
        response = chain.invoke({"query": query, "context": context})

        if isinstance(response, AIMessage):
            response = response.content

        if isinstance(response, str):
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {"error": "Failed to decode response"}
        elif isinstance(response, dict):
            return response
        else:
            return {"error": "Invalid response structure"}
    def recommend_simple(self, query, k=5):
        """Simple similarity-based recommendation without LLM"""
        context_docs = self.db.similarity_search(query, k=k)
        return self._format_output(context_docs)


if __name__ == "__main__":
    recommender = ProductRecommender("product_catalog.csv")
    
    advanced_results = recommender.llm_enhanced_recommendation(
        "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes. "
    )
    print(type(advanced_results))
    print(advanced_results)
    
    print(json.dumps(advanced_results, indent=2))
