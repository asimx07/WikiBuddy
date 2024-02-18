import requests
import os
import sys
import time

def wait_for_server():
    """
    Wait for the server to start by checking if it's reachable.
    """
    retries = 0
    max_retries = 10
    while retries < max_retries:
        try:
            # Try sending a test request to the server
            response = requests.get("http://localhost:8000/")
            if response.status_code == 200:
                # Server is running, return
                return
        except Exception as e:
            # Server not yet running, wait for a moment and retry
            retries += 1
            time.sleep(10)
    # If max retries reached, raise an error
    raise TimeoutError("Server did not start within the specified time.")

def test_app():
   
    # Make a POST request to the /openAiChat endpoint
    response = requests.get("http://localhost:8000/")

    # Check if the response is successful (status code 200)
    assert response.status_code == 200

    # Check if the response contains the expected content
    
    # Open the app in the browser
    import webbrowser
    webbrowser.open_new_tab("http://localhost:8000/gradio")
test_app()