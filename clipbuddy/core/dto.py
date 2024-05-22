from typing import NamedTuple

class LlmItem(NamedTuple):
    name: str
    model: str
    prompt_ver: int
    temperature: float
    max_tokens: int
    request_timeout: int
    response_format: dict
    summary_template: str
    histroy_template: str