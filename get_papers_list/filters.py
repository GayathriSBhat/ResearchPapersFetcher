# Used for classification as academic or Non-Academic
from typing import List, Dict, Tuple
import re
from urllib.parse import urlparse
from ftfy import fix_text
from googletrans import Translator
from tqdm import tqdm

ACADEMIC_KEYWORDS = [
    "university", "université", "universitat", "college", "faculty", "school", 
    "institute", "institutions", "academy", "department", "departments",
    "research institute", "medical center", "graduate school", "labs"
] ## add more as per requirements

ACADEMIC_EMAIL_SUFFIXES = [
    ".edu", ".ac.uk", ".ac.in", ".edu.au", ".ac.jp", ".ac.kr", ".edu.cn",
    ".ac.za", ".edu.sg", ".edu.my", ".ac.ir", ".ac.id", ".edu.br", ".edu.mx"
]

# Regex pattern to extract email addresses
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# Initialize the Google Translate client
translator = Translator()

# Normalize whitespace and strip unwanted trailing characters in affiliations.
def normalize_affiliation(text: str, debug: bool = False) -> str:
    return re.sub(r"\s+", " ", text.strip(" .;"))

# Translate other languages detected to English   
def translate_affiliation(text: str, debug: bool = False)-> str:
    # Remove characters not part of QUERTY 
    fixed = fix_text(text)
    # Translate if not English
    try:
        detected = translator.detect(fixed)
        if detected.lang != "en":
            translated = translator.translate(fixed, src=detected.lang, dest="en")
            
            if debug:
                print(f"\n[DEBUG] Affiliation Translation:")
                print(f"  Original: {text}")
                print(f"  Fixed:    {fixed}")
                print(f"  Detected: {detected.lang}")
                print(f"  English:  {translated.text}")

            fixed = translated.text
        elif debug:
            print(f"\n[DEBUG] Affiliation (No Translation Needed):")
            print(f"  Original: {text}")
            print(f"  Fixed:    {fixed}")
    except Exception as e:
        if debug:
            print(f"[WARN] Translation failed: {e}")
    return re.sub(r"\s+", " ", fixed.strip(" .;"))

# Extract email domain    
def get_email_domain(email: str) -> str:
    return email.split('@')[-1].lower() if '@' in email else ""

# Check if the email belongs to an academic domain.
def is_academic_email(email: str) -> bool:
    domain = get_email_domain(email)
    return any(domain.endswith(suffix) for suffix in ACADEMIC_EMAIL_SUFFIXES)

# Check if the email belongs to an academic domain
def is_non_academic(affiliation: str, email: str = "") -> bool:
    affil = affiliation.lower()
    # Check for academic keywords in the affiliation text
    has_acad = any(re.search(rf"\b{kw}\b", affil) for kw in ACADEMIC_KEYWORDS)
    
    if email and is_academic_email(email):
        return False  # If email is academic, consider it academic regardless of keywords
    
    return not has_acad

# Extract non-academic authors from a list of author dictionaries.
def extract_non_academic_authors(authors: List[Dict], debug: bool = False, use_translation: bool = False) -> Tuple[List[str], List[str], str]:
    non_acad_authors = []
    companies = set()
    selected_email = ""

    # Iterate over authors with progress bar (tqdsm - progress bar)
    for author in tqdm(authors, desc="Processing authors"):
        name = author.get("Name", "")
        raw_affil = author.get("Affiliation", "") or ""

        # Iterate over authors with progress bar
        found_email = re.search(EMAIL_REGEX, raw_affil)
        author_email = found_email.group(0) if found_email else ""

        # Remove the email from the affiliation string and normalize it
        clean_affil = normalize_affiliation(
            re.sub(r"(Electronic address:)?\s*" + EMAIL_REGEX, "", raw_affil)
        )

        # Translate if requested
        if use_translation:
            processed_affil = translate_affiliation(clean_affil, debug=debug)
        else:
            processed_affil = clean_affil

        # Determine if this is a non-academic affiliation
        if is_non_academic(processed_affil, author_email):
            non_acad_authors.append(name)
            companies.add(clean_affil)

            # Save the first non-academic email if not already selected
            if author_email and not is_academic_email(author_email) and not selected_email:
                selected_email = author_email

    return non_acad_authors, list(companies), selected_email

