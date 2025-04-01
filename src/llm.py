from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def setup_llm():
    """Initialize the LLM via HuggingFaceHub with specified parameters."""
    return HuggingFaceHub(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        model_kwargs={
            "max_new_tokens": 512,
            "temperature": 0.2,  # Lower temperature for more deterministic responses
            "repetition_penalty": 1.1,
            "return_full_text": False
        }
    )

def setup_prompt_template():
    """Create a prompt template and output parser for the chain."""
    template = (
        "<|system|>\n"
        "You are a helpful and precise AI Assistant for Partido State University. Your goal is to accurately provide information from the Citizen Charter of Partido State University.\n"
        "Answer the user’s query based only on the provided CONTEXT.\n"
        "CONTEXT: {context}</s>\n"  # {context} will be dynamically replaced by retrieved documents
        "<|user|> {query} </s>\n"  # {query} is the user's question
        "<|assistant|>"  # Assistant’s response
    )
    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()
    return prompt, output_parser

def assemble_chain(retriever, prompt, llm, output_parser):
    """Assemble the chain using retriever, prompt, LLM, and output parser."""
    return (
        {"context": retriever, "query": RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )