import os
import asyncio
import shlex
from typing import Tuple
from ..logging import LOGGER

def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    # Heroku me Git available nahi hota, env se info lo
    commit = os.getenv("GIT_COMMIT", "unknown")
    branch = os.getenv("GIT_BRANCH", "main")
    heroku_env = os.getenv("HEROKU_ENV", "false")

    LOGGER(__name__).info(
        f"Running in Heroku={heroku_env} | Branch={branch} | Commit={commit}"
    )

    # Requirements install karna ho to uncomment karo:
    # install_req("pip3 install --no-cache-dir -r requirements.txt")

    return {"commit": commit, "branch": branch}
