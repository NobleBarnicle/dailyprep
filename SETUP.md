# Development Environment Setup

This guide will help you set up the necessary components for the Criminal Code web application.

## Prerequisites

- Python 3.8 or higher
- Docker (for running MongoDB and Elasticsearch)
- Git

## Setting Up the Database and Search Engine

The easiest way to set up MongoDB and Elasticsearch is using Docker:

### MongoDB

```bash
# Run MongoDB container
docker run --name criminal-code-mongo -p 27017:27017 -d mongo:latest
```

### Elasticsearch

```bash
# Run Elasticsearch container
docker run --name criminal-code-elasticsearch -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" -e "xpack.security.enabled=false" \
  -d docker.elastic.co/elasticsearch/elasticsearch:8.11.1
```

## Configuration

1. Create a `.env` file based on the provided `.env.example`:

```bash
cp .env.example .env
```

2. Make sure the MongoDB and Elasticsearch connection settings match your setup.

## Setting Up the Python Environment

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Importing Data

To import the Criminal Code data into MongoDB and Elasticsearch:

```bash
python -m src.scripts.import_data
```

## Running the API

Start the FastAPI application:

```bash
python run_api.py
```

The API should now be accessible at http://localhost:8000, and the interactive API documentation is available at http://localhost:8000/docs.

## Common Issues and Troubleshooting

### MongoDB Connection Issues

- Make sure the MongoDB container is running: `docker ps`
- Check MongoDB logs: `docker logs criminal-code-mongo`
- Verify the connection string in the `.env` file

### Elasticsearch Connection Issues

- Make sure the Elasticsearch container is running: `docker ps`
- Check Elasticsearch logs: `docker logs criminal-code-elasticsearch`
- Verify the connection URL in the `.env` file
- Try accessing Elasticsearch directly: `curl http://localhost:9200`

### API Issues

- Check that the virtual environment is activated
- Verify that all required packages are installed
- Look for error messages in the console output when running the API 