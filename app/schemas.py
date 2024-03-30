# for  Pydantic models that define more or less a "schema" (a valid data shape).
from pydantic import BaseModel, StrictStr


class ArtDelete(BaseModel):
    art_id: int = None
    lager_id : int = None
    deleted : bool
    
class ArtCreate(BaseModel):
    art_number : str
    art_name : str
    art_info : str = ''
    ek: float = 0.0
    vk: float = 0.0
    producer: str = "Unbekannt" 