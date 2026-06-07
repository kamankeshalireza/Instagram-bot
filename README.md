🤖 Instagram Downloader Bot
A Telegram bot that downloads Instagram posts, reels, IGTV, and stories – in original quality.

No watermarks. No ads. Just send a link and get your media.

🚀 Live demo? Add @YourBotUsername on Telegram (replace with your actual bot username)

✨ What it can do
Feature	Status
📸 Download photo posts	✅
🎥 Download reels (short videos)	✅
📺 Download IGTV videos	✅
🖼️ Download carousel posts (multiple images)	✅
📖 Download stories	✅
🎬 Original quality – no compression	✅
🔗 Just send a link – that's it	✅
🛠️ Tech Stack
Python 3.11+

python-telegram-bot – Telegram API wrapper

instaloader – Instagram content downloader

Railway / PythonAnywhere / Heroku – Deployment ready

🚀 Quick Start (Run it yourself)
Prerequisites
Python 3.11 or higher

A Telegram bot token from @BotFather

Local installation
bash
# Clone the repo
git clone https://github.com/kamankeshalireza/Instagram-bot.git
cd Instagram-bot

# Install dependencies
pip install -r requirements.txt

# Set your bot token (Linux/Mac)
export BOT_TOKEN="your_bot_token_here"

# Or on Windows (Command Prompt)
set BOT_TOKEN="your_bot_token_here"

# Run the bot
python bot.py
Deploy to the cloud (free options)
Platform	Difficulty	Best for
Railway	Easy	Always-on bot
PythonAnywhere	Medium	Free tier with limits
Heroku	Medium	Legacy setups (needs credit card now)
📱 How to use
Start a chat with your bot on Telegram

Send any Instagram link – for example:

https://www.instagram.com/p/Cxample123/

https://www.instagram.com/reel/Cxample456/

https://www.instagram.com/stories/username/123456789/

Wait 2–5 seconds

Receive the media file – ready to save or share

💡 Pro tip: The bot works in group chats too. Just mention the bot or reply to a message containing an Instagram link.

🧠 Why I built this

I got tired of sketchy websites and broken downloaders. So I made my own Telegram bot – simple, clean, and free. It's also a great way to learn how to:

Work with the Telegram Bot API

Use instaloader to interact with Instagram

Deploy Python bots to the cloud

📁 Project Structure

Instagram-bot/        
├── bot.py              # Main bot logic            
├── requirements.txt    # Dependencies          
├── .gitignore          # What not to commit          
└── LICENSE             # MIT license          
⚠️ Important notes
This bot uses instaloader, which works without an Instagram login (but may have rate limits)

For private profile content – the bot can't access it (Instagram's privacy rules)

Use responsibly. Don't spam or abuse the bot

🛣️ Roadmap (maybe coming soon)
Support for highlight downloads

Add progress indicator for large videos

Support downloading multiple links at once

Add /help command with examples in English & Persian

🤝 Contributing
Found a bug? Have a cool idea?

Open an Issue

Submit a Pull Request

Or just star ⭐ the repo to show love

📜 License
MIT – free to use, modify, and share. Just keep the original credits.

🌟 Show some love
If this bot helped you, give it a star ⭐ on GitHub and share it with friends who need a simple Instagram downloader.

💬 Need help?
Check the Issues tab first. If your problem isn't solved there, open a new issue with:

What you tried to download

Any error messages (copy-paste them)

Your environment (local, Railway, etc.)
