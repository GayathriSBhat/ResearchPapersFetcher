# get_papers_list/cli.py

import argparse
from get_papers_list.pubmed_client import search_pubmed, fetch_details
from get_papers_list.filters import extract_non_academic_authors
from get_papers_list.exporter import export_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors")
    parser.add_argument("query", type=str, help="PubMed search query")
    parser.add_argument("-f", "--file", help="Output CSV filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.debug:
        print(f"Searching PubMed for query: {args.query}")

    ids = search_pubmed(args.query)
    papers = fetch_details(ids)
    filtered = []

    for paper in papers:
        non_acad_auths, companies, email = extract_non_academic_authors(paper["Authors"])
        if non_acad_auths:
            paper["NonAcademicAuthors"] = non_acad_auths
            paper["CompanyAffiliations"] = companies
            paper["CorrespondingEmail"] = email
            filtered.append(paper)

    export_to_csv(filtered, args.file)

if __name__ == "__main__":
    main()
