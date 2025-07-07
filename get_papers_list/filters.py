# get_papers_list/filters.py

from typing import List, Dict
import re

NON_ACADEMIC_KEYWORDS = ["pharma", "biotech", "inc", "ltd", "gmbh", "corp", "laboratories", "therapeutics"]

def is_non_academic(affiliation: str) -> bool:
    affiliation_lower = affiliation.lower()
    return any(keyword in affiliation_lower for keyword in NON_ACADEMIC_KEYWORDS) and \
           not re.search(r"\b(university|college|institute|hospital|school|center|centre)\b", affiliation_lower)

def extract_non_academic_authors(authors: List[Dict]) -> (List[str], List[str], str):
    non_academic_names = []
    company_names = set()
    corresponding_email = ""

    for author in authors:
        affiliation = author["Affiliation"] or ""
        if is_non_academic(affiliation):
            non_academic_names.append(author["Name"])
            company_names.add(affiliation)
            if not corresponding_email and author["Email"]:
                corresponding_email = author["Email"].strip(";.,")
    return non_academic_names, list(company_names), corresponding_email
