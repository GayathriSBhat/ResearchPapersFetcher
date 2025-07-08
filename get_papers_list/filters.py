from typing import List, Dict, Tuple
import re
from urllib.parse import urlparse

ACADEMIC_KEYWORDS = [
    "university", "université", "universitat", "college", "faculty", "school", 
    "institute", "institutions", "academy", "department", "departments", "center", "centre",
    "hospital", "clinics", "research institute", "medical center", "graduate school", 
    "public health", "labs"
]

ACADEMIC_EMAIL_SUFFIXES = [
    ".edu", ".ac.uk", ".ac.in", ".edu.au", ".ac.jp", ".ac.kr", ".edu.cn",
    ".ac.za", ".edu.sg", ".edu.my", ".ac.ir", ".ac.id", ".edu.br", ".edu.mx"
]

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

def normalize_affiliation(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip(" .;"))

def get_email_domain(email: str) -> str:
    return email.split('@')[-1].lower() if '@' in email else ""

def is_academic_email(email: str) -> bool:
    domain = get_email_domain(email)
    return any(domain.endswith(suffix) for suffix in ACADEMIC_EMAIL_SUFFIXES)

def is_non_academic(affiliation: str, email: str = "") -> bool:
    affil = affiliation.lower()
    has_acad = any(re.search(rf"\b{kw}\b", affil) for kw in ACADEMIC_KEYWORDS)
    
    if email and is_academic_email(email):
        return False  # If email is academic, consider it academic regardless of keywords
    
    return not has_acad

def extract_non_academic_authors(authors: List[Dict]) -> Tuple[List[str], List[str], str]:
    non_acad_authors = []
    companies = set()
    selected_email = ""  # Will store only non-academic email

    for author in authors:
        name = author.get("Name", "")
        raw_affil = author.get("Affiliation", "") or ""

        # Extract email from affiliation
        found_email = re.search(EMAIL_REGEX, raw_affil)
        author_email = found_email.group(0) if found_email else ""

        # clean_affil = normalize_affiliation(
        #     re.sub(r"(Electronic address:)?\s*" + EMAIL_REGEX, "", raw_affil)
        # )

        clean_affil = raw_affil

        if is_non_academic(clean_affil, author_email):
            non_acad_authors.append(name)
            companies.add(clean_affil)
            # Only store email if it's non-academic
            if author_email and not is_academic_email(author_email) and not selected_email:
                selected_email = author_email

    return non_acad_authors, list(companies), selected_email
