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

    msg: str = (
        subprocess.run(["legendary", "status"], capture_output=True)
        .stdout.splitlines()[0]
        .decode()
    )
    match_: re.Match | None = re.match(r"Epic account: (.*)", msg)
    if match_ is None:
        raise RuntimeError(
            f"Unexpected content from 'legendary status' result. Wanted 'Epic account: <acc>', got: {msg}"
        )
    acc: str = match_.groups()[0]

    return acc != "<not logged in>"
