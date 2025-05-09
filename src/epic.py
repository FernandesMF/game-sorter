import re
import subprocess

from fastapi import APIRouter

router = APIRouter()


# """"
# Please  open the following URL: https://legendary.gl/epiclogin
# Please enter the "authorizationCode" value from the JSON response
# """


@router.get("")
async def weblogin_flow():

    is_logged: bool = await check_egs_auth()
    if not is_logged:
        return (
            "Please open the following URL: https://legendary.gl/epiclogin "
            "and enter the 'authorizationCode' value from the JSON response "
            "in a POST request to '/epic/authcode'"
        )


# TODO remove endpoint after the whole auth is implemented
@router.get(
    "/status",
    response_description="Checks current state of authentication in epic store",
    response_model=bool,
)
async def check_egs_auth() -> bool:

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


@router.post("/authcode")
async def authenticate_with_code(auth_code: str):

    msg = subprocess.run(
        ["legendary", "auth", "--code", auth_code], capture_output=True
    )

    is_logged = await check_egs_auth()
    if not is_logged:
        return f"Authentication did not work, please try again: {msg.stderr.decode()}"

    return "Authentication successful!"
