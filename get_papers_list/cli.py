# get_papers_list/cli.py

import argparse
from get_papers_list.pubmed_client import search_pubmed, fetch_details
from get_papers_list.filters import extract_non_academic_authors
from get_papers_list.exporter import export_to_csv
from get_papers_list.llm_classifier import classify_affiliations_with_llm

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors")
    parser.add_argument("query", type=str, default= "cancer therapy", help="PubMed search query")
    parser.add_argument("-f", "--file", default=None, help="Output CSV filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--llm", action="store_true", help="Use LLM for affiliation classification")


    args = parser.parse_args()

    if args.debug:
        print(f"Searching PubMed for query: {args.query}")

    ids = search_pubmed(args.query)
    papers = fetch_details(ids)
    filtered = []

    for paper in papers:

        if args.llm:
            non_acad_auths, companies, email = classify_affiliations_with_llm(paper["Authors"])
        else:
            non_acad_auths, companies, email = extract_non_academic_authors(paper["Authors"])
        
        paper["NonAcademicAuthors"] = non_acad_auths 
        paper["CompanyAffiliations"] = companies 
        paper["CorrespondingEmail"] = email 
        filtered.append(paper)

    export_to_csv(filtered, args.file)

if __name__ == "__main__":
    main()
