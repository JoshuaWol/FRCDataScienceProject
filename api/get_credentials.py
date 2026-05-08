def get_frc_credentials():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    import base64
    FIRST_API_AUTH_KEY = os.getenv("FIRST_API_AUTH_KEY")
    FIRST_API_USERNAME = os.getenv("FIRST_API_USERNAME")
    FIRST_API_ACCESS_TOKEN = FIRST_API_USERNAME + ":" + FIRST_API_AUTH_KEY
    
    return base64.b64encode(FIRST_API_ACCESS_TOKEN.encode()).decode()

def get_tba_credentials():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    TBA_API_AUTH_KEY = os.getenv("THE_BLUE_ALLIANCE_API_KEY")
    
    return TBA_API_AUTH_KEY