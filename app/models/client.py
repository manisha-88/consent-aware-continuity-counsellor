from pydantic import BaseModel


class Client(BaseModel):
    client_id: str