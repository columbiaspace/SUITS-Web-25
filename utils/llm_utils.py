from openai import OpenAI
from dotenv import load_dotenv
from rich.markdown import Markdown
from rich.console import Console
from anthropic import Anthropic
import os

# Load environment variables
load_dotenv()

# Initialize clients and console
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
perplexity_client = OpenAI(
    api_key=os.getenv('PERPLEXITY_API_KEY'), 
    base_url="https://api.perplexity.ai"
)
claude_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
console = Console()

def get_openai_completion(messages, model="gpt-4o"):
    """
    Get completion from OpenAI models.
    
    Args:
        messages (list or str): List of message dictionaries or a single string query
        model (str): OpenAI model identifier
        
    Returns:
        tuple: (updated_messages, success, response/error_message)
    """
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    try:
        if model != "gpt-4o":
            messages = [msg for msg in messages if msg["role"] != "system"]

        response = openai_client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        ai_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ai_response})
        
        return messages, True, ai_response
        
    except Exception as e:
        return messages, False, str(e)

def get_perplexity_completion(messages, model="sonar-pro", stream=False):
    """
    Get completion from Perplexity models.
    
    Args:
        messages (list or str): List of message dictionaries or a single string query
        model (str): Perplexity model name
        stream (bool): Whether to stream the response
        
    Returns:
        tuple: (updated_messages, success, response/error_message)
    """
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    # Filter out system messages as Perplexity might not handle them
    messages = [msg for msg in messages if msg["role"] != "system"]

    params = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "stream": stream
    }

    try:
        response = perplexity_client.chat.completions.create(**params)
        if stream:
            return messages, True, response
        
        ai_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ai_response})
        return messages, True, ai_response
    except Exception as e:
        return messages, False, str(e)

def get_claude_completion(messages, model="claude-3-sonnet-20240229"):
    """
    Get completion from Claude models.
    
    Args:
        messages (list or str): List of message dictionaries or a single string query
        model (str): Claude model identifier
        
    Returns:
        tuple: (updated_messages, success, response/error_message)
    """
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    
    try:
        response = claude_client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[msg for msg in messages if msg["role"] != "system"]
        )
        
        ai_response = response.content[0].text
        messages.append({"role": "assistant", "content": ai_response})
        
        return messages, True, ai_response
        
    except Exception as e:
        return messages, False, str(e)

def get_llm_completion(query, model="gpt-4o", stream=False):
    """
    Unified interface for getting completions from OpenAI, Perplexity, or Claude models.
    
    Args:
        query (str or list): User query or message list
        model (str): Model identifier (e.g., "gpt-4o", "sonar-pro", "claude-3-sonnet")
        stream (bool): Whether to stream the response (Perplexity only)
        
    Returns:
        tuple: (success, response/error_message)
    """
    # Claude models
    if model.startswith("claude"):
        messages, success, response = get_claude_completion(query, model)
        return success, response
    
    # Perplexity models
    elif model.startswith("sonar"):
        messages, success, response = get_perplexity_completion(query, model, stream)
        return success, response
    
    # OpenAI models
    else:
        messages, success, response = get_openai_completion(query, model)
        return success, response

def interactive_chat():
    """Interactive chat interface supporting OpenAI, Perplexity, and Claude models."""
    models = {
        "1": "gpt-4o",
        "2": "o1-preview",
        "3": "o1-mini",
        "4": "sonar-pro",
        "5": "sonar",
        "6": "sonar-reasoning",
        "7": "claude-3-sonnet-20240229",
        "8": "claude-3-opus-20240229",
        "9": "claude-3-haiku-20240307"
    }
    
    print("\nAvailable models:")
    for key, model in models.items():
        print(f"{key}: {model}")
    
    model_choice = input("\nChoose a model (1-9) or press Enter for default (gpt-4o): ").strip()
    selected_model = models.get(model_choice, "gpt-4o")
    print(f"\nUsing model: {selected_model}")

    messages = []
    if selected_model == "gpt-4o":
        messages.append({
            "role": "system",
            "content": "You are a helpful AI assistant. Respond in a friendly and concise manner."
        })
    
    print("\nChat started! (Type 'quit' to end)")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("\nGoodbye!")
            break
            
        success, response = get_llm_completion(
            messages + [{"role": "user", "content": user_input}] if messages else user_input,
            selected_model
        )
        
        if success:
            print("\nAI:")
            if isinstance(response, str):
                md = Markdown(response)
                console.print(md)
            else:  # Streaming response
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        print(chunk.choices[0].delta.content, end="")
                print()
        else:
            print(f"\nError: {response}")
            break

if __name__ == "__main__":
    interactive_chat() 