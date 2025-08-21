# 📖 Project Description

This project, **code_doc**, is a Python tool designed to automatically analyze a code repository's structure and content, and generate a rich and comprehensive `README.md` documentation file. It leverages LLMs (Large Language Models) via API to interpret codebases, summarize relevant elements, and structure them in a professional README documentation format.

---

# ⚙️ System Behavior

The system orchestrates the following workflow:

1. **Directory Analysis**
   - The `DirectoryAnalyzer` scans the repository recursively.
   - Filters off, files using `.gitignore` patterns and `venv` paths.
   - Generates structured metadata and summary for each file via an LLM.

2. **README Generation**
   - The `LLMApi_generate_README` class prepares a structured JSON input based on the directory structure.
   - It communicates with an LLM API, sending a detailed prompt with system instructions and repository data.
   - Finally, the LLM’s output (a detailed Markdown file) is saved as `README.md`.

3. **Summary Generation (Auxiliary)**
   - Optional review summaries of individual files can be generated using `LLMApi_summary`.

---

# 📂 Code Structure

The project is composed of the following Python modules:

```plaintext
├── main.py                # Entry point to generate the README
├── generate_JSON.py       # Directory scanning and metadata generation
├── generate_summary.py    # LLM-based summary generator (auxiliary)
├── requirements.txt       # Python dependencies
```

- All core logic is modularized into classes for scalability and maintainability.
- Configuration and secrets are managed via `.env` file

# 🛠️ Configuration Structure

 Configuration of Sensitive data like API keys are loaded from `.env` files using the `dotenv` library.

### Sample .env Structure:

```env
API_KEY = YOUR_API_KEY
MODEL = YOUR_MODEL_HERE  
BASE_URL = YOUR_BASE_URL
```

---

# 📝 Notes

- Ensure your `.env` file includes the `API_KEY` to enable LLM functionality.
- Place a `.gitignore` and optionally a `.venv_path` in your root directory for correct filtering.
- This system assumes that your target repository's structure is compatible with Python-based recursive scanning.
- Avoid placing extremely large files in your repository, as these may limit performance during summarization.

---

# ❌ Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| API Key not found | `.env` is missing or `OPENAI_API_KEY` not set | Add your OpenAI API key to `.env` |
| Module not found | Missing dependencies | Run `pip install -r requirements.txt` |
| File summarization fails | Unsupported file type or LLM timeout | Add support for the file type or improve prompt |
| YAML Config not loading | Invalid YAML syntax | Validate `config.yaml` syntax or allow auto-generation |

---

# 🔖 Version

- **Version:** v1.0.0 (Initial Release)
---

# 👥 Team

- **Gabriel** – Creator, Software Architect, and Lead Developer

### Contributions

This project is open to contributions. For major changes, please open an issue first to discuss what you'd like to modify.

---

*“Documentation is the love letter you write to your future self.”* – Damian Conway

> Let technology help write that letter for you. ✨