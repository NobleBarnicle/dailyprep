# Criminal Code Web Application Project Outline

Version: 0.2.0 Last Updated: 2025-03-03

## Vision
The vision for the web-app is a version of the Criminal Code of Canada built for busy criminal lawyers. The current government website has significant limitations in navigation, aesthetics, UI/UX, scrolling behavior, and mobile responsiveness. This project aims to create a superior alternative while serving as a learning experience in modern web development and LLM integration.

Base_URL: https://laws-lois.justice.gc.ca/eng/acts/c-46/FullText.html

## Backend Architecture

### FastAPI Application

- Python 3.11-based RESTful API
- Asynchronous request handling
- Modular router structure
- CORS handling for frontend integration
- Automatic request validation with Pydantic
- Comprehensive error handling and logging
- Dependency injection for services

### Data Processing

- BeautifulSoup4 for HTML parsing
- Automated data extraction pipeline
- Data cleaning and normalization
- JSON-based data structure

### Database Design

- MongoDB for primary storage
- Hierarchical document structure
- Collections:
  - Parts (structural divisions of the code)
  - Sections (individual provisions)
  - Additional metadata

### Search Engine

- Elasticsearch integration (completed)
- Full-text search capabilities
- Custom analyzers for legal terminology
- Highlighting of search results
- Relevance scoring

### API Design  

- RESTful architecture
- Key endpoints:
  - GET /api/sections - List sections with pagination
  - GET /api/sections/{section_id} - Get specific section
  - GET /api/sections/number/{number} - Get section by number
  - GET /api/search - Search with query parameters
  - GET /api/table-of-contents - Get hierarchical structure

## Infrastructure

### Docker Containerization

- Multi-container setup with docker-compose
- Separate containers for:
  - FastAPI application
  - MongoDB database
  - Elasticsearch service
- Development and testing environments

### Caching (Planned)

- In-memory data caching
- Performance optimization

## Security

### API Security

- Input validation with Pydantic
- CORS configuration
- HTTPS implementation (planned for production)

## Frontend Architecture (Planned)

### Framework

- Next.js
- TypeScript for type safety
- React Server Components for optimal performance

### Core Layout Components

- Main Reading Pane
  - Vertical scrolling view
  - Continuous page presentation
  - Infinite scroll with lazy loading

### Top Bar

- Persistent search bar
- Search results overlay
- Additional tools (TBD)

### Left Sidebar    

- Expandable, nested table of contents
- Default view: Parts of Criminal Code
- Floating behavior during scroll
- Critical for navigation and user experience

## User Experience Features (Planned)

### Search Functionality

- Always-visible search bar
- Section/subsection result targeting
- Smooth zoom animation to results
- Visual feedback for scroll direction
- Highlight of found terms

### Visual Design

- Modern, sleek aesthetic
- Light/dark mode toggle
- Sans-serif fonts for readability
- Adjustable font sizing
- Optimized whitespace and line spacing

### Responsive Design

- Mobile-first approach
- Adaptive layouts for all screen sizes
- Collapsible navigation for mobile
- Floating UI elements

## Technical Implementation

### Performance Optimizations

- Asynchronous API with FastAPI
- Efficient database queries
- Optimized search indexing

### Frontend Development (Next Phase)

- Server-side rendering (SSR) for initial load
- Static site generation (SSG) for static content
- Client-side data fetching for dynamic content

### Suggested Libraries

- Next.js App Router
- TanStack Query for data fetching
- Tailwind CSS for styling
- Framer Motion for animations
- Zod for schema validation