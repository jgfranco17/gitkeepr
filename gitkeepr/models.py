from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class GithubRepository:
    name: str
    private: bool
    url: str
    topics: List[str]

    @classmethod
    def from_json(cls, json_data: Dict[str, str]) -> "GithubRepository":
        return cls(
            name=json_data["name"],
            private=json_data["private"],
            url=json_data["html_url"],
            topics=json_data["topics"],
        )
