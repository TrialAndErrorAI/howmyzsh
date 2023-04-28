import os
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.document_loaders import GitLoader
from langchain.vectorstores import VectorStore, Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain

REPO_PATH = "out/ohmyzsh-wiki"
OHMYZSH_WIKI_URL = "https://github.com/ohmyzsh/wiki"
PRESISTENT_PATH = ".vdb"
DEBUG = True

memory = None

print('this is memory.py')
load_dotenv()

class Memory: 
    _instance = None
    vectordb = None

    def __init__(self):
        if self._instance is not None:
            raise Exception("Memory is a singleton")
        else:
            Memory._instance = self
            self.vectordb = self.update_memory()
    
    @staticmethod
    def get_instance():
        if Memory._instance is None:
            Memory()
        return Memory._instance
    


    # TODO - make it singleton and load it once
    def query(self, query):
        if self.vectordb is None:
            self.vectordb = Chroma(persist_directory=PRESISTENT_PATH, embedding_function=OpenAIEmbeddings())

        context_docs = self.vectordb.as_retriever().get_relevant_documents(query)
        chain = load_qa_chain(llm=OpenAI(), chain_type="stuff")
        answer = chain.run(input_documents=context_docs, question=query)

        if DEBUG:
            print(f"Found {len(context_docs)} relevant documents")
            print(f"Answer: {answer}")

        return answer
    
    ## Private methods
    def update_memory(self):
        docs = self._sniff_github(clone_url=None if os.path.exists(REPO_PATH) else OHMYZSH_WIKI_URL, branch="main", file_ext="md")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        doc_chunks = text_splitter.split_documents(docs)
        vectordb = Chroma.from_documents(documents=doc_chunks, embedding=OpenAIEmbeddings(), persist_directory=PRESISTENT_PATH)
        vectordb.persist()
        if DEBUG:
            print(f"[[Memory Update]]. Added {len(doc_chunks)} vectors to the vector store.")
        return vectordb
    
    def _sniff_github(self, clone_url=None, branch="main", file_ext=None):
        loader = GitLoader(repo_path="out/ohmyzsh-wiki",
                        clone_url=clone_url,
                        branch=branch, 
                        file_filter= lambda file_path: file_path.endswith(f".{file_ext}")) if file_ext else None

        documents = loader.load()
        if DEBUG:
            print(f"Found {len(documents)} documents in repo\n")    
        return documents

def get_memory():
    global memory
    if memory is None:
        return Memory.get_instance()
    else:
        return memory

def main():
    memory = Memory.get_instance()
    print(memory.query("how to install ohmyzsh"))

if __name__ == "__main__":
    main()