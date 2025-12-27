from google import genai
from gitingest import ingest
import dotenv
import os

dotenv.load_dotenv(".env")
repo_url = os.getenv("repo_url")
api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
# 1. Setup Gemini
#genai.configure(api_key=api_key)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
#for model in client.models.list():
#    print(model.name)

#model = genai.GenerativeModel(model)


# 2. Ingest Repo
summary, tree, content = ingest(repo_url, token=os.getenv("ACCESS_TOKEN"))
name = repo_url.split("/")[-1]
repo_context = f"File Tree:\n{tree}\n\nCode Content:\n{content}"

with open(f"Documentation/{name}.txt", "w", encoding="utf-8") as f:
    f.write(repo_context)
# 3. Define the Documentation Prompt
doc_prompt = f"""
You are an expert technical writer. Based on the following codebase context, 
please generate a comprehensive 'Project-Overview.md' file. 
Include:
1. System Architecture
2. Key Modules & their responsibilities
3. Setup & Installation
4. API Endpoints (if applicable)

Context:
{repo_context}
"""

# 4. Generate & Save
response = client.models.generate_content(model=os.getenv("model"), contents=doc_prompt)
with open(f"Documentation/Project-Overview-{name}.md", "w") as f:
    f.write(response.text)