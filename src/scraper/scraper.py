import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://laws-lois.justice.gc.ca/eng/acts/c-46/FullText.html"


def fetch_html(url):
    """Fetch HTML content from a given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text


def parse_html(html):
    """Parse HTML content and return a BeautifulSoup object."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def extract_parts_and_sections(soup):
    """Extract parts and sections from the HTML and return as a structured dictionary."""
    data = []
    
    # Example extraction logic (to be expanded based on actual HTML structure)
    parts = soup.find_all('h2', class_='Part')
    for part in parts:
        part_title = part.get_text(strip=True)
        part_id = part.get('id')
        
        sections = []
        next_sibling = part.find_next_sibling()
        while next_sibling and next_sibling.name != 'h2':
            if next_sibling.name == 'p' and 'Section' in next_sibling.get('class', []):
                section_number = next_sibling.find('a', class_='sectionLabel').get_text(strip=True)
                section_content = next_sibling.get_text(strip=True)
                sections.append({
                    'number': section_number,
                    'content': section_content
                })
            next_sibling = next_sibling.find_next_sibling()
        
        data.append({
            'part_title': part_title,
            'part_id': part_id,
            'sections': sections
        })
    
    return data


def save_to_json(data, filename='criminal_code.json'):
    """Save the extracted data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def save_html(html, filename='criminal_code.html'):
    """Save the HTML content to a file."""
    with open(filename, 'w') as f:
        f.write(html)


def main():
    # Fetch the HTML content
    html_content = fetch_html(BASE_URL)
    
    # Save the HTML content to a file
    save_html(html_content)
    
    # Parse the HTML content
    soup = parse_html(html_content)
    
    # Extract parts and sections
    data = extract_parts_and_sections(soup)
    
    # Save the data to a JSON file
    save_to_json(data)
    
    print("Data extraction complete. HTML saved to criminal_code.html and data saved to criminal_code.json.")


if __name__ == "__main__":
    main() 