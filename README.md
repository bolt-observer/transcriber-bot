# Transcriber Bot 
Telegram bot that transcribes audio messages sent to it.

The bot keeps no state and deletes files after processing.

PSA: this is under heavy development

## Deployment
```
git clone https://github.com/bolt-observer/transcriber-bot.git
cd transcriber-bot
pip install -r requirements.txt 
cp example_settings.py settings.py
# edit settings.py
python transcriberbot.py
```

## Configuration
`TELEGRAM_BOT_TOKEN` - Follow [telegram's](https://core.telegram.org/bots#how-do-i-create-a-bot) instruction on how to create your own telegram bot. This will provide you with a token that you put in `settings.py` 

`MODEL_PATH` - Download one of the whisper models converted to ggml format from [HuggingFace](https://huggingface.co/ggerganov/whisper.cpp) and put the path to the file in `settings.py`. Example `MODEL_PATH="~/whisper.cpp/models/ggml-base.en.bin"`

## Todo
- audio file handling
- better error handling
