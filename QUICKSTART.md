# Criminal Code Web Application - Quick Start Guide

This guide will help you quickly get started with the Criminal Code web application.

## Quick Start with Docker

The easiest way to run the entire application is using Docker and Docker Compose:

```bash
# Clone the repository
git clone [repository-url]
cd [repository-name]

# Start all services
docker-compose up -d

# Access the API
# The API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

This will start:
- MongoDB for data storage
- Elasticsearch for search functionality
- The Criminal Code API
- A one-time data import service to populate the databases

## Manual Setup

If you prefer to set up the components manually:

1. Set up MongoDB and Elasticsearch (see [SETUP.md](SETUP.md))

2. Create a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Import the data:
```bash
python -m src.scripts.import_data
```

6. Start the API:
```bash
python run_api.py
```

## Testing the API

Once the API is running, you can test it using:

```bash
python -m src.scripts.test_api
```

Or access the interactive API documentation at http://localhost:8000/docs

## Available API Endpoints

- `GET /api/sections` - Get all sections (paginated)
- `GET /api/sections/{section_id}` - Get a specific section by ID
- `GET /api/sections/number/{number}` - Get a section by its number
- `GET /api/search?q={query}` - Search the Criminal Code
- `GET /api/table-of-contents` - Get the table of contents

## Next Steps

Now that you have the backend running, you can:

1. Explore the API using the interactive documentation
2. Set up a frontend to interact with the API
3. Customize the search functionality for specific needs 