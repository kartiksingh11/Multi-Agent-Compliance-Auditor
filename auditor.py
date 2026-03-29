from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

class ComplianceSystem:
    def __init__(self, model_name="llama3"):
        # No API key needed for local Ollama
        self.llm = ChatOllama(
            model=model_name,
            temperature=0
        )

    def run_audit(self, index, query):
        # 1. Researcher Agent: Retrieve context
        retriever = index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(query)
        context = "\n---\n".join([n.get_content() for n in nodes])
        sources = [n.metadata for n in nodes]

        # 2. Generator: Draft answer
        draft_prompt = f"Using this bank policy context: {context}\n\nAnswer the query: {query}"
        # .invoke().content is the standard for LangChain 0.3+
        draft_response = self.llm.invoke(draft_prompt).content

        # 3. Critic Agent: Verification Loop
        critic_prompt = PromptTemplate.from_template("""
            Role: Senior Compliance Auditor
            Context: {context}
            Answer: {answer}
            
            Task: Verify if the answer is 100% grounded in the context. 
            Output: 'VERIFIED' or 'REJECTED: [Reason]'
        """)
        
        verification = self.llm.invoke(critic_prompt.format(
            context=context, answer=draft_response
        )).content
        
        return draft_response, verification, sources