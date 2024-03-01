import requests
from urllib.parse import urlparse
from typing import Optional, Dict, Any, List
# from bs4 import BeautifulSoup
# from redux_store import store, set_mapped_results
# from next_navigation import useRouter

class GithubExplorer:
    def __init__(self, repository_url: str) -> None:
        self.repository_url: str = repository_url
        self.files_read: int = 0
        self.folders_read: int = 0
        self.results: List[Dict[str, Any]] = []
        # self.dispatch = useDispatch()
        # self.router = useRouter()
    
    
    def handle_get_owner_and_repo(self, repository_url: str) -> Optional[Dict[str, str]]:
        try:
            parsed_url = urlparse(repository_url)
            path_parts = parsed_url.path.split('/')
            path_parts = [part for part in path_parts if part]  # Filter out empty strings
            owner = path_parts[0]
            repo = path_parts[1]
            return {'owner': owner, 'repo': repo}
        except Exception as e:
            print(f"Error fetching owner and repo details: {e}")
            return None

    def fetch_repository_contents(self, owner: str, repo: str, path: str) -> Any:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        print(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            print(f"Error fetching repository contents: {e}")
            raise

    def fetch_default_branch(self, owner: str, repo: str) -> str:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['default_branch']
        except Exception as e:
            print(f"Error fetching repository information: {e}")
            raise

    def fetch_and_display_file(self, owner: str, repo: str, path: str) -> str:
        try:
            default_branch = self.fetch_default_branch(owner, repo)
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/{path}"
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            print(content)
            return content
        except Exception as e:
            print(f"Error fetching file contents: {e}")
            return ""

    def is_supported_file_type(self, file_name: str) -> bool:
        supported_extensions = [".py"]
        file_extension = file_name[file_name.rfind("."):].lower()
        return file_extension in supported_extensions

    def parse_and_process_contents(self, file_name: str, content: str) -> Dict[str, Any]:
        mapped_results = []
        # change it 
        try:
            parserImp.init()
            parser = parserImp.getParser()
            tree = parser.parse(content)
            root = Lookup(tree.rootNode)
            res = root.traverse({}, "")
            print("Result:", file_name, res)
            lines = len(content.split("\n"))
            filtered_results = {key: value for key, value in res.items() if value.get('grade') is not None}
            mapped_result = {'fileName': file_name, 'lines': lines, 'filteredResults': filtered_results}

            print('mappedResult', mapped_result)
            return mapped_result
        except Exception as e:
            print(f"Error parsing and processing contents: {e}")
            return {}

    def traverse_directory(self, owner: str, repo: str, path: str) -> None:
        contents = self.fetch_repository_contents(owner, repo, path)
        mapped_results = []
        for item in contents:
            if item['type'] == "dir":
                self.folders_read += 1
                self.traverse_directory(owner, repo, item['path'])
            elif item['type'] == "file" and self.is_supported_file_type(item['name']):
                self.files_read += 1
                content = self.fetch_and_display_file(owner, repo, item['path'])
                res = self.parse_and_process_contents(item['name'], content)
                mapped_results.append(res)
        #change it
        # self.dispatch(set_mapped_results(mapped_results))
        # self.router.push("/code/results")
        # print("Store state:", store.getState().results)

    def start_traverse(self) -> None:
        extracted_info = self.handle_get_owner_and_repo(self.repository_url)
        print(extracted_info)
        if extracted_info and extracted_info.get('owner') and extracted_info.get('repo'):
            self.traverse_directory(extracted_info['owner'], extracted_info['repo'],"")
        else:
            print("Missing repository information.")



if __name__ == "__main__":
    github_url = input("Enter the GitHub repository URL: ")
    explorer = GithubExplorer(github_url)
    explorer.start_traverse()
