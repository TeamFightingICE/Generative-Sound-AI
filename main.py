import asyncio
import os

import typer
from dotenv import load_dotenv
from pyftg.socket.aio.gateway import Gateway
from typing_extensions import Annotated, Optional

from src.core import SampleSoundGenAI
from src.utils import setup_logging

app = typer.Typer(pretty_exceptions_enable=False)


async def start_process(host: str, port: int):
    host = os.environ.get("SERVER_HOST", host)
    port = int(os.environ.get("SERVER_PORT", port))
    gateway = Gateway(host, port)
    sound_genai = SampleSoundGenAI()
    gateway.register_sound(sound_genai)
    await gateway.start_sound(keep_alive=True)
    await gateway.close()


@app.command()
def main(
        host: Annotated[Optional[str], typer.Option(help="Host used by DareFightingICE")] = "127.0.0.1",
        port: Annotated[Optional[int], typer.Option(help="Port used by DareFightingICE")] = 31415):
    asyncio.run(start_process(host, port))


if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    app()
