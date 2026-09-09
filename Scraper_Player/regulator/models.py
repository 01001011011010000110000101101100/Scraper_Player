from httpx import URL
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum


@dataclass(slots=True)
class EpisodeModel :

    number : str
    source_url : URL

@dataclass(slots=True)
class IconModel :

    title : str
    page_url : URL 
    icon_url : Optional[URL] = None

@dataclass(slots=True)
class PageDetailsModel :

    # 1. Strings :
    title : str
    description : str = "" 
    continuity : str = ""

    # 2. URLs :
    icon_url : Optional[URL] = None
    source_url : Optional[URL] = None

    # 3. Lists :
    categories : List[str] = field(default_factory=list)
    episodes_urls : List[EpisodeModel] = field(default_factory=list)


# class Language(Enum, str):
#     English = "english.json"
#     Arabic = "arabic.json"

# @dataclass(slots=True)
# class PageTextModel:
#     continuity: str = ""
#     description: str = ""
#     categories: str = ""
#     episode_count: List[str] = field(default_factory=list)
#     episode_button: List[str] = field(default_factory=list)