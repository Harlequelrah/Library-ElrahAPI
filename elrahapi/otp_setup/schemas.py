from pydantic import BaseModel

class OTPVerification(BaseModel):
    otp:str
    temp_token:str
