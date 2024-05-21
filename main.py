import asyncio

import typer
from dotenv import load_dotenv
from pyftg.socket.aio.gateway import Gateway

from src.core import SampleSoundGenAI
from src.utils import setup_logging
from TestAudio import TestAudio

app = typer.Typer(pretty_exceptions_enable=False)


async def start_process():
    gateway = Gateway()
    sound_genai = SampleSoundGenAI()
    test_audio = TestAudio()
    gateway.register_sound(sound_genai)
    gateway.register_ai("TestAudio", test_audio)
    task1 = gateway.start_sound()
    task2 = gateway.start_ai()
    task3 = gateway.run_game(["ZEN", "ZEN"], ["TestAudio", "Keyboard"], 1)
    await asyncio.gather(task1, task2, task3)
    await gateway.close()


@app.command()
def main():
    asyncio.run(start_process())


if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    app()
