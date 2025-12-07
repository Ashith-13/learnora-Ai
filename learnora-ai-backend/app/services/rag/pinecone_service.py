from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class PineconeService:
    """Service for managing Pinecone vector database operations"""
    
    def __init__(self):
        """Initialize Pinecone client"""
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.dimension = 1536  # OpenAI text-embedding-3-small dimension
        self.metric = "cosine"
        self.index = None
        
    async def initialize(self):
        """Initialize or connect to Pinecone index"""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes().names()
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric=self.metric,
                    spec=ServerlessSpec(
                        cloud='aws',
                        region=settings.PINECONE_ENVIRONMENT
                    )
                )
                logger.info(f"Index {self.index_name} created successfully")
            else:
                logger.info(f"Connecting to existing index: {self.index_name}")
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            return True
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {str(e)}")
            raise
    
    async def upsert_vectors(
        self,
        vectors: List[tuple],
        namespace: str = ""
    ) -> Dict[str, Any]:
        """
        Upsert vectors to Pinecone index
        
        Args:
            vectors: List of tuples (id, vector, metadata)
            namespace: Namespace for organizing vectors
            
        Returns:
            Upsert response
        """
        try:
            if not self.index:
                await self.initialize()
            
            response = self.index.upsert(
                vectors=vectors,
                namespace=namespace
            )
            
            logger.info(f"Upserted {len(vectors)} vectors to namespace '{namespace}'")
            return response
            
        except Exception as e:
            logger.error(f"Error upserting vectors: {str(e)}")
            raise
    
    async def query(
        self,
        vector: List[float],
        top_k: int = 5,
        namespace: str = "",
        filter: Optional[Dict] = None,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Query similar vectors from Pinecone
        
        Args:
            vector: Query vector
            top_k: Number of results to return
            namespace: Namespace to query
            filter: Metadata filter
            include_metadata: Whether to include metadata in response
            
        Returns:
            Query results with matches
        """
        try:
            if not self.index:
                await self.initialize()
            
            results = self.index.query(
                vector=vector,
                top_k=top_k,
                namespace=namespace,
                filter=filter,
                include_metadata=include_metadata
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error querying vectors: {str(e)}")
            raise
    
    async def delete(
        self,
        ids: Optional[List[str]] = None,
        delete_all: bool = False,
        namespace: str = ""
    ) -> Dict[str, Any]:
        """
        Delete vectors from index
        
        Args:
            ids: List of vector IDs to delete
            delete_all: Delete all vectors in namespace
            namespace: Namespace to delete from
            
        Returns:
            Delete response
        """
        try:
            if not self.index:
                await self.initialize()
            
            if delete_all:
                response = self.index.delete(delete_all=True, namespace=namespace)
                logger.info(f"Deleted all vectors from namespace '{namespace}'")
            elif ids:
                response = self.index.delete(ids=ids, namespace=namespace)
                logger.info(f"Deleted {len(ids)} vectors from namespace '{namespace}'")
            else:
                raise ValueError("Must provide either ids or delete_all=True")
            
            return response
            
        except Exception as e:
            logger.error(f"Error deleting vectors: {str(e)}")
            raise
    
    async def fetch(
        self,
        ids: List[str],
        namespace: str = ""
    ) -> Dict[str, Any]:
        """
        Fetch vectors by IDs
        
        Args:
            ids: List of vector IDs
            namespace: Namespace to fetch from
            
        Returns:
            Fetched vectors
        """
        try:
            if not self.index:
                await self.initialize()
            
            results = self.index.fetch(ids=ids, namespace=namespace)
            return results
            
        except Exception as e:
            logger.error(f"Error fetching vectors: {str(e)}")
            raise
    
    async def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the index
        
        Returns:
            Index statistics
        """
        try:
            if not self.index:
                await self.initialize()
            
            stats = self.index.describe_index_stats()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting index stats: {str(e)}")
            raise
    
    async def update_metadata(
        self,
        id: str,
        metadata: Dict[str, Any],
        namespace: str = ""
    ) -> Dict[str, Any]:
        """
        Update metadata for a vector
        
        Args:
            id: Vector ID
            metadata: New metadata
            namespace: Namespace
            
        Returns:
            Update response
        """
        try:
            if not self.index:
                await self.initialize()
            
            response = self.index.update(
                id=id,
                set_metadata=metadata,
                namespace=namespace
            )
            
            logger.info(f"Updated metadata for vector {id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating metadata: {str(e)}")
            raise
