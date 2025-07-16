from string import Template

from fastapi import APIRouter
from httpx import Response, get
from slugify import slugify
from thefuzz import process


router = APIRouter()


METACRITIC_SEARCH_TEMPLATE = Template(
    "https://backend.metacritic.com/finder/metacritic/autosuggest/{$game_title}?apiKey=1MOZgmNFxvmljaQR1X9KAij9Mo4xAY3u"
)
VALID_MATCH_THRESHOLD = 80


class MatchValidationError(RuntimeError):
    pass


def standardize_title(title: str) -> str:
    # slugify and substitute dashes by '%20'
    txt = "%20".join(slugify(title).split('-'))    
    return txt


async def request_metacritic_data(title: str) -> dict:
    url = METACRITIC_SEARCH_TEMPLATE.substitute(
        game_title=standardize_title(title)
    )
    resp:Response = get(url)
    resp.raise_for_status()
    return resp.json()


def find_best_title_correspondence(title, resp: dict) -> int:
    # aggregate titles in a list
    titles:list[str] = [x["title"] for x in resp["data"]["items"]]

    # make fuzzy search in 'item.title' field
    best_match:tuple[str, int] = process.extractOne(title, titles, score_cutoff= VALID_MATCH_THRESHOLD)
    if not best_match:
        raise MatchValidationError(f"No good match found for title {title}")
    best_match_idx:int = titles.index(best_match[0])

    return best_match_idx


def extract_metacritic_data(resp:dict, index:int) -> dict:
    raw_data = resp["data"]["items"][index]
    data = {
        "score": raw_data["criticScoreSummary"]["score"],
        "must_play": raw_data["mustPlay"],
        "genres": [x["name"] for x in raw_data["genres"]]
    }

    return data


@router.post("/search")
async def get_metacritic_data(title:str) -> dict:
    resp = await request_metacritic_data(title)
    index = find_best_title_correspondence(title, resp)
    data = extract_metacritic_data(resp, index)

    return data
