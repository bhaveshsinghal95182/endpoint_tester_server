import requests
import json
from typing import Union, Dict, Any, Optional

def send_http_request(
    url: str, 
    method: str = 'GET', 
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Union[str, Dict[str, Any]]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Union[str, Dict[str, Any], bytes]:
    """
    Send an HTTP request to a given URL and return the response data in its original format.
    
    Args:
        url (str): The URL to send the request to
        method (str): HTTP method (GET, POST, PUT, DELETE, etc.). Default is 'GET'
        headers (dict, optional): HTTP headers to include in the request
        data (str/dict, optional): Data to send in the request body
        params (dict, optional): URL parameters for GET requests
        timeout (int): Request timeout in seconds. Default is 30
    
    Returns:
        Union[str, Dict[str, Any], bytes]: Response data in its original format
        - JSON responses return as dictionary
        - Text responses return as string
        - Binary data returns as bytes
    
    Raises:
        requests.exceptions.RequestException: For network-related errors
        requests.exceptions.HTTPError: For HTTP error status codes
    """
    
    try:
        # Send the HTTP request
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            data=data,
            params=params,
            timeout=timeout
        )
        
        response.raise_for_status()
        
        content_type = response.headers.get('content-type', '').lower()
        
        if 'application/json' in content_type:
            # Return JSON as dictionary
            try:
                return response.json()
            except json.JSONDecodeError:
                # If JSON parsing fails, return as text
                return response.text
        
        elif any(text_type in content_type for text_type in ['text/', 'application/xml', 'application/html']):
            # Return text-based content as string
            return response.text
        
        else:
            # Return binary content as bytes
            return response.content
            
    except requests.exceptions.Timeout:
        raise Exception(f"Request to {url} timed out after {timeout} seconds")
    
    except requests.exceptions.ConnectionError:
        raise Exception(f"Failed to connect to {url}")
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error {response.status_code}: {e}")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")


# Example usage:
if __name__ == "__main__":
    # Example 1: GET request for JSON data
    try:
        json_data = send_http_request("https://jsonplaceholder.typicode.com/posts/1")
        print("JSON Response:", json_data)
        print("Type:", type(json_data))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: GET request for text/HTML
    try:
        html_data = send_http_request("https://httpbin.org/html")
        print("\nHTML Response:", html_data[:100] + "...")
        print("Type:", type(html_data))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: POST request with JSON data
    try:
        post_data = {
            "title": "Test Post",
            "body": "This is a test",
            "userId": 1
        }
        response = send_http_request(
            "https://jsonplaceholder.typicode.com/posts",
            method="GET",
            headers={"Content-Type": "application/json"},
            data=json.dumps(post_data)
        )
        print("\nPOST Response:", response)
        print("Type:", type(response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: GET request with parameters
    try:
        params_response = send_http_request(
            "https://httpbin.org/get",
            params={"key1": "value1", "key2": "value2"}
        )
        print("\nGET with params:", params_response)
    except Exception as e:
        print(f"Error: {e}")