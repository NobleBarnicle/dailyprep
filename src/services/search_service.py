from typing import Dict, List, Any, Optional
import os
from elasticsearch import AsyncElasticsearch
from dotenv import load_dotenv

load_dotenv()

# Initialize Elasticsearch client
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "criminal_code")

class SearchService:
    """Service for handling search operations."""
    
    es_client: Optional[AsyncElasticsearch] = None
    
    @classmethod
    async def initialize(cls):
        """Initialize Elasticsearch client."""
        cls.es_client = AsyncElasticsearch([ELASTICSEARCH_URL])
        
    @classmethod
    async def close(cls):
        """Close Elasticsearch client."""
        if cls.es_client:
            await cls.es_client.close()
    
    @classmethod
    async def ensure_index_exists(cls):
        """Ensure the Criminal Code index exists in Elasticsearch."""
        if not cls.es_client:
            await cls.initialize()
            
        exists = await cls.es_client.indices.exists(index=ELASTICSEARCH_INDEX)
        if not exists:
            await cls.create_index()
    
    @classmethod
    async def create_index(cls):
        """Create the Criminal Code index with proper mappings."""
        if not cls.es_client:
            await cls.initialize()
            
        mappings = {
            "mappings": {
                "properties": {
                    "section_id": {"type": "keyword"},
                    "number": {"type": "keyword"},
                    "type": {"type": "keyword"},
                    "text": {
                        "type": "text",
                        "analyzer": "english",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    },
                    "marginal_note": {
                        "type": "text",
                        "analyzer": "english",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    }
                }
            },
            "settings": {
                "analysis": {
                    "analyzer": {
                        "english": {
                            "tokenizer": "standard",
                            "filter": ["lowercase", "english_stop", "english_stemmer"]
                        }
                    },
                    "filter": {
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        },
                        "english_stemmer": {
                            "type": "stemmer",
                            "language": "english"
                        }
                    }
                }
            }
        }
        
        await cls.es_client.indices.create(index=ELASTICSEARCH_INDEX, body=mappings)
    
    @classmethod
    async def index_document(cls, document: Dict[str, Any]):
        """Index a document in Elasticsearch."""
        if not cls.es_client:
            await cls.initialize()
            
        await cls.ensure_index_exists()
        
        await cls.es_client.index(
            index=ELASTICSEARCH_INDEX,
            id=document["section_id"],
            document=document
        )
    
    @classmethod
    async def index_bulk_documents(cls, documents: List[Dict[str, Any]]):
        """Index multiple documents in Elasticsearch."""
        if not cls.es_client:
            await cls.initialize()
            
        await cls.ensure_index_exists()
        
        body = []
        for doc in documents:
            body.append({"index": {"_index": ELASTICSEARCH_INDEX, "_id": doc["section_id"]}})
            body.append(doc)
        
        await cls.es_client.bulk(body=body)
    
    @classmethod
    async def search(cls, query: str, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Search the Criminal Code index."""
        if not cls.es_client:
            await cls.initialize()
            
        from_val = (page - 1) * page_size
        
        search_query = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["text^2", "marginal_note"],
                    "fuzziness": "AUTO"
                }
            },
            "highlight": {
                "fields": {
                    "text": {},
                    "marginal_note": {}
                }
            },
            "from": from_val,
            "size": page_size
        }
        
        response = await cls.es_client.search(
            index=ELASTICSEARCH_INDEX,
            body=search_query
        )
        
        hits = response["hits"]["hits"]
        total = response["hits"]["total"]["value"]
        
        results = []
        for hit in hits:
            source = hit["_source"]
            highlights = []
            
            if "highlight" in hit:
                for field, field_highlights in hit["highlight"].items():
                    highlights.extend(field_highlights)
            
            results.append({
                "section_id": source["section_id"],
                "number": source.get("number", ""),
                "type": source["type"],
                "text": source["text"],
                "score": hit["_score"],
                "highlights": highlights
            })
        
        return {
            "total_results": total,
            "results": results,
            "page": page,
            "page_size": page_size
        } 