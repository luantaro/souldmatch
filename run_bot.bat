@echo off
echo Installing dependencies...
pip install aiogram==3.15.0 python-dotenv==1.0.0

echo Starting SoulMatch Bot...
python bot.py

pause
