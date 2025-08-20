import os
import json
from generate_summary import LLMApi_summary


class DirectoryAnalyzer:
    def __init__(self, verbose=False, gitignore_path=".gitignore", venv_path=".venv_path"):
        self.verbose = verbose
        self.gitignore_path = gitignore_path
        self.venv_path = venv_path

        # Inicializa o gerador de sumários
        self.summary_gen = LLMApi_summary(verbose)
        self.summary_gen.setInitialContext(
            "You are acting as a code review expert. Analyze the following Python code file and provide a clear and concise summary. I want it to be short, very summarized"
        )

    # --- MÉTODOS AUXILIARES ---
    def _is_in_gitignore(self, item):
        if not os.path.exists(self.gitignore_path):
            return False
        with open(self.gitignore_path, "r", encoding="utf-8", errors="ignore") as f:
            ignores = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return item in ignores

    def _is_venv(self, item):
        if not os.path.exists(self.venv_path):
            return False
        with open(self.venv_path, "r", encoding="utf-8", errors="ignore") as f:
            ignores = [line.split("/")[-1].rstrip("\n") for line in f if line.strip()]
        return item in ignores

    def _summarize_file(self, file_path):
        extension = os.path.splitext(file_path)[1]
        if extension not in [".py", ".txt", ".js", ".cpp", ".c"]:
            return "Not readable file"
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                self.summary_gen.generate(f.read())
                return json.loads(self.summary_gen.request())
        except Exception as e:
            return f"file cannot be readable: {e}"

    # --- MÉTODO PRINCIPAL ---
    def get_structure(self, path, root_dir=None, counter=None):
        if root_dir is None:
            root_dir = path
            
        if counter is None:
            total_files = sum(
                len([f for f in files if not f.startswith(".")])
                for _, _, files in os.walk(path)
            )
            counter = {"current": 0, "total": total_files}

        structure = {
            "name": os.path.basename(path) or path,
            "path": os.path.abspath(path),
            "relative_path": os.path.relpath(path, root_dir),
            "type": "directory",
            "children": []
        }

        try:
            for item in os.listdir(path):
                # --- FILTROS ---
                if item.startswith("."):  
                    self.debug_print(f"Ignoring hidden: {item}")
                    continue

                if self._is_in_gitignore(item):
                    self.debug_print(f"Ignoring .gitignore pattern: {item}")
                    continue

                if item in ["__init__.py", "__pycache__", "LICENSE", "README.md", "old"]:
                    self.debug_print(f"Ignoring system/dev file: {item}")
                    continue

                if self._is_venv(item):
                    self.debug_print(f"Ignoring .venv pattern: {item}")
                    continue

                item_path = os.path.join(path, item)

                if os.path.isdir(item_path):
                    structure["children"].append(self.get_structure(item_path, root_dir))

                elif os.path.isfile(item_path):
                    counter["current"] += 1
                    print(f"[{counter['current']}] Processando: {item}")

                    content = self._summarize_file(item_path)
                    structure["children"].append({
                        "name": item,
                        "path": os.path.abspath(item_path),
                        "relative_path": os.path.relpath(item_path, root_dir),
                        "type": "file",
                        "extension": os.path.splitext(item)[1],
                        "content": content
                    })

                else:
                    structure["children"].append({
                        "name": item,
                        "path": os.path.abspath(item_path),
                        "relative_path": os.path.relpath(item_path, root_dir),
                        "type": "unknown"
                    })

        except PermissionError:
            structure["children"].append({
                "name": "(Acesso negado)",
                "path": os.path.abspath(path),
                "relative_path": os.path.relpath(path, root_dir),
                "type": "unreadable"
            })

        return structure

    def save_to_json(self, path):
        data = self.get_structure(path)
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def debug_print(self, msg):
        if self.verbose:
            print(msg)

if __name__ == "__main__":
    analyzer = DirectoryAnalyzer()
    current_dir = os.getcwd()
    json_output = analyzer.save_to_json(current_dir)

    with open("estrutura.json", "w", encoding="utf-8") as f:
        f.write(json_output)
