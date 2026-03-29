# CompliAgent Local Multi Agent Compliance Auditor

## Overview

CompliAgent is a local AI powered compliance auditing system built using a multi agent architecture. It leverages retrieval augmented generation (RAG) with local large language models via Ollama to analyze bank policies and answer compliance related queries.

The system ensures that generated answers are validated against source documents using an internal critic agent, making it suitable for high trust environments like banking and finance.

## Features

* Fully local execution using Ollama (no API key required)
* Multi agent workflow with researcher, generator, and critic roles
* Retrieval augmented generation using vector search
* Context grounded responses with verification loop
* Persistent vector database using ChromaDB
* Streamlit based interactive interface
* Source attribution for transparency
* Model selection support (llama3, mistral, phi3)

## Tech Stack

* Programming Language: Python
* LLM Framework: LangChain
* Indexing Framework: LlamaIndex
* Embeddings: Ollama Embeddings
* Vector Database: ChromaDB
* Frontend: Streamlit

## Architecture

The system consists of the following components:

1. Data Ingestion

   * Splits policy documents into chunks
   * Converts text into embeddings using Ollama
   * Stores vectors in ChromaDB

2. Retrieval

   * Fetches top relevant chunks based on query similarity

3. Generator Agent

   * Uses LLM to generate answers based on retrieved context

4. Critic Agent

   * Verifies whether the generated answer is grounded in context
   * Outputs VERIFIED or REJECTED with reason

## Dataset / Input

* Input is unstructured bank policy text
* Metadata includes source information for traceability

## Installation

Step 1: Clone the repository

git clone
cd compliagent

Step 2: Install dependencies

pip install langchain langchain-core langchain-ollama llama-index chromadb streamlit

Step 3: Install and run Ollama

Download Ollama and pull required models

ollama pull llama3
ollama pull mistral
ollama pull phi3

Ensure Ollama is running locally before starting the application

## Execution Instructions

Step 1: Run the Streamlit application

streamlit run app.py

Step 2: Ingest policy documents

* Paste bank policy text in the sidebar
* Click "Index Documents" to generate embeddings

Step 3: Ask compliance queries

* Enter a query in the chat input
* System retrieves context, generates answer, and verifies it

## Project Structure

* src/

  * ingestion/

    * processor.py
  * agents/

    * auditor.py
* chroma_db/
* app.py
* README.md

## How the System Works

The system follows a multi agent pipeline:

1. Researcher retrieves relevant context from vector database
2. Generator creates an answer using the retrieved context
3. Critic verifies whether the answer is fully grounded

Final Output includes:

* Generated answer
* Verification status (VERIFIED or REJECTED)
* Source references

## Example Workflow

1. Input: Bank policy text
2. Query: "What are the KYC requirements?"
3. Output:

   * Answer generated from policy
   * Verification result
   * Source attribution

## Future Improvements

* Add support for document uploads (PDF, DOCX)
* Enhance critic with multi step reasoning
* Integrate role based access control
* Deploy as enterprise API service
* Add logging and audit trails

## License

This project is licensed under the MIT License

## Acknowledgements

* LangChain for agent orchestration
* LlamaIndex for indexing and retrieval
* Ollama for local LLM inference
* ChromaDB for vector storage
* Streamlit for UI framework
