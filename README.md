# BeerBot
Telegram bot for ordering beer from Zagovor Brewery.

For launching locally you need:
1. Define .env file in the root of the project with all fields (rename example.env -> .env)
2. pip install -r requirements.txt
3. Launch miklyx_bot.py 

OR you can launch it via Docker:
1. Execute command: docker build --tag zagovor_bot .
2. Execute command: docker run -d zagovor_bot:latest

That's it.
