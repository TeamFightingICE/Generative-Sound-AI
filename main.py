import asyncio

import typer
from dotenv import load_dotenv
from pyftg.socket.asyncio.generative_sound_gateway import \
    GenerativeSoundGateway

from src.core import SampleSoundGenAI

app = typer.Typer()


async def start_process():
    gateway = GenerativeSoundGateway(port=12345)
    sound_genai = SampleSoundGenAI()
    gateway.set_sound_ai(sound_genai)
    await gateway.run()
    await gateway.close()


@app.command()
def main():
    asyncio.run(start_process())


if __name__ == "__main__":
    load_dotenv()
    app()
