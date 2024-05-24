import asyncio

import typer
from dotenv import load_dotenv
from pyftg.socket.aio.gateway import Gateway

from src.core import SampleSoundGenAI
from src.utils import setup_logging

app = typer.Typer(pretty_exceptions_enable=False)


async def start_process():
    gateway = Gateway()
    sound_genai = SampleSoundGenAI()
    gateway.register_sound(sound_genai)
    await gateway.start_sound(keep_alive=True)
    await gateway.close()


@app.command()
def main():
    asyncio.run(start_process())


if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    app()
