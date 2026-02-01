from typing import List, Literal, Optional

from pydantic import BaseModel


class PracticeItem(BaseModel):
    task_id: str
    module_id: str
    type: Literal["choice", "rewrite"]
    prompt: str
    options: Optional[List[str]] = None
