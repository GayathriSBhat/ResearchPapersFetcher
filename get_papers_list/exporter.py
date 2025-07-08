import csv
import os
from typing import List, Dict

def export_to_csv(papers: List[Dict], filename: str = None) -> None:
    if not papers:
        print("No papers to export.")
        return

    headers = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]

    if filename:
        # Check if file exists to decide whether to write the header
        file_exists = os.path.isfile(filename)
        mode = 'a' if file_exists else 'w'

        with open(filename, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            if not file_exists:
                writer.writeheader()

            for paper in papers:
                writer.writerow({
                    "PubmedID": paper.get("PubmedID", ""),
                    "Title": paper.get("Title", ""),
                    "Publication Date": paper.get("PublicationDate", ""),
                    "Non-academic Author(s)": "; ".join(paper.get("NonAcademicAuthors", [])),
                    "Company Affiliation(s)": "; ".join(paper.get("CompanyAffiliations", [])),
                    "Corresponding Author Email": paper.get("CorrespondingEmail", "")
                })

        print(f"Exported {len(papers)} paper(s) to {filename}")
    else:
        # Print to console if no filename provided
        for paper in papers:
            print(f"{paper['PubmedID']}: {paper['Title']}")
