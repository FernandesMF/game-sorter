import re
import subprocess

from fastapi import APIRouter

router = APIRouter()


# """"
# Please  open the following URL: https://legendary.gl/epiclogin
# Please enter the "authorizationCode" value from the JSON response
# """


@router.get(
    "/status",
    response_description="Checks current state of authentication in epiic store",
    response_model=bool,
)
async def egs_not_logged() -> bool:

    msg = subprocess.run(
        ["legendary", "status"], capture_output=True
    ).stdout.splitlines()[0]
    match_: re.Match | None = re.match(r"Epic account: (.*)", msg.decode())
    acc: str | None = match_.groups()[0] if match_ else None

    return (acc is not None) and (acc != "<not logged in>")
