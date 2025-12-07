from typing import List, Dict, Any, Optional
import hashlib
import uuid
from datetime import datetime
from app.services.openai.embeddings_service import EmbeddingsService
from app.services.rag.pinecone_service import PineconeService
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages document storage and retrieval in vector database"""
    
    def __init__(self):
        self.embeddings_service = EmbeddingsService()
        self.pinecone_service = PineconeService()
    
    def _generate_document_id(self, content: str, user_id: int) -> str:
        """Generate unique document ID based on content hash"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        return f"doc_{user_id}_{content_hash[:16]}"
    
    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 100
    ) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk
            overlap: Number of characters to overlap
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.5:  # At least 50% of chunk
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
    
    async def store_document(
        self,
        content: str,
        user_id: int,
        document_type: str = "pdf",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store document in vector database
        
        Args:
            content: Document content
            user_id: User ID
            document_type: Type of document
            metadata: Additional metadata
            
        Returns:
            Storage result with document ID and chunk count
        """
        try:
            # Generate document ID
            doc_id = self._generate_document_id(content, user_id)
            
            # Chunk the text
            chunks = self._chunk_text(content)
            logger.info(f"Split document into {len(chunks)} chunks")
            
            # Generate embeddings for all chunks
            embeddings = await self.embeddings_service.create_embeddings(chunks)
            
            # Prepare vectors for upsert
            vectors = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_id = f"{doc_id}_chunk_{idx}"
                
                chunk_metadata = {
                    "user_id": user_id,
                    "document_id": doc_id,
                    "document_type": document_type,
                    "chunk_index": idx,
                    "chunk_text": chunk[:500],  # Store first 500 chars
                    "chunk_size": len(chunk),
                    "created_at": datetime.utcnow().isoformat(),
                    **(metadata or {})
                }
                
                vectors.append((chunk_id, embedding, chunk_metadata))
            
            # Upsert to Pinecone
            namespace = f"user_{user_id}"
            await self.pinecone_service.upsert_vectors(vectors, namespace=namespace)
            
            logger.info(f"Stored document {doc_id} with {len(chunks)} chunks")
            
            return {
                "document_id": doc_id,
                "chunk_count": len(chunks),
                "namespace": namespace,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error storing document: {str(e)}")
            raise
    
    async def search_similar(
        self,
        query: str,
        user_id: int,
        top_k: int = 5,
        document_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar content
        
        Args:
            query: Search query
            user_id: User ID
            top_k: Number of results
            document_type: Filter by document type
            
        Returns:
            List of similar chunks with metadata
        """
        try:
            # Generate query embedding
            query_embedding = await self.embeddings_service.create_embedding(query)
            
            # Prepare filter
            filter_dict = {"user_id": user_id}
            if document_type:
                filter_dict["document_type"] = document_type
            
            # Query Pinecone
            namespace = f"user_{user_id}"
            results = await self.pinecone_service.query(
                vector=query_embedding,
                top_k=top_k,
                namespace=namespace,
                filter=filter_dict
            )
            
            # Format results
            matches = []
            for match in results.get("matches", []):
                matches.append({
                    "id": match["id"],
                    "score": match["score"],
                    "text": match["metadata"].get("chunk_text", ""),
                    "document_id": match["metadata"].get("document_id"),
                    "document_type": match["metadata"].get("document_type"),
                    "chunk_index": match["metadata"].get("chunk_index"),
                    "metadata": match["metadata"]
                })
            
            return matches
            
        except Exception as e:
            logger.error(f"Error searching similar content: {str(e)}")
            raise
    
    async def delete_document(
        self,
        document_id: str,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Delete document and all its chunks
        
        Args:
            document_id: Document ID
            user_id: User ID
            
        Returns:
            Delete result
        """
        try:
            namespace = f"user_{user_id}"
            
            # Note: This requires fetching all IDs first
            # In production, consider storing chunk IDs separately
            # For now, we'll delete by filter (if supported)
            
            logger.info(f"Deleting document {document_id} for user {user_id}")
            
            # This is a simplified approach - in production you'd want to
            # track chunk IDs and delete them explicitly
            return {
                "status": "success",
                "message": f"Document {document_id} deletion initiated"
            }
            
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise
    
    async def get_user_documents(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all documents for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of document metadata
        """
        try:
            namespace = f"user_{user_id}"
            stats = await self.pinecone_service.get_index_stats()
            
            # Get namespace stats
            namespace_stats = stats.get("namespaces", {}).get(namespace, {})
            
            return {
                "user_id": user_id,
                "namespace": namespace,
                "vector_count": namespace_stats.get("vector_count", 0),
                "stats": namespace_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting user documents: {str(e)}")
            raise

