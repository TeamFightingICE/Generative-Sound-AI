import typer
from dotenv import load_dotenv
from loguru import logger

from src.frame_processing.core import run_frame_processing

app = typer.Typer()


@app.command()
def main():
    logger.info("Starting main process")
    run_frame_processing()


if __name__ == "__main__":
    load_dotenv()
    app()
