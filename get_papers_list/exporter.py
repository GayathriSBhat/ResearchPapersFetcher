# get_papers_list/exporter.py

import csv
from typing import List, Dict
import sys

def export_to_csv(papers: List[Dict], file: str = None) -> None:
    fieldnames = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
    output = open(file, mode="w", newline="", encoding="utf-8") if file else sys.stdout
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for paper in papers:
        writer.writerow({
            "PubmedID": paper["PubmedID"],
            "Title": paper["Title"],
            "Publication Date": paper["PublicationDate"],
            "Non-academic Author(s)": "; ".join(paper["NonAcademicAuthors"]),
            "Company Affiliation(s)": "; ".join(paper["CompanyAffiliations"]),
            "Corresponding Author Email": paper["CorrespondingEmail"],
        })
    if file:
        output.close()
