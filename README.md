# MCP Python Example

This example shows how to implement a Model Context Protocol (MCP) in Python and integrate with different LLM backends:

-   **OpenAI** via SDK v1.x (`OpenAI(api_key).chat.completions.create()`)
-   **Local LLaMA** via `llama-cpp-python`

## Setup

1. Create a virtual environment and activate:
    ```bash
    python3 -m venv venv
    source venv/bin/activate    # Linux/Mac
    venv\\Scripts\\activate   # Windows

    ```
2. Install lib

    ```bash
    pip install -r requirements.txt
    ```

3. Run server

    ```bash
    uvicorn server:app --reload
    ```

4. Run client

    ```bash
    python client.py
    ```
