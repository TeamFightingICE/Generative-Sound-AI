import asyncio
from pathlib import Path

import typer
from dotenv import load_dotenv
from pyftg.socket.asyncio.generative_sound_gateway import \
    GenerativeSoundGateway

from src.core import SampleSoundGenAI
from src.utils import setup_logging

app = typer.Typer(pretty_exceptions_enable=False)


async def start_process():
    gateway = GenerativeSoundGateway(port=12345)
    sound_genai = SampleSoundGenAI()
    gateway.register(sound_genai)
    await gateway.run()
    await gateway.close()


@app.command()
def main():
    asyncio.run(start_process())


if __name__ == "__main__":
    Path("logs").mkdir(exist_ok=True)
    load_dotenv()
    setup_logging()
    app()
