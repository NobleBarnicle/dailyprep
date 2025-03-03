# Criminal Code Web Application

A modern, user-friendly web application for accessing and navigating the Criminal Code of Canada.

## Project Overview

This project aims to create a superior alternative to the current government website for accessing the Criminal Code of Canada, with improved navigation, aesthetics, UI/UX, scrolling behavior, and mobile responsiveness.

## Current Progress

- ✅ Web scraper for extracting the Criminal Code content
- ✅ Parser for converting HTML to structured JSON data
- 🔄 Backend API development (in progress)
- 🔜 Frontend development
- 🔜 Search functionality
- 🔜 Deployment

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
│   ├── scraper/           # Web scraping modules
│   ├── parser/            # HTML parsing and data extraction
│   ├── api/               # API implementation
│   ├── database/          # Database models and connection handling
│   └── services/          # Business logic services
├── tests/                 # Test files
│   ├── scraper/
│   ├── parser/
│   ├── api/
│   └── services/
├── frontend/              # Frontend code (to be added)
│   ├── components/        # UI components
│   ├── pages/             # Page layouts
│   ├── styles/            # CSS/styling
│   └── utils/             # Frontend utilities
└── Notes_to_self/         # Project documentation and notes
```

## Backend Architecture

### API Framework
We'll use FastAPI for our backend, which provides:
- Modern, high-performance framework
- Automatic OpenAPI documentation
- Type validation with Pydantic
- Asynchronous request handling
- Easy to test and maintain

### Database
MongoDB will be used for storing the structured Criminal Code data:
- Flexible schema for complex legal document structure
- Native JSON support
- Good performance for read-heavy applications
- Powerful query capabilities

### Search Functionality
Elasticsearch will be integrated for advanced search capabilities:
- Full-text search across the entire Criminal Code
- Faceted search for filtering by sections, parts, etc.
- Relevant ranking of search results
- Support for legal terminology and fuzzy matching

### Authentication (if needed)
- JWT-based authentication for admin functions
- Role-based access control

## API Endpoints (Planned)

- `GET /api/sections` - Get all sections of the Criminal Code
- `GET /api/sections/{section_id}` - Get a specific section by ID
- `GET /api/parts/{part_id}` - Get a specific part by ID
- `GET /api/search` - Search the Criminal Code by keywords
- `GET /api/table-of-contents` - Get the hierarchical structure of the Code

## Development Roadmap

1. **Phase 1: Backend Foundation** (Current)
   - Set up FastAPI project structure
   - Design and implement database models
   - Create basic API endpoints for retrieving sections
   - Develop data import pipeline from parser to database

2. **Phase 2: Search Functionality**
   - Integrate Elasticsearch
   - Implement search endpoints
   - Optimize search relevance for legal text

3. **Phase 3: Frontend Development**
   - Set up frontend framework (React, Vue, etc.)
   - Implement responsive UI components
   - Create navigation and search interfaces
   - Develop section viewer with proper formatting

4. **Phase 4: Advanced Features**
   - Bookmarking and annotations
   - Cross-references within the Code
   - Version tracking of Code amendments
   - Export functionality (PDF, etc.)

5. **Phase 5: Testing and Deployment**
   - Comprehensive testing
   - Performance optimization
   - Deployment to production
   - Monitoring and maintenance

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