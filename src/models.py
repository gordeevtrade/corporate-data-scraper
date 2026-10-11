"""
Lightweight data models for corporate and team member extraction.
Built with standard library dataclasses for zero-dependency execution.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json

@dataclass
class TeamMember:
    name: str
    title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    bio_summary: Optional[str] = None
    competencies: List[str] = field(default_factory=list)
    profile_url: Optional[str] = None

@dataclass
class ScrapeResult:
    url: str
    company_name: Optional[str] = None
    total_members_found: int = 0
    members: List[TeamMember] = field(default_factory=list)
    markdown_content: Optional[str] = None
    status: str = "SUCCESS"

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
