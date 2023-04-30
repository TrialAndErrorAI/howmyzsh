import os
from typing import List
from langchain.schema import Document
from langchain.document_loaders import UnstructuredMarkdownLoader

DEBUG = True

def logd(msg):
    if DEBUG:
        print('Debug: ' + msg)

def sniff_github(repo_path, branch="main", clone_url=None, file_filter=None) -> List[Document]:
    # print while taking care of None type 
    logd('sniff_github() ' + str(repo_path) + ' ' + str(branch) + ' ' + str(clone_url) + ' ' + str(file_filter))
    try: 
        from git import Blob, Repo  # type: ignore
    except ImportError as ex:
        raise ImportError(
            "Could not import git python package. "
            "Please install it with `pip install GitPython`."
        ) from ex

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
    
    docs: List[Document] = []
    for item in repo.tree().traverse():
        logd(item.path)
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
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                file_type = os.path.splitext(item.name)[1]

                # loads only text files
                try:
                    text_content = content.decode("utf-8")
                except UnicodeDecodeError:
                    continue

                metadata = {
                    "file_path": rel_file_path,
                    "file_name": item.name,
                    "file_type": file_type,
                }
                doc = Document(page_content=text_content, metadata=metadata)
                docs.append(doc)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    return docs
   
def main(): 
    repo_path = "out/ohmyzsh-wiki"
    sniff_github(repo_path, clone_url="https://github.com/ohmyzsh/wiki", branch="main")
    
if __name__ == "__main__":
    main()
       