from dotenv import load_dotenv
import os
import base64


load_dotenv()


def get_frc_credentials():
    FIRST_API_AUTH_KEY = os.getenv("FIRST_API_AUTH_KEY")
    FIRST_API_USERNAME = os.getenv("FIRST_API_USERNAME")
    FIRST_API_ACCESS_TOKEN = FIRST_API_USERNAME + ":" + FIRST_API_AUTH_KEY
    
    return base64.b64encode(FIRST_API_ACCESS_TOKEN.encode()).decode()

def get_tba_credentials():
    TBA_API_AUTH_KEY = os.getenv("THE_BLUE_ALLIANCE_API_KEY")
    
    return TBA_API_AUTH_KEY