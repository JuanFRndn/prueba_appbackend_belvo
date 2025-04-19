from pydantic import BaseModel

class BankLinkRequest(BaseModel):
    institution: str
    username: str
    password: str