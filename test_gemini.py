"""Standalone script to test Gemini API connection."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.speed_feed.gemini_client import GeminiClient


async def main():
    """Test Gemini connection with a simple prompt."""
    print("Testing Gemini API connection...\n")
    
    try:
        client = GeminiClient()
        print("✓ Gemini client initialized")
        
        # Test with a simple prompt
        prompt = "What is 2+2? Answer in one sentence."
        print(f"Prompt: {prompt}\n")
        
        # Try with retry logic for quota issues
        max_retries = 3
        retry_delay = 25  # seconds
        
        for attempt in range(max_retries):
            try:
                response = await client.test_connection(prompt)
                
                print("=== Gemini Test Result ===")
                print(f"Status: ✓ Success")
                print(f"Prompt: {prompt}")
                print(f"\nResponse: {response}")
                print("\n✓ Gemini API is working correctly!")
                return
                
            except ValueError as e:
                error_msg = str(e)
                if "quota" in error_msg.lower() or "429" in error_msg:
                    if attempt < max_retries - 1:
                        print(f"⚠ Quota limit hit. Waiting {retry_delay} seconds before retry {attempt + 2}/{max_retries}...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        print(f"\n✗ Test Failed after {max_retries} attempts")
                        print(f"Error: {error_msg}")
                        print("\n💡 Tip: Wait a few minutes and try again, or upgrade your API plan.")
                        sys.exit(1)
                else:
                    raise
            except Exception as e:
                print(f"\n✗ Test Failed")
                print(f"Error: {e}")
                sys.exit(1)
        
    except Exception as e:
        print(f"\n✗ Test Failed")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
