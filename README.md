# Generative-Sound-AI

## Prerequisites

Before setting up the project, ensure you have Python 3.12 installed on your system.

## Quickstart with Docker

- Boot DareFightingICE
- Run the docker container
```
docker run -it --rm -e SERVER_HOST=host.docker.internal ghcr.io/teamfightingice/generative-sound-ai
```

## Instruction

__1. Install dependencies with pip__
```
pip install -r requirements.txt
```

__2. Install OpenAL Soft__

- For Windows, please copy the DLL files in `lib/windows` to `C:/Windows/System32` folder.

- For Linux (Ubuntu, other distros should be similar)
```
sudo apt-add-repository universe
sudo apt-get update
sudo apt-get install libopenal-dev makehrtf openal-info
```

- For MacOS
```
brew install openal-soft
echo 'export DYLD_LIBRARY_PATH="/opt/homebrew/opt/openal-soft/lib:$DYLD_LIBRARY_PATH"' >> ~/.zshrc
```

__3. Run the generative sound AI__
- Boot DareFightingICE
- Execute `main.py`
```
python main.py
```
