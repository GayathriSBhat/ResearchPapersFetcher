# get_papers_list/llm_classifier.py
from typing import List, Tuple, Dict
from llama_cpp import Llama
from tqdm import tqdm

# Configure your model path
model_path = "D:/pharmaPublisher/models/mistral-7b-instruct-v0.2.Q2_K.gguf"

# Load the model
llm = Llama(
    model_path=model_path,
    n_threads=4,     # Adjust per CPU
    n_ctx=512,
    verbose=False    # Disable LLM outputs to stdout
)

print(f"Loaded LLM model from {model_path}")

BATCH_SIZE = 5

def classify_affiliations_with_llm(authors: List[Dict]) -> Tuple[List[str], List[str], str]:
    non_acad_auths = []
    company_names = []
    corresponding_email = ""

    if not authors:
        return non_acad_auths, company_names, corresponding_email

    # Split into batches
    for i in tqdm(range(0, len(authors), BATCH_SIZE), desc="Classifying affiliations (LLM)"):
        batch = authors[i:i + BATCH_SIZE]
        
        # Create prompt with multiple affiliations
        prompt = "Classify the following affiliations as 'academic' or 'non-academic':\n"
        for idx, author in enumerate(batch):
            affil = author.get("Affiliation", "").strip()
            prompt += f"{idx + 1}. {affil}\n"

        prompt += "\nRespond in the format:\n1. academic\n2. non-academic\n..."

        output = llm(prompt, max_tokens=20 + 10 * len(batch), echo=False)
        response = output["choices"][0]["text"].strip().lower()

        # Extract results line-by-line
        lines = response.splitlines()
        for j, line in enumerate(lines):
            if j >= len(batch):
                continue

            if "non-academic" in line:
                name = batch[j].get("Name", "")
                affil = batch[j].get("Affiliation", "")
                email = batch[j].get("Email", "")
                non_acad_auths.append(name)
                company_names.append(affil)
                if not corresponding_email and email:
                    corresponding_email = email

    return non_acad_auths, company_names, corresponding_email
