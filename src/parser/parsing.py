from bs4 import BeautifulSoup
import json
import sys
import html
import os
import time

HTML_FILE = 'data/criminal_code.html'  # Updated to include the data directory


def load_html(filename):
    """Load HTML content from a file with proper encoding."""
    # Handle relative paths from the project root
    if not os.path.isabs(filename):
        filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), filename)
    
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def parse_html(html):
    """Parse HTML content and return a BeautifulSoup object."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def load_schema(filename='data/schema.json'):
    """Load the schema from a JSON file."""
    # Handle relative paths from the project root
    if not os.path.isabs(filename):
        filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), filename)
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_historical_notes(element):
    """Extract all historical notes following an element."""
    historical_notes = []
    
    # Find the next sibling that is a div with class HistoricalNote
    current = element
    while current:
        current = current.find_next_sibling()
        if not current:
            break
            
        # If we encounter another section or a marginal note before finding a historical note,
        # then the historical note doesn't belong to this section
        if (current.name == 'p' and ('Section' in current.get('class', []) or 'MarginalNote' in current.get('class', []))) or \
           (current.name == 'h2' and 'Part' in current.get('class', [])):
            break
            
        # Only process HistoricalNote divs
        if current.name == 'div' and 'HistoricalNote' in current.get('class', []):
            # Find all HistoricalNoteSubItem elements, even if they're nested
            for note in current.select('li.HistoricalNoteSubItem'):
                # Check if the note has a link (which might contain amendment details)
                link = note.find('a')
                if link:
                    # If it has a link, just get the text of the link
                    note_text = link.get_text(strip=True)
                else:
                    # Otherwise, get the full text of the note
                    note_text = note.get_text(strip=True)
                    
                # Include all historical notes
                historical_notes.append(note_text)
            
            # Continue looking for more historical notes instead of breaking
            # This allows us to capture multiple HistoricalNote divs if they exist
    
    # Debug output for historical notes
    if historical_notes:
        section_id = element.get('id', 'unknown')
        print(f"  Found historical notes for element {section_id}: {len(historical_notes)} notes")
        
    return ' '.join(historical_notes) if historical_notes else None


def extract_list_items(ul_element):
    """Extract list items and their nested structure."""
    items = []
    if not ul_element:
        return items
        
    for li in ul_element.find_all('li', recursive=False):
        item = {}
        # Get the paragraph text within the list item
        p_element = li.find('p', recursive=False)
        if p_element:
            # Extract the label (e.g., (a), (b), etc.)
            law_label = p_element.find('span', class_='lawlabel')
            label = law_label.get_text().strip() if law_label else None
            
            # Remove the label from the text if it exists
            if law_label:
                law_label.decompose()
            
            item['text'] = p_element.get_text().strip()
            if label:
                item['label'] = label

        # Check for nested lists
        nested_ul = li.find('ul', class_='ProvisionList', recursive=False)
        if nested_ul:
            item['sub_items'] = extract_list_items(nested_ul)
            
        # Check for continued text after nested lists
        continued_p = li.find('p', class_='ContinuedParagraph', recursive=False)
        if continued_p:
            item['continued_text'] = continued_p.get_text().strip()
            
        items.append(item)
    return items


def extract_external_references(element):
    """Extract external cross-references from an element."""
    references = []
    
    # Find all cite elements with class XRefExternalAct
    cite_elements = element.find_all('cite', class_='XRefExternalAct')
    
    for cite in cite_elements:
        # Extract the reference text and link if available
        reference = {
            'text': cite.get_text().strip()
        }
        
        # Check if there's a link inside the cite element
        link = cite.find('a')
        if link and 'href' in link.attrs:
            reference['href'] = link['href']
            
        references.append(reference)
        
    return references if references else None


def extract_element_content(element):
    """Extract content from a section element."""
    content = {}
    
    # Extract section number if present
    section_label = element.find('a', class_='sectionLabel')
    if section_label:
        content['number'] = section_label.get_text().strip()
        
    # Extract marginal note
    marginal_note = element.find_previous_sibling('p', class_='MarginalNote')
    if marginal_note:
        content['marginal_note'] = marginal_note.get_text().replace('Marginal note:', '').strip()
        
    # Extract section ID
    if 'id' in element.attrs:
        content['section_id'] = element.get('id')
        
    # Debug output
    section_num = content.get('number', 'unknown')
    print(f"Processing section {section_num}")
    
    # Check if this is a section with inline definitions
    defined_terms = element.find_all('span', class_='DefinedTerm')
    
    # Check if this is a section with indented definitions
    # Make sure we're only getting the immediate next sibling that's a definition list
    next_sibling = element.find_next_sibling()
    definition_list = next_sibling if next_sibling and next_sibling.name == 'dl' and 'Definition' in next_sibling.get('class', []) else None
    
    # Check if this is a section with a list
    # We need to be careful to only associate a list with a section if it's directly following the section
    # and not separated by a HistoricalNote or other elements
    next_sibling = element.find_next_sibling()
    
    # Check for external references in the section
    external_references = extract_external_references(element)
    
    # Check if this is a section with subsections
    # This is identified by a ul with class="Section ProvisionList"
    if element.name == 'ul' and 'Section' in element.get('class', []) and 'ProvisionList' in element.get('class', []):
        # Extract subsections first to check if any have inline definitions or indented definitions
        subsections = extract_subsections(element)
        
        # Check if any subsection has a definition marginal note, defined terms, or indented definitions
        has_inline_definitions = False
        has_indented_definitions = False
        has_external_references = False
        
        # If any subsection has external references, collect them at the section level too
        all_external_references = []
        
        for subsection in subsections:
            if subsection.get('has_definition_marginal_note') or subsection.get('defined_terms'):
                has_inline_definitions = True
                # Remove the temporary flag
                if 'has_definition_marginal_note' in subsection:
                    del subsection['has_definition_marginal_note']
            
            # Check if any subsection has an indented definition
            if subsection.get('definitions'):
                has_indented_definitions = True
                print(f"  Section {section_num} has subsection with indented definitions")
                
            # Check if any subsection has external references
            if subsection.get('external_references'):
                has_external_references = True
                print(f"  Section {section_num} has subsection with external references")
                # Add these references to the section-level collection
                all_external_references.extend(subsection.get('external_references', []))
        
        # Determine the section type based on which type of definitions it has
        if has_external_references:
            content['type'] = 'SectionWithExternalReference'
            # Store the external references at the section level too
            if all_external_references:
                content['external_references'] = all_external_references
            print(f"  Section {section_num} classified as SectionWithExternalReference")
        elif has_indented_definitions:
            content['type'] = 'SectionWithSubsectionsWithIndentedDefinitions'
            print(f"  Section {section_num} classified as SectionWithSubsectionsWithIndentedDefinitions")
        elif has_inline_definitions:
            content['type'] = 'SectionWithSubsectionsWithInlineDefinitions'
            print(f"  Section {section_num} classified as SectionWithSubsectionsWithInlineDefinitions")
        else:
            content['type'] = 'SectionWithSubsections'
            print(f"  Section {section_num} classified as SectionWithSubsections")
        
        # Add the subsections to the content
        content['subsections'] = subsections
        
        # Look for historical notes after the section
        historical_note = extract_historical_notes(element)
        if historical_note:
            content['historical_note'] = historical_note
    # Only classify as SectionWithList if the next sibling is directly a ProvisionList
    elif next_sibling and next_sibling.name == 'ul' and 'ProvisionList' in next_sibling.get('class', []):
        # Check if there's a continued text paragraph after the list
        list_element = next_sibling
        continued_text = list_element.find_next_sibling()
        
        if continued_text and continued_text.name == 'p' and 'ContinuedSectionSubsection' in continued_text.get('class', []):
            # This is a section with continued text
            content['type'] = 'SectionWithContinuedText'
            content['lead_in'] = element.get_text().strip()
            content['items'] = extract_list_items(list_element)
            content['continued_text'] = continued_text.get_text().strip()
            print(f"  Section {section_num} has continued text: {continued_text.get_text().strip()[:30]}...")
            print(f"  Section {section_num} classified as SectionWithContinuedText")
            
            # Look for historical notes after the continued text
            historical_note = extract_historical_notes(continued_text)
            if historical_note:
                content['historical_note'] = historical_note
        else:
            # This is a regular section with a list
            content['type'] = 'SectionWithList'
            content['lead_in'] = element.get_text().strip()
            content['items'] = extract_list_items(list_element)
            print(f"  Section {section_num} classified as SectionWithList")
            
            # If no continued text, look for historical notes directly after the list
            historical_note = extract_historical_notes(list_element)
            if historical_note:
                content['historical_note'] = historical_note
    elif definition_list:
        # Check if this also has inline definitions (combined case)
        if defined_terms:
            content['type'] = 'SectionWithCombinedDefinitions'
            print(f"  Section {section_num} has both indented and inline definitions")
            print(f"  Section {section_num} classified as SectionWithCombinedDefinitions")
            
            # Extract the inline defined terms
            terms = []
            for term in defined_terms:
                dfn = term.find('dfn')
                if dfn:
                    terms.append(dfn.get_text().strip())
            
            if terms:
                content['defined_terms'] = terms
        else:
            # This is a section with indented definitions only
            content['type'] = 'SectionWithIndentedDefinitions'
            print(f"  Section {section_num} classified as SectionWithIndentedDefinitions")
            
        content['text'] = element.get_text().strip()
        
        # Extract the defined terms and their definitions
        definitions = []
        for dt in definition_list.find_all('dt'):
            term_element = dt.find('span', class_='DefinedTerm')
            if term_element:
                term = term_element.find('dfn').get_text().strip() if term_element.find('dfn') else term_element.get_text().strip()
                
                # Find the corresponding dd element
                dd = dt.find_next_sibling('dd')
                if dd:
                    definition = {
                        'term': term,
                        'text': dd.get_text().strip()
                    }
                    
                    # Check if the definition has a list
                    list_element = dd.find('ul', class_='ProvisionList')
                    if list_element:
                        definition['items'] = extract_list_items(list_element)
                    
                    definitions.append(definition)
        
        if definitions:
            content['definitions'] = definitions
            
        # Look for historical notes after the definition list
        historical_note = extract_historical_notes(definition_list)
        if historical_note:
            content['historical_note'] = historical_note
    elif defined_terms:
        # This is a section with inline definitions
        content['type'] = 'SectionWithInlineDefinitions'
        content['text'] = element.get_text().strip()
        print(f"  Section {section_num} classified as SectionWithInlineDefinitions")
        
        # Extract the defined terms
        terms = []
        for term in defined_terms:
            dfn = term.find('dfn')
            if dfn:
                terms.append(dfn.get_text().strip())
        
        if terms:
            content['defined_terms'] = terms
            
        # For sections with inline definitions, look for historical notes directly after the section
        historical_note = extract_historical_notes(element)
        if historical_note:
            content['historical_note'] = historical_note
    else:
        # Check for external references in the section text
        if external_references:
            content['type'] = 'SectionWithExternalReference'
            content['text'] = element.get_text().strip()
            content['external_references'] = external_references
            print(f"  Section {section_num} has external references")
            print(f"  Section {section_num} classified as SectionWithExternalReference")
        else:
            content['type'] = 'Section'
            content['text'] = element.get_text().strip()
            print(f"  Section {section_num} classified as regular Section")
        
        # For regular sections, look for historical notes directly after the section
        historical_note = extract_historical_notes(element)
        if historical_note:
            content['historical_note'] = historical_note
        
    return content


def extract_subsections(ul_element):
    """Extract subsections from a section with subsections."""
    subsections = []
    
    # Process each li element (subsection)
    for li in ul_element.find_all('li', recursive=False):
        subsection = {}
        
        # Check if this subsection has its own marginal note
        marginal_note = li.find('p', class_='MarginalNote')
        if marginal_note:
            subsection['marginal_note'] = marginal_note.get_text().replace('Marginal note:', '').strip()
        
        # Check if this subsection has a definition marginal note
        definition_marginal_note = li.find('p', class_='MarginalNoteDefinedTerm')
        if definition_marginal_note:
            subsection['marginal_note'] = definition_marginal_note.get_text().strip()
            # Mark this subsection as having a definition
            subsection['has_definition_marginal_note'] = True
            
        # Get the subsection paragraph
        subsection_p = li.find('p', class_='Subsection')
        if not subsection_p:
            print(f"  Warning: Found a subsection without a paragraph element")
            continue
            
        # Extract subsection number
        law_label = subsection_p.find('span', class_='lawlabel')
        if law_label:
            subsection['number'] = law_label.get_text().strip()
        else:
            print(f"  Warning: Subsection does not have a law label")
            
        # Extract subsection text
        # First, check if this is the first subsection which contains the section number
        section_label = subsection_p.find('a', class_='sectionLabel')
        if section_label:
            # Remove the section label from the text
            section_label_parent = section_label.parent
            if section_label_parent:
                section_label_parent.decompose()
                
        # Remove the law label from the text
        if law_label:
            law_label.decompose()
            
        subsection['text'] = subsection_p.get_text().strip()
        
        # Check for external references in the subsection
        external_references = extract_external_references(subsection_p)
        if external_references:
            subsection['external_references'] = external_references
            print(f"  Subsection {subsection.get('number', 'unknown')} has external references: {external_references}")
        
        # Check for lists within the subsection
        provision_list = li.find('ul', class_='ProvisionList', recursive=False)
        if provision_list:
            items = extract_list_items(provision_list)
            subsection['items'] = items
            print(f"  Subsection {subsection.get('number', 'unknown')} has {len(items)} list items")
            
        # Check for continued text after the list
        continued_text = li.find('p', class_='ContinuedSectionSubsection', recursive=False)
        if continued_text:
            subsection['continued_text'] = continued_text.get_text().strip()
            print(f"  Subsection {subsection.get('number', 'unknown')} has continued text")
            
        # Check for definitions within the subsection
        definition_list = li.find('dl', class_='Definition', recursive=False)
        if definition_list:
            # Extract the defined terms and their definitions
            definitions = []
            for dt in definition_list.find_all('dt'):
                term_element = dt.find('span', class_='DefinedTerm')
                if term_element:
                    term = term_element.find('dfn').get_text().strip() if term_element.find('dfn') else term_element.get_text().strip()
                    
                    # Find the corresponding dd element
                    dd = dt.find_next_sibling('dd')
                    if dd:
                        definition = {
                            'term': term,
                            'text': dd.get_text().strip()
                        }
                        
                        # Check if the definition has a list
                        list_element = dd.find('ul', class_='ProvisionList')
                        if list_element:
                            definition['items'] = extract_list_items(list_element)
                        
                        definitions.append(definition)
            
            if definitions:
                subsection['definitions'] = definitions
                print(f"  Subsection {subsection.get('number', 'unknown')} has {len(definitions)} definitions")
                
        # Check for defined terms within the subsection
        defined_terms = subsection_p.find_all('span', class_='DefinedTerm')
        if defined_terms:
            terms = []
            for term in defined_terms:
                dfn = term.find('dfn')
                if dfn:
                    terms.append(dfn.get_text().strip())
            
            if terms:
                subsection['defined_terms'] = terms
                print(f"  Subsection {subsection.get('number', 'unknown')} has {len(terms)} inline defined terms")
                
        subsections.append(subsection)
        
    print(f"  Extracted {len(subsections)} subsections total")
    return subsections


def extract_data(soup):
    """Extract structured data from the HTML soup."""
    data = []
    seen_sections = set()  # Track sections we've already processed
    seen_section_ids = set()  # Track section IDs we've already processed
    
    # Process each section in order
    for element in soup.find_all(['h2', 'p', 'ul']):
        # Skip elements inside historical notes, amendments, or popups
        if element.find_parent('div', class_='HistoricalNote') or element.find_parent('div', class_='AmendedText') or element.find_parent('section', class_='mfp-hide'):
            continue
            
        if element.name == 'h2' and 'Part' in element.get('class', []):
            # Extract Part information
            part_data = {
                'type': 'Part',
                'part_id': element.get('id'),
                'text': element.get_text().strip()
            }
            data.append(part_data)
        elif element.name == 'ul' and 'Section' in element.get('class', []) and 'ProvisionList' in element.get('class', []):
            # This is a section with subsections
            # Check if we've already processed this section ID
            section_id = element.get('id')
            if section_id and section_id in seen_section_ids:
                continue
                
            # Add the section ID to the set of processed IDs
            if section_id:
                seen_section_ids.add(section_id)
                
            # Extract section content
            section_data = extract_element_content(element)
            data.append(section_data)
        elif element.name == 'p' and 'Section' in element.get('class', []):
            # This is a regular section or a section with a list
            # Check if we've already processed this section
            section_label = element.find('a', class_='sectionLabel')
            if section_label:
                section_number = section_label.get_text().strip()
                if section_number in seen_sections:
                    continue
                    
                # Add the section number to the set of processed sections
                seen_sections.add(section_number)
                
            # Extract section content
            section_data = extract_element_content(element)
            data.append(section_data)
            
    return data


def extract_metadata(soup):
    """Extract metadata from the HTML document."""
    metadata = {}
    
    # Find all meta tags with Dublin Core terms
    meta_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('dcterms.')})
    
    for tag in meta_tags:
        # Extract the property name (remove the 'dcterms.' prefix)
        property_name = tag.get('name').replace('dcterms.', '')
        
        # Extract the content
        content = tag.get('content')
        
        # Add to metadata dictionary
        metadata[property_name] = content
        
    return metadata


def save_to_json(data, filename='parsed_data.json'):
    """
    Save the data to a JSON file.
    
    Args:
        data (dict): The data to save.
        filename (str): The name of the file to save the data to.
    """
    # Use absolute path for the output file
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return output_path


def validate_parsed_data(data):
    """Validate the parsed data for completeness and quality."""
    print("\nValidating parsed data...")
    
    # Statistics
    section_types = {}
    has_historical_note = 0
    has_external_references = 0
    has_defined_terms = 0
    
    # Check each section
    for section in data['sections']:
        # Count section types
        section_type = section.get('type', 'Unknown')
        section_types[section_type] = section_types.get(section_type, 0) + 1
        
        # Check for historical notes
        if 'historical_note' in section:
            has_historical_note += 1
            
        # Check for external references
        if 'external_references' in section:
            has_external_references += 1
            
        # Check for defined terms
        if 'defined_terms' in section:
            has_defined_terms += 1
            
        # Specific checks for different section types
        if section_type == 'SectionWithSubsections':
            if 'subsections' not in section:
                print(f"Warning: Section {section.get('number', 'unknown')} is marked as SectionWithSubsections but has no subsections")
        
        if section_type == 'SectionWithList':
            if 'items' not in section:
                print(f"Warning: Section {section.get('number', 'unknown')} is marked as SectionWithList but has no items")
        
        if section_type == 'SectionWithContinuedText':
            if 'continued_text' not in section:
                print(f"Warning: Section {section.get('number', 'unknown')} is marked as SectionWithContinuedText but has no continued_text")
        
        if section_type == 'SectionWithInlineDefinitions':
            if 'defined_terms' not in section:
                print(f"Warning: Section {section.get('number', 'unknown')} is marked as SectionWithInlineDefinitions but has no defined_terms")
        
        if section_type == 'SectionWithIndentedDefinitions':
            if 'definitions' not in section:
                print(f"Warning: Section {section.get('number', 'unknown')} is marked as SectionWithIndentedDefinitions but has no definitions")
        
        if section_type == 'SectionWithExternalReference':
            if 'external_references' not in section:
                print(f"Warning: Section {section.get('number', 'unknown')} is marked as SectionWithExternalReference but has no external_references")
    
    # Print statistics
    print("\nParsing Statistics:")
    print(f"Total sections: {len(data['sections'])}")
    print(f"Sections with historical notes: {has_historical_note}")
    print(f"Sections with external references: {has_external_references}")
    print(f"Sections with defined terms: {has_defined_terms}")
    print("\nSection Types:")
    for section_type, count in section_types.items():
        print(f"  {section_type}: {count}")
    
    print("\nMetadata:")
    for key, value in data['metadata'].items():
        print(f"  {key}: {value}")
    
    print("\nValidation complete.")
    

def main():
    # Check for command-line argument to switch HTML file
    if len(sys.argv) > 1:
        global HTML_FILE
        HTML_FILE = sys.argv[1]
    
    # Start timing
    start_time = time.time()
    
    print(f"Starting parsing of {HTML_FILE}...")
    
    # Load the schema
    schema = load_schema()
    
    # Load the HTML content
    html_content = load_html(HTML_FILE)
    print(f"HTML loaded in {time.time() - start_time:.2f} seconds")
    
    # Parse the HTML content
    soup = parse_html(html_content)
    print(f"HTML parsed in {time.time() - start_time:.2f} seconds")
    
    # Extract metadata
    metadata = extract_metadata(soup)
    
    # Extract data using the schema
    sections_data = extract_data(soup)
    print(f"Data extraction completed in {time.time() - start_time:.2f} seconds")
    
    # Combine metadata and sections data
    data = {
        "metadata": metadata,
        "sections": sections_data
    }
    
    # Validate the parsed data
    validate_parsed_data(data)
    
    # Use a different output filename for the full code
    output_filename = 'full_criminal_code.json' if 'criminal_code.html' in HTML_FILE else 'parsed_data.json'
    
    # Save the data to a JSON file
    output_path = save_to_json(data, output_filename)
    
    # Calculate total time
    total_time = time.time() - start_time
    print(f"Parsing complete in {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    print(f"Data saved to {output_path} from {HTML_FILE}")
    
    return data


if __name__ == "__main__":
    main() 