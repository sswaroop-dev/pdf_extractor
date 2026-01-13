"""Gemini AI Client for PDF processing."""

import asyncio
import logging
from pathlib import Path

import google.generativeai as genai

from ...core.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google Gemini AI API."""

    def __init__(self):
        """Initialize Gemini client with API key."""
        self.api_key = settings.GEMINI_API_KEY
        self._model = None
        
        # Validate API key
        if not self.api_key or self.api_key.strip() == "":
            raise ValueError("GEMINI_API_KEY is not set in environment variables or .env file")
        
        if "your" in self.api_key.lower() or "placeholder" in self.api_key.lower() or len(self.api_key) < 20:
            raise ValueError(
                "GEMINI_API_KEY appears to be a placeholder. Please set a valid API key in your .env file. "
                "Get your API key from: https://makersuite.google.com/app/apikey"
            )
        
        genai.configure(api_key=self.api_key)
    
    @property
    def model(self):
        """Lazy load the model to ensure we get the latest available model."""
        if self._model is None:
            # Try models in order of free-tier availability
            # gemini-flash-latest and gemini-pro-latest typically have better free-tier limits
            models_to_try = [
                "gemini-flash-latest",  # Usually has better free-tier support
                # "gemini-pro-latest",    # Alternative with good free-tier
                # "gemini-2.0-flash",     # Newer model but stricter limits
            ]
            
            last_error = None
            for model_name in models_to_try:
                try:
                    self._model = genai.GenerativeModel(model_name)
                    logger.info(f"Successfully initialized model: {model_name}")
                    return self._model
                except Exception as e:
                    last_error = e
                    logger.debug(f"Failed to initialize {model_name}: {e}")
                    continue
            
            # If all models failed, raise error
            raise ValueError(
                f"Failed to initialize any Gemini model. Last error: {last_error}. "
                f"Please check available models or API key configuration."
            )
        return self._model

    async def extract_details(self, file_path: str, prompt: str) -> str:
        """Extract details from PDF using Gemini AI.
        
        Args:
            file_path: Path to the PDF file.
            prompt: Prompt to send to Gemini for extraction.
        
        Returns:
            Extracted text/data from Gemini.
        
        Raises:
            FileNotFoundError: If PDF file doesn't exist.
            ValueError: If Gemini fails to process the PDF.
            Exception: For other errors during processing.
        """
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            # 1. Upload to Google
            logger.info(f"Uploading file to Gemini: {file_path_obj.name}")
            raw_file = genai.upload_file(path=str(file_path_obj))
            
            # 2. Wait for Google to finish processing the PDF
            max_wait_time = 300  # 5 minutes max
            wait_time = 0
            while raw_file.state.name == "PROCESSING":
                if wait_time >= max_wait_time:
                    raise TimeoutError("Gemini file processing timed out")
                
                await asyncio.sleep(2)
                wait_time += 2
                raw_file = genai.get_file(raw_file.name)
                logger.debug(f"File processing status: {raw_file.state.name}")
            
            if raw_file.state.name == "FAILED":
                raise ValueError("Gemini failed to process the PDF.")
            
            # 3. Ask the AI to extract data
            logger.info("Requesting extraction from Gemini...")
            response = self.model.generate_content([raw_file, prompt])
            
            # Clean up uploaded file
            try:
                genai.delete_file(raw_file.name)
                logger.debug(f"Cleaned up uploaded file: {raw_file.name}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup uploaded file: {cleanup_error}")
            
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            
            # Provide more helpful error messages
            if "API key" in error_msg or "API_KEY" in error_msg or "401" in error_msg or "403" in error_msg:
                raise ValueError(
                    f"Gemini API authentication failed. Please check your GEMINI_API_KEY in .env file. "
                    f"Get your API key from: https://makersuite.google.com/app/apikey\n"
                    f"Original error: {error_msg}"
                )
            elif "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                # Extract retry delay if available
                retry_seconds = None
                if "retry in" in error_msg.lower():
                    import re
                    match = re.search(r"retry in ([\d.]+)s", error_msg.lower())
                    if match:
                        retry_seconds = float(match.group(1))
                
                error_detail = (
                    f"Gemini API quota/rate limit exceeded. "
                    f"This usually means you've hit the free tier limits.\n"
                    f"Options:\n"
                    f"  1. Wait and retry (quota resets periodically)\n"
                    f"  2. Upgrade your API plan at: https://ai.google.dev/pricing\n"
                    f"  3. Check your quota usage: https://ai.dev/rate-limit\n"
                )
                if retry_seconds:
                    error_detail += f"\nSuggested retry delay: {int(retry_seconds)} seconds"
                
                raise ValueError(f"{error_detail}\nOriginal error: {error_msg}")
            elif "400" in error_msg or "Bad Request" in error_msg:
                raise ValueError(
                    f"Invalid request to Gemini API. This might be due to file format or size issues. "
                    f"Original error: {error_msg}"
                )
            elif "timeout" in error_msg.lower():
                raise TimeoutError(
                    f"Request to Gemini API timed out. The file might be too large or the service is slow. "
                    f"Original error: {error_msg}"
                )
            else:
                logger.error(f"Error extracting details from {file_path}: {e}", exc_info=True)
                raise
    
    async def test_connection(self, prompt: str = "Say hello in one sentence.") -> str:
        """Test Gemini connection with a simple text prompt (no file upload).
        
        Args:
            prompt: Simple text prompt to test the connection.
        
        Returns:
            Response text from Gemini.
        
        Raises:
            Exception: If the connection test fails.
        """
        try:
            logger.info(f"Testing Gemini connection with prompt: {prompt[:50]}...")
            response = self.model.generate_content(prompt)
            logger.info("Gemini connection test successful")
            return response.text
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages
            if "API key" in error_msg or "API_KEY" in error_msg or "401" in error_msg or "403" in error_msg:
                raise ValueError(
                    f"Gemini API authentication failed. Please check your GEMINI_API_KEY in .env file. "
                    f"Get your API key from: https://makersuite.google.com/app/apikey\n"
                    f"Original error: {error_msg}"
                )
            elif "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                retry_seconds = None
                if "retry in" in error_msg.lower():
                    import re
                    match = re.search(r"retry in ([\d.]+)s", error_msg.lower())
                    if match:
                        retry_seconds = float(match.group(1))
                
                error_detail = (
                    f"Gemini API quota/rate limit exceeded.\n"
                    f"Suggested retry delay: {int(retry_seconds) if retry_seconds else 'unknown'} seconds"
                )
                raise ValueError(f"{error_detail}\nOriginal error: {error_msg}")
            else:
                logger.error(f"Gemini connection test failed: {e}", exc_info=True)
                raise ValueError(f"Gemini connection test failed: {error_msg}")