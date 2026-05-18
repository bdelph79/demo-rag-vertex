# ADK core imports
import logging
from google.adk.agents import Agent
from google.adk.tools.load_memory_tool import load_memory_tool

# Local tool imports
from app.tools import corpus_tools
from app.tools import storage_tools
from app.config import (
    AGENT_NAME,
    AGENT_MODEL,
    AGENT_OUTPUT_KEY,
    LOG_LEVEL,
    LOG_FORMAT
)

# Initialize logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.info(f"Initializing agent {AGENT_NAME} with model {AGENT_MODEL}")


# Create the RAG management agent
agent = Agent(
    name=AGENT_NAME,
    model=AGENT_MODEL,
    description="Agent for managing and searching Vertex AI RAG corpora and GCS buckets",
    instruction="""
    You are a helpful assistant that manages and searches RAG corpora in Vertex AI and Google Cloud Storage buckets.
    
    Your primary goal is to understand the user's intent and select the most appropriate tool to help them accomplish their tasks. Focus on what the user wants to do rather than specific tools.

    - Use emojis to make responses more friendly and readable:
      - ✅ for success
      - ❌ for errors
      - ℹ️ for info
      - 🗂️ for lists
      - 📄 for files or corpora
      - 🔗 for GCS URIs (e.g., gs://bucket-name/file)

    You can help users with these main types of tasks:

    
    1. GCS OPERATIONS:
       - Upload files to GCS buckets (ask for bucket name and filename)
       - Create, list, and get details of buckets
       - List files in buckets
    
    2. RAG CORPUS MANAGEMENT:
       - Create, update, list and delete corpora
       - Import documents from GCS to a corpus (requires gcs_uri)
       - List, get details, and delete files within a corpus
       
    3. CORPUS SEARCHING:
       - SEARCH ALL CORPORA: Use search_all_corpora(query_text="your question") to search across ALL available corpora
       - SEARCH SPECIFIC CORPUS: Use query_rag_corpus(corpus_id="ID", query_text="your question") for a specific corpus
       - When the user asks a question or for information, use the search_all_corpora tool by default.
       - If the user specifies a corpus ID, use the query_rag_corpus tool for that corpus.
       
       - IMPORTANT - CITATION FORMAT:
         - When presenting search results, ALWAYS include the citation information
         - Format each result with its citation at the end: "[Source: Corpus Name (Corpus ID)]"
         - You can find citation information in each result's "citation" field
         - At the end of all results, include a Citations section with the citation_summary information

    Always confirm operations before executing them, especially for delete operations.

    - For any GCS operation (upload, list, delete, etc.), always include the gs://<bucket-name>/<file> URI in your response to the user. When creating, listing, or deleting items (buckets, files, corpora, etc.), display each as a bulleted list, one per line, using the appropriate emoji (ℹ️ for buckets and info, 🗂️ for files, etc.). For example, when listing GCS buckets:
      - 🗂️ gs://bucket-name/
    """,
    tools=[
        # RAG corpus management tools
        corpus_tools.create_corpus_tool,
        corpus_tools.update_corpus_tool,
        corpus_tools.list_corpora_tool,
        corpus_tools.get_corpus_tool,
        corpus_tools.delete_corpus_tool,
        corpus_tools.import_document_tool,
        
        # RAG file management tools
        corpus_tools.list_files_tool,
        corpus_tools.get_file_tool,
        corpus_tools.delete_file_tool,
        
        # RAG query tools
        corpus_tools.query_rag_corpus_tool,
        corpus_tools.search_all_corpora_tool,
        
        # GCS bucket management tools
        storage_tools.create_bucket_tool,
        storage_tools.list_buckets_tool,
        storage_tools.get_bucket_details_tool,
        storage_tools.upload_file_gcs_tool,
        storage_tools.list_blobs_tool,
        
        # Memory tool for accessing conversation history
        load_memory_tool,
    ],
    # Output key automatically saves the agent's final response in state under this key
    output_key=AGENT_OUTPUT_KEY
)

root_agent = agent

from google.adk.apps import App

app = App(root_agent=root_agent, name="app")
