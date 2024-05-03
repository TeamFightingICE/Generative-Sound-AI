# Generative-Sound-AI

**Note:** This project uses Python 3.12.

First, install dependencies with pip.
```
pip install -r requirements.txt
pip install git+https://github.com/TeamFightingICE/pyftg@dev
```

For Windows
```
copy dll files in lib\windows\ to system32 folder
```

For Linux (Ubuntu, other distros should be similar)
```
sudo apt-add-repository universe
sudo apt-get update
sudo apt-get install libopenal-dev makehrtf openal-info
```

For MacOS
```
brew install openal-soft
echo 'export DYLD_LIBRARY_PATH="/opt/homebrew/opt/openal-soft/lib:$DYLD_LIBRARY_PATH"' >> ~/.zshrc
```

Run main process
```
python main.py
```
