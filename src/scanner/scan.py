def scan_file(file_path):
    """
    Dummy scanner that checks if a file is empty or not.
    Replace with real scan logic as needed.
    """
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        if content:
            return {"status": "ok", "message": "File has content", "size": len(content)}
        else:
            return {"status": "empty", "message": "File is empty", "size": 0}
    except Exception as e:
        return {"status": "error", "message": str(e)}
