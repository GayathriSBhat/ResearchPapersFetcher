# get_papers_list/pubmed_client.py

from typing import List, Dict, Any
import requests
import xml.etree.ElementTree as ET
import re

EMAIL = "youremail@example.com"
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def search_pubmed(query: str, max_results: int = 100) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "email": EMAIL,
    }
    response = requests.get(f"{BASE_URL}/esearch.fcgi", params=params)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

def fetch_details(pubmed_ids: List[str]) -> List[Dict[str, Any]]:
    ids_str = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids_str,
        "retmode": "xml",
        "email": EMAIL,
    }
    response = requests.get(f"{BASE_URL}/efetch.fcgi", params=params)
    response.raise_for_status()

    # Save XML for debugging
    with open("pubmed_response.xml", "w", encoding="utf-8") as f:
        f.write(response.text)

    
    return parse_pubmed_xml(response.text)

def parse_pubmed_xml(xml_data: str) -> List[Dict[str, Any]]:
    root = ET.fromstring(xml_data)
    results = []

    for article in root.findall(".//PubmedArticle"):
        data = {
            "PubmedID": article.findtext(".//PMID"),
            "Title": article.findtext(".//ArticleTitle"),
            "PublicationDate": article.findtext(".//PubDate/Year") or "Unknown",
            "Authors": [],
        }

        if(data["PubmedID"] == "40624691"):
            print("here")

        authors = article.findall(".//Author")
        for author in authors:
            name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()
            affiliation = author.findtext(".//AffiliationInfo/Affiliation", default="")

            email = ""
            if affiliation:
                match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", affiliation)
                if match:
                    email = match.group(0)
                
            data["Authors"].append({
                "Name": name,
                "Affiliation": affiliation,
                "Email": email,
            })
        results.append(data)
    return results
