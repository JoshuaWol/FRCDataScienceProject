def getCredentials():
    from dotenv import load_dotenv
    import base64
    import os
    load_dotenv()
    FIRST_API_AUTH_KEY = os.getenv("FIRST_API_AUTH_KEY")
    FIRST_API_USERNAME = os.getenv("FIRST_API_USERNAME")
    FIRST_API_ACCESS_TOKEN = FIRST_API_USERNAME + ":" + FIRST_API_AUTH_KEY
    
    return base64.b64encode(FIRST_API_ACCESS_TOKEN.encode()).decode()