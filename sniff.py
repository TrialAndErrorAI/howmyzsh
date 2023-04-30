import os
from git import Blob, Repo 
from typing import List
from langchain.schema import Document
from langchain.document_loaders import UnstructuredMarkdownLoader

DEBUG = True
def logd(msg):
    if DEBUG:
        print(f'Debug: {msg}')

"""_summary_
    Loads files from a Git repository into a list of documents.             
"""
def _clone_or_load(repo_path, branch, clone_url, file_filter): 
    if os.path.exists(os.path.join(repo_path, '.git')):
        repo = Repo(repo_path)
        repo.remotes.origin.pull()
        logd('Debug: Repo Loaded from path. ' + repo.git.working_dir)
    elif clone_url:
        repo = Repo.clone_from(clone_url, repo_path)
        logd('Repo Cloned at ' + repo.git.working_dir)
    else :
        raise ValueError(f"No git repo at path {repo_path}")

    repo.git.checkout(branch)
    
    return repo
    
def sniff_github(repo_path, branch="main", use_markdown_loader=False, clone_url=None, file_filter=None) -> List[Document]:
    logd('sniff_github() ' + str(repo_path) + ' ' + str(branch) + ' ' + str(clone_url) + 'filter=' + str(file_filter is not None)) 
    repo = _clone_or_load(repo_path, branch, clone_url, file_filter)
 
    docs: List[Document] = []
    for item in repo.tree().traverse():
        if not isinstance(item, Blob):
            continue

        file_path = os.path.join(repo_path, item.path)

        ignored_files = repo.ignored([file_path])
        if len(ignored_files):
            continue

        # uses filter to skip files
        if file_filter and not file_filter(file_path):
            continue

        rel_file_path = os.path.relpath(file_path, repo_path)
        logd(rel_file_path)
    
        if use_markdown_loader:
            doc = UnstructuredMarkdownLoader(file_path).load()
            docs.append(doc)
        else:
            doc = _load_file(file_path, rel_file_path)
            if doc:
                docs.append(doc)        

    return docs

def _load_file(file_path, rel_file_path):
    try:
        with open(file_path, "rb") as f:
            content = f.read()
            # file_type = os.path.splitext(item.name)[1]
            file_type = os.path.splitext(file_path)[1]
            file_name = os.path.basename(file_path)

            # loads only text files
            try:
                text_content = content.decode("utf-8")
            except UnicodeDecodeError:
                return None

            metadata = {
                "file_path": rel_file_path,
                "file_name": file_name,
                "file_type": file_type,
            }
            doc = Document(page_content=text_content, metadata=metadata)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    
    return doc

        
def main(): 
    repo_path = "out/ohmyzsh-wiki"
    filter_fn = lambda file_path: file_path.endswith(".md")
    docs = sniff_github(repo_path, clone_url="https://github.com/ohmyzsh/wiki", branch="main", file_filter=filter_fn, use_markdown_loader=True)
    # print first doc
    logd(docs[0])

    
if __name__ == "__main__":
    main()
       