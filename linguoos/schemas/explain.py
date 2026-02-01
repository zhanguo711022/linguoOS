from typing import List, Optional

from pydantic import BaseModel


class Explanation(BaseModel):
    title: str
    one_liner: str
    structure_template: List[str]
    example: Optional[str] = None
    return_to: str = "practice"
