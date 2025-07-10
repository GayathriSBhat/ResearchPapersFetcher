# get_papers_list/pubmed_client.py

from typing import List, Dict, Any
import requests
import xml.etree.ElementTree as ET
import re

# Required for PubMed API usage; NCBI recommends including an email for contact purposes
EMAIL = "youremail@example.com"
# Base URL for NCBI's E-utilities (Entrez API)
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# Performs a search on PubMed for the given query and returns a list of PubMed IDs.
def search_pubmed(query: str, max_results: int = 50) -> List[str]: # max_results is for batch size 
    params = {
        "db": "pubmed", # Search in the PubMed database
        "term": query, # The search term provided by the user
        "retmax": max_results, # Limit on the number of returned IDs
        "retmode": "json",  # Request JSON response
        "email": EMAIL, # Required for NCBI compliance
    }
    response = requests.get(f"{BASE_URL}/esearch.fcgi", params=params)
    response.raise_for_status() # Raise an exception for HTTP errors
    return response.json()["esearchresult"]["idlist"]  # Extract ID list from response

def fetch_details(pubmed_ids: List[str]) -> List[Dict[str, Any]]:
    ids_str = ",".join(pubmed_ids) # Convert list of IDs to comma-separated string
    params = {
        "db": "pubmed", 
        "id": ids_str,
        "retmode": "xml",  # Request XML format for rich metadata
        "email": EMAIL,
    }
    response = requests.get(f"{BASE_URL}/efetch.fcgi", params=params)
    response.raise_for_status()

    # Write the XML response to a file for debugging purposes
    with open("pubmed_response.xml", "w", encoding="utf-8") as f:
        f.write(response.text)

    # Parse the XML and return structured data
    return parse_pubmed_xml(response.text)

def parse_pubmed_xml(xml_data: str) -> List[Dict[str, Any]]:
    # returns the 'root' element of the XML tree.
    root = ET.fromstring(xml_data)
    results = []

    # Loop through each PubMed article in the XML
    for article in root.findall(".//PubmedArticle"):
        data = {
            "PubmedID": article.findtext(".//PMID"), 
            "Title": article.findtext(".//ArticleTitle"), 
            "PublicationDate": article.findtext(".//PubDate/Year") or "Unknown",
            "Authors": [], # Will be filled with parsed author info
        }

        # Loop through all authors in the article
        authors = article.findall(".//Author")
        for author in authors:
            # Get full name (First + Last)
            name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()
            # Get affiliation if available
            affiliation = author.findtext(".//AffiliationInfo/Affiliation", default="")
            # Attempt to extract an email address from the affiliation text
            email = ""
            if affiliation:
                match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", affiliation)
                if match:
                    email = match.group(0)
            # Append structured author info to the list    
            data["Authors"].append({
                "Name": name,
                "Affiliation": affiliation,
                "Email": email,
            })
        results.append(data)
    return results
