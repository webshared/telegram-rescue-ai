# Kherson Flood Relief Project 🇺🇦

We're running a Telegram bot to monitor multiple channels for SOS calls. Our bot uses OpenAI to sort out the real deal evacuation requests from the noise, then whips up a neat summary for our rescue boats.

Ми запустили бота в Telegram, щоб відстежувати кілька каналів для викликів SOS. Наш бот використовує OpenAI для відсіювання реальних запитів на евакуацію зі шуму, а потім складає чітке резюме для наших рятувальних човнів.

Telegram channel: https://t.me/KhersonEvacuation


# 🤝 Contributions Welcome!

Here's what we currently need:

1. **GPT-4 API ACCESS:** We aim to enhance the parsing of requests and the generation of summaries. Access to GPT-4 API could significantly boost our project's effectiveness and accuracy.

2. **PULL REQUESTS:** Got ideas? We're open to all kinds of contributions! Feel free to make a pull request, and let's collaborate to make this project better.


## How to run the script

### Install dependencies
```
pip install openai duckdb telethon
```

### Update the config
```
cp scripts/config.template.py scripts/config.py
```

Update `scripts/config.py` with your API keys, channel names, and preferred settings.

### Run
```
python ./srcipts/go.py
```

