import chromadb
from llama_index.core import Document, StorageContext, VectorStoreIndex, Settings
from llama_index.core.node_parser import LangchainNodeParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding # Add this

class DataIngestor:
    def __init__(self, model_name="llama3"):
        # Configure LlamaIndex to use local Ollama for embeddings
        Settings.embed_model = OllamaEmbedding(model_name=model_name)
        
        # Initialize Persistent ChromaDB
        self.db = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.db.get_or_create_collection("compliance_vault")
        self.vector_store = ChromaVectorStore(chroma_collection=self.collection)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

    def process_policy(self, text, metadata):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " "]
        )
        parser = LangchainNodeParser(splitter)
        
        doc = Document(text=text, metadata=metadata)
        nodes = parser.get_nodes_from_documents([doc])
        
        # This will now use Ollama for vector generation
        index = VectorStoreIndex(nodes, storage_context=self.storage_context)
        return index