import os
from typing import List
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.vectorstores import VectorStore, Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.schema import Document
from git import Repo

from sniff import sniff_github

REPO_PATH = "out/ohmyzsh-wiki"
OHMYZSH_WIKI_URL = "https://github.com/ohmyzsh/wiki"
PRESISTENT_PATH = ".vdb"
DEBUG = True

memory = None

load_dotenv()

DEBUG = True
def logd(msg):
    if DEBUG:
        print('Debug: ' + msg)
class Memory: 
    _instance = None
    vectordb = None

    def __init__(self):
        if self._instance is not None:
            raise Exception("Memory is a singleton")
        else:
            Memory._instance = self
            self.update_memory()
    
    @staticmethod
    def get_instance():
        if Memory._instance is None:
            Memory()
        return Memory._instance

    def query(self, query, with_sources=False):
        if self.vectordb is None:
            self.vectordb = Chroma(persist_directory=PRESISTENT_PATH, embedding_function=OpenAIEmbeddings())

        context_docs = self.vectordb.as_retriever().get_relevant_documents(query)
        logd(f"Found {len(context_docs)} relevant documents")
        answer = ""
        if with_sources:
            chain = load_qa_with_sources_chain(llm=OpenAI(), chain_type="stuff")
            answer = chain({"input_documents": context_docs[:2], "question": query}, return_only_outputs=True)
        else:
            answer = load_qa_chain(llm=OpenAI(), chain_type="stuff").run(input_documents=context_docs, question=query)

        return answer
    
    def update_memory(self):
        docs = sniff_github(repo_path=REPO_PATH, 
                            clone_url=OHMYZSH_WIKI_URL, 
                            branch="main", 
                            use_markdown_loader=True,
                            file_filter=lambda x: x.endswith(".md"))
        logd(f'Loaded {len(docs)} documents from {OHMYZSH_WIKI_URL}')
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        doc_chunks = text_splitter.split_documents(docs)
        self._embed_documents(doc_chunks)
        if DEBUG:
            print(f"[[Memory Update]]. Added {len(doc_chunks)} vectors to the vector store.")

    ## Private methods
    def _embed_documents(self, docs: List[Document]):
        self.vectordb = Chroma.from_documents(documents=docs, 
                                              embedding=OpenAIEmbeddings(), 
                                              persist_directory=PRESISTENT_PATH)
        if PRESISTENT_PATH:
            self.vectordb.persist()
        
def get_memory():
    global memory
    if memory is None:
        return Memory.get_instance()
    else:
        return memory

def main():
    query = "how to install ohmyzsh"
    memory = Memory.get_instance()
    answer = memory.query("how to install ohmyzsh", with_sources=True)
    print(f'Question: {query}\nAnswer: {answer}')
    # print(memory.vectordb.similarity_search("how to install ohmyzsh", k=2))

if __name__ == "__main__":
    main()