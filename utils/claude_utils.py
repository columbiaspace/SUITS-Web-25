from dotenv import load_dotenv
from anthropic import Anthropic
import base64
import httpx

import os

# Load environment variables
load_dotenv()

def process_image(image_url, message_text="Describe this image."): 
    """
    Process an image using Claude's vision capabilities.
    
    Args:
        image_url (str): URL of the image to process
        message_text (str): Text prompt to send with the image
        
    Returns:
        str: Claude's response
    """
    try:
        # Get image data from URL
        image_response = httpx.get(image_url)
        image_response.raise_for_status()  # Raise exception for bad status codes
        
        # Determine media type from URL (basic implementation)
        media_type = "image/jpeg" if image_url.lower().endswith(('.jpg', '.jpeg')) else "image/png"
        
        # Encode image data
        image_data = base64.standard_b64encode(image_response.content).decode("utf-8")

        client = get_claude_client()
        if not client:
            return None

        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": message_text
                        }
                    ],
                }
            ],
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

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