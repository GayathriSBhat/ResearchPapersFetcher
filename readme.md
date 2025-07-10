## Module : get-papers-list

Fetches research papers from PubMed based on a user query and filters those with authors from biotech or pharmaceutical companies.
Supports both regex-based and LLM-based affiliation classification, optional translation of non-English metadata, and CSV export for downstream analysis.

## Features

- Search via PubMed API
- Filters non-academic authors using affiliation heuristics(regex or LLM as per user requirement)
- Translate foreign-language affiliations with Google Translat
- Outputs CSV with relevant fields
- CLI interface with --file, --debug, --llm and --help options
- Compare regex-based vs LLM-based classification for validation

## Installation

# Clone the repo
git clone https://github.com/GayathriSBhat/get-papers-list
cd get-papers-list

# Install dependencies
poetry install 

## Example Usage
# Basic search and export to CSV
poetry run get-papers-list "cancer therapy" -f results.csv

# Use LLM to classify affiliations
poetry run get-papers-list "synthetic biology" --llm -f llmresults.csv

# Translate non-English affiliations before regex filtering
poetry run get-papers-list "drug delivery" --translate -f results.csv

# Compare regex vs LLM classifications
poetry run get-papers-list "gene editing" --llm --compareTest

## Command-Line Arguments
- query: search term for pubmed query
--max_results : Max no. of articles to fetch (default = 50)
-f, --f : CSV filename to export results
--llm: Enable llm based affiliation classification
--debug: print debug logs and query info
--translate: Translate affiliation metadata to English
--compareTest: compare regex vs LLM author classification

## LLM Integration

The tool supports LLaMA-compatible models via .
To enable it:
1) Download a .gguf model file (e.g., Mistral-7B). 
(link: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/tree/main)
- Look for a file with a name like: 'mistral-7b-instruct-v0.2.Q4_K_M.gguf'
2) Click the Download icon next to the version you want.
3) Save it into your project under:pharmaPublisher/models/

## Comparing LLM vs Regex
The --compareTest option cross-validates outputs from two classification approaches.
It flags mismatches and enforces a strict assertion if differences exceed a set threshold.

## Requirements
- Python 3.9+
- poetry or pip
- requests, tqdm, ftfy, googletrans, llama-cpp-python

## Output
CSV File with following details: 
It shows all Research papers searched; however for author's name, affiliations and their email address it only shows non-academic authors.

Here are the Attributes of the output.csv
-PubMedID : ID of research paper articles available on pubmed database https://pubmed.ncbi.nlm.nih.gov/ 
-Title : Reasearch Paper Title
-Publication Date : Date of Publishing the  Article
-Non-academic authors : Authors working in industries and companies not universities or academic instituions
-Company Affiliations: Industries and names of companies to which the authors are associated
-Corresponding Author email : Emails of non-academic authors



