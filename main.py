from mcp.server.fastmcp import FastMCP
from typing import Union, Dict, Any, Optional
from sourcecode import send_http_request

# Create an MCP server
mcp = FastMCP("Endpoint Tester")

@mcp.tool()
def http_request(url: str) -> Union[str, Dict[str, Any], bytes]:
    """
    Send an HTTP request to a given URL and return the response data in its original format.
    
    Args:
        url (str): The URL to send the request to
    
    Returns:
        Union[str, Dict[str, Any], bytes]: Response data in its original format
        - JSON responses return as dictionary
        - Text responses return as string
        - Binary data returns as bytes
    
    Raises:
        requests.exceptions.RequestException: For network-related errors
        requests.exceptions.HTTPError: For HTTP error status codes
    """
    return send_http_request(url=url)

@mcp.tool()
def http_request_with_method(url: str, method: str):
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
    return send_http_request(url=url, method=method)

@mcp.tool()
def detailed_http_request( url: str, 
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
    return send_http_request(url, method, headers, data, params)

if __name__ == "__main__":
    mcp.run()