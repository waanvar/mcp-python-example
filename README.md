# MCP Python Example

ตัวอย่างนี้แสดงการใช้งาน Model Context Protocol (MCP) ด้วย Python

## การติดตั้ง

1. สร้าง virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\\Scripts\\activate    # Windows
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
