from typing import List, Dict, Any, Optional
from app.services.rag.vector_store import VectorStore
from app.services.openai.gpt4_service import GPT4Service
import logging

logger = logging.getLogger(__name__)


class RetrievalService:
    """Service for RAG (Retrieval-Augmented Generation)"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.gpt4_service = GPT4Service()
    
    async def retrieve_and_generate(
        self,
        query: str,
        user_id: int,
        top_k: int = 3,
        document_type: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve relevant context and generate response
        
        Args:
            query: User query
            user_id: User ID
            top_k: Number of relevant chunks to retrieve
            document_type: Filter by document type
            system_prompt: Custom system prompt
            
        Returns:
            Generated response with sources
        """
        try:
            # Retrieve relevant context
            logger.info(f"Retrieving context for query: {query[:100]}...")
            relevant_chunks = await self.vector_store.search_similar(
                query=query,
                user_id=user_id,
                top_k=top_k,
                document_type=document_type
            )
            
            if not relevant_chunks:
                return {
                    "answer": "I couldn't find any relevant information in your documents to answer this question.",
                    "sources": [],
                    "context_used": False
                }
            
            # Prepare context from retrieved chunks
            context = "\n\n".join([
                f"[Source {i+1}]: {chunk['text']}"
                for i, chunk in enumerate(relevant_chunks)
            ])
            
            # Prepare prompt with context
            default_system_prompt = """You are a helpful AI assistant. Answer the user's question based on the provided context.
If the context doesn't contain enough information to answer the question, say so clearly.
Always cite which source(s) you're using when answering."""
            
            prompt = f"""Context from documents:
{context}

Question: {query}

Please provide a clear and accurate answer based on the context above."""
            
            # Generate response
            logger.info("Generating response with GPT-4...")
            response = await self.gpt4_service.generate_response(
                prompt=prompt,
                system_prompt=system_prompt or default_system_prompt,
                max_tokens=500
            )
            
            # Format sources
            sources = [
                {
                    "document_id": chunk["document_id"],
                    "score": chunk["score"],
                    "text_preview": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"],
                    "chunk_index": chunk["chunk_index"]
                }
                for chunk in relevant_chunks
            ]
            
            return {
                "answer": response,
                "sources": sources,
                "context_used": True,
                "retrieved_chunks": len(relevant_chunks)
            }
            
        except Exception as e:
            logger.error(f"Error in retrieve_and_generate: {str(e)}")
            raise
    
    async def summarize_document(
        self,
        document_id: str,
        user_id: int,
        summary_type: str = "brief"
    ) -> Dict[str, Any]:
        """
        Summarize a document using RAG
        
        Args:
            document_id: Document ID
            user_id: User ID
            summary_type: Type of summary (brief, detailed, key_points)
            
        Returns:
            Document summary
        """
        try:
            # Retrieve all chunks for the document
            chunks = await self.vector_store.search_similar(
                query=document_id,  # Use document_id as query to get all chunks
                user_id=user_id,
                top_k=50  # Get more chunks for complete document
            )
            
            # Filter chunks for this specific document
            doc_chunks = [
                chunk for chunk in chunks
                if chunk["document_id"] == document_id
            ]
            
            if not doc_chunks:
                return {
                    "summary": "Document not found or empty.",
                    "success": False
                }
            
            # Sort chunks by index
            doc_chunks.sort(key=lambda x: x["chunk_index"])
            
            # Combine chunks
            full_text = "\n\n".join([chunk["text"] for chunk in doc_chunks])
            
            # Generate summary based on type
            prompts = {
                "brief": "Provide a brief 2-3 sentence summary of this document:",
                "detailed": "Provide a detailed summary covering all main points of this document:",
                "key_points": "Extract and list the key points from this document in bullet format:"
            }
            
            prompt = f"""{prompts.get(summary_type, prompts['brief'])}

{full_text}"""
            
            summary = await self.gpt4_service.generate_response(
                prompt=prompt,
                system_prompt="You are a helpful assistant that creates clear and accurate summaries.",
                max_tokens=800
            )
            
            return {
                "summary": summary,
                "document_id": document_id,
                "summary_type": summary_type,
                "chunk_count": len(doc_chunks),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error summarizing document: {str(e)}")
            raise
    
    async def answer_from_multiple_documents(
        self,
        query: str,
        user_id: int,
        document_ids: List[str],
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Answer query using multiple specific documents
        
        Args:
            query: User query
            user_id: User ID
            document_ids: List of document IDs to search
            top_k: Number of chunks per document
            
        Returns:
            Generated response with sources
        """
        try:
            all_chunks = []
            
            # Retrieve chunks from each document
            for doc_id in document_ids:
                chunks = await self.vector_store.search_similar(
                    query=query,
                    user_id=user_id,
                    top_k=top_k
                )
                
                # Filter for this document
                doc_chunks = [c for c in chunks if c["document_id"] == doc_id]
                all_chunks.extend(doc_chunks)
            
            # Sort by relevance score
            all_chunks.sort(key=lambda x: x["score"], reverse=True)
            
            # Take top chunks across all documents
            relevant_chunks = all_chunks[:top_k * 2]  # Get more chunks for better context
            
            # Generate response
            return await self.retrieve_and_generate(
                query=query,
                user_id=user_id,
                top_k=0  # We already have chunks
            )
            
        except Exception as e:
            logger.error(f"Error answering from multiple documents: {str(e)}")
            raise
    
    async def find_related_content(
        self,
        content: str,
        user_id: int,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find content related to given text
        
        Args:
            content: Content to find relations for
            user_id: User ID
            top_k: Number of related items
            
        Returns:
            List of related content
        """
        try:
            related = await self.vector_store.search_similar(
                query=content,
                user_id=user_id,
                top_k=top_k
            )
            
            return related
            
        except Exception as e:
            logger.error(f"Error finding related content: {str(e)}")
            raise