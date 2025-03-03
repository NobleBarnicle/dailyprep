# Criminal Code Web Application: Architecture Overview

This document provides an overview of the backend architecture for the Criminal Code web application.

## Overall Architecture

We've implemented a modern, layered architecture following best practices:

1. **API Layer**: FastAPI endpoints that handle HTTP requests
2. **Service Layer**: Business logic and operations
3. **Repository Layer**: Database interactions
4. **Data Layer**: Models and database connections

This separation of concerns makes the code more maintainable and testable.

## Key Files and Their Purposes

### API Layer

- **`src/api/main.py`**: The entry point for the FastAPI application. It:
  - Sets up the FastAPI app with configuration
  - Adds CORS middleware for frontend communication
  - Registers exception handlers
  - Connects to MongoDB and Elasticsearch on startup
  - Registers all API routers

- **`src/api/routers/section_router.py`**: Handles endpoints for retrieving sections:
  - `GET /api/sections` - List all sections with pagination
  - `GET /api/sections/{section_id}` - Get a specific section by ID
  - `GET /api/sections/number/{number}` - Get a section by its number

- **`src/api/routers/search_router.py`**: Handles search functionality:
  - `GET /api/search` - Search the Criminal Code with query parameters

- **`src/api/routers/toc_router.py`**: Provides the table of contents:
  - `GET /api/table-of-contents` - Get hierarchical structure of the Criminal Code

### Database Layer

- **`src/database/config.py`**: Manages database connections:
  - Establishes connection to MongoDB
  - Provides functions to connect and disconnect
  - Defines collection names and database settings

- **`src/database/models.py`**: Defines Pydantic models for:
  - Data validation and serialization
  - API request/response schemas
  - Document structure for MongoDB and Elasticsearch

- **`src/database/repository.py`**: Contains repository classes:
  - `SectionRepository`: CRUD operations for sections
  - `PartRepository`: CRUD operations for parts of the Criminal Code
  - These abstract away database operations from business logic

### Service Layer

- **`src/services/section_service.py`**: Implements business logic for sections:
  - Retrieving sections and parts
  - Building table of contents
  - Importing data from JSON to database

- **`src/services/search_service.py`**: Handles search functionality:
  - Elasticsearch connection and operations
  - Index creation and management
  - Search queries with highlighting and scoring

### Utility Scripts

- **`src/scripts/import_data.py`**: One-time script to:
  - Import Criminal Code data into MongoDB
  - Index the data in Elasticsearch for searching

- **`src/scripts/test_api.py`**: Test script to:
  - Verify API endpoints are working
  - Test search functionality
  - Check table of contents generation

- **`run_api.py`**: Script to start the FastAPI application:
  - Loads environment variables
  - Configures host and port
  - Starts the uvicorn server

### Deployment Configuration

- **`Dockerfile`**: Defines how to build the application container:
  - Uses Python 3.11 slim image
  - Installs dependencies
  - Copies application code
  - Sets up entry point

- **`docker-compose.yml`**: Orchestrates multiple services:
  - API service (our FastAPI application)
  - MongoDB for data storage
  - Elasticsearch for search functionality
  - Data import service (one-time job)

- **`.env.example`**: Template for environment variables:
  - Database connection settings
  - Elasticsearch configuration
  - API settings

### Documentation

- **`SETUP.md`**: Instructions for setting up the development environment
- **`QUICKSTART.md`**: Quick start guide for running the application
- **`docs/FRONTEND_PLAN.md`**: Plan for frontend development (Phase 3)

## Critical Junctions

The most important connections in the system are:

1. **API to Service Layer**: The routers call service methods to handle business logic
   ```python
   # Example from section_router.py
   section = await SectionService.get_section_by_id(section_id)
   ```

2. **Service to Repository Layer**: Services use repositories for database operations
   ```python
   # Example from section_service.py
   return await SectionRepository.get_section_by_id(section_id)
   ```

3. **Database Connection**: The MongoDB connection is established at application startup
   ```python
   # In main.py
   @app.on_event("startup")
   async def startup_db_client():
       await connect_to_mongodb()
       await SearchService.initialize()
   ```

4. **Data Import Pipeline**: The import script connects the parsed JSON data to the database
   ```python
   # In import_data.py
   import_results = await SectionService.import_data_from_json(data_file)
   ```

5. **Search Integration**: The search service connects to Elasticsearch
   ```python
   # In search_service.py
   cls.es_client = AsyncElasticsearch([ELASTICSEARCH_URL])
   ```

## Data Flow

A typical request flows through the system like this:

1. HTTP request comes to an endpoint (e.g., `/api/sections/123`)
2. The router handles the request and calls the appropriate service
3. The service uses repositories to fetch data from MongoDB
4. The repository returns the data to the service
5. The service processes the data if needed
6. The router returns the response to the client

For search requests, the flow is similar but uses Elasticsearch instead of MongoDB for the actual search operation.

## Development Progress

We've completed:
- Phase 1: Backend Foundation
- Phase 2: Search Functionality

Next is Phase 3: Frontend Development, which will involve building a React application that consumes our API. 