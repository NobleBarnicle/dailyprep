from bs4 import BeautifulSoup
import json
import sys
import html

HTML_FILE = 'data/parsing_code.html'  # Default to test file


def load_html(filename):
    """Load HTML content from a file with proper encoding."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def parse_html(html):
    """Parse HTML content and return a BeautifulSoup object."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def extract_data(soup):
    """Extract data from the HTML and return as a structured dictionary."""
    data = []
    
    # Example extraction logic (to be expanded based on actual HTML structure)
    parts = soup.find_all('h2', class_='Part')
    for part in parts:
        part_title = part.get_text(strip=True)
        part_id = part.get('id')
        
        # Capture subheadings
        subheading = None
        next_sibling = part.find_next_sibling()
        if next_sibling and next_sibling.name == 'h3' and 'Subheading' in next_sibling.get('class', []):
            subheading = next_sibling.get_text(strip=True)
            next_sibling = next_sibling.find_next_sibling()
        
        sections = []
        while next_sibling and next_sibling.name != 'h2':
            if next_sibling.name == 'p' and 'Section' in next_sibling.get('class', []):
                section_number = next_sibling.find('a', class_='sectionLabel').get_text(strip=True)
                section_content = next_sibling.get_text(strip=True)
                
                # Capture marginal notes
                marginal_note = None
                previous_sibling = next_sibling.find_previous_sibling()
                if previous_sibling and 'MarginalNote' in previous_sibling.get('class', []):
                    marginal_note = previous_sibling.get_text(strip=True)
                    marginal_note = html.unescape(marginal_note).replace('\u2014', '—')
                
                # Capture historical notes
                historical_note = None
                next_sibling_historical = next_sibling.find_next_sibling()
                if next_sibling_historical and 'HistoricalNote' in next_sibling_historical.get('class', []):
                    historical_note = next_sibling_historical.get_text(strip=True)
                    historical_note = html.unescape(historical_note)
                
                sections.append({
                    'number': section_number,
                    'content': section_content,
                    'marginal_note': marginal_note,
                    'historical_note': historical_note
                })
            next_sibling = next_sibling.find_next_sibling()
        
        data.append({
            'part_title': part_title,
            'part_id': part_id,
            'subheading': subheading,
            'sections': sections
        })
    
    return data


def save_to_json(data, filename='parsed_data.json'):
    """Save the extracted data to a JSON file without escaping non-ASCII characters."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    # Check for command-line argument to switch HTML file
    if len(sys.argv) > 1:
        global HTML_FILE
        HTML_FILE = sys.argv[1]
    
    # Load the HTML content
    html_content = load_html(HTML_FILE)
    
    # Parse the HTML content
    soup = parse_html(html_content)
    
    # Extract data
    data = extract_data(soup)
    
    # Save the data to a JSON file
    save_to_json(data)
    
    print(f"Parsing complete. Data saved to parsed_data.json from {HTML_FILE}.")


if __name__ == "__main__":
    main() 