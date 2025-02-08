# Criminal Code Web Application

A modern, user-friendly web application for accessing and navigating the Criminal Code of Canada.

## Project Overview

This project aims to create a superior alternative to the current government website for accessing the Criminal Code of Canada, with improved navigation, aesthetics, UI/UX, scrolling behavior, and mobile responsiveness.

## Development Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
├── data/                  # Raw data files
├── src/                   # Source code
│   ├── scraper/          # Web scraping modules
│   ├── parser/           # HTML parsing and data extraction
│   └── api/              # API implementation
├── tests/                # Test files
│   ├── scraper/
│   ├── parser/
│   └── api/
└── Notes_to_self/        # Project documentation and notes
```

## Running Tests

```bash
pytest
```

## Code Style

This project uses:
- Black for code formatting
- Flake8 for style guide enforcement
- MyPy for static type checking

## License

[License details to be added] 