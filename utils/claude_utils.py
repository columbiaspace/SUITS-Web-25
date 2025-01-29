from dotenv import load_dotenv
from anthropic import Anthropic
import os

# Load environment variables
load_dotenv()

def get_claude_client():
    """Initialize and return the Anthropic client."""
    try:
        return Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            # anthropic_version="2024-01-22"
        )
    except Exception as e:
        print(f"Error initializing Anthropic client: {str(e)}")
        return None

def get_claude_completion(prompt, model="claude-3-sonnet-20240229", stream=False):
    """
    Get completion from Claude models.
    
    Args:
        prompt (str): User prompt
        model (str): Claude model identifier
        stream (bool): Whether to stream the response
        
    Returns:
        str or generator: Response text or stream
    """
    client = get_claude_client()
    if not client:
        return None

    try:
        if stream:
            return client.messages.stream(
                model=model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
        else:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
    except Exception as e:
        print(f"Error getting Claude completion: {str(e)}")
        return None

def example_usage():
    """Example usage of Claude API functions."""
    # Basic completion
    response = get_claude_completion("Explain quantum computing in simple terms")
    if response:
        print("\nBasic completion:")
        print(response)

    # Streaming example
    print("\nStreaming response:")
    stream = get_claude_completion("Write a short poem about AI", stream=True)
    if stream:
        with stream as response:
            for chunk in response:
                if chunk.content:
                    print(chunk.content[0].text, end="", flush=True)
        print()

if __name__ == "__main__":
    example_usage() 