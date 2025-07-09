# Compares results of regex based and llm based extraction 
import csv

REGEX_FILE = "results.csv"
LLM_FILE = "llmresults.csv"

def load_csv_by_pubmed_id(file_path: str) -> dict:
    """Load CSV and return a dict keyed by PubmedID."""
    data = {}
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pubmed_id = row["PubmedID"]
            data[pubmed_id] = row
    return data

def test_llm_and_regex_results_agree():
    regex_data = load_csv_by_pubmed_id(REGEX_FILE)
    llm_data = load_csv_by_pubmed_id(LLM_FILE)

    mismatches = []

    for pubmed_id in regex_data:
        if pubmed_id not in llm_data:
            continue

        r = regex_data[pubmed_id]
        l = llm_data[pubmed_id]

        # Compare non-academic authors
        r_authors = set(r["Non-academic Author(s)"].split("; "))
        l_authors = set(l["Non-academic Author(s)"].split("; "))

        if r_authors != l_authors:
            mismatches.append({
                "PubmedID": pubmed_id,
                "Regex Authors": r_authors,
                "LLM Authors": l_authors
            })

    assert len(mismatches) <= 5, f"Too many mismatches:\n{mismatches[:5]}"
