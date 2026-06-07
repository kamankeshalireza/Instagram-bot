import logging
import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import instaloader

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Instagram URL patterns
INSTAGRAM_PATTERNS = [
    r'https?://(?:www\.)?instagram\.com/p/([a-zA-Z0-9_-]+)',
    r'https?://(?:www\.)?instagram\.com/reel/([a-zA-Z0-9_-]+)',
    r'https?://(?:www\.)?instagram\.com/tv/([a-zA-Z0-9_-]+)',
    r'https?://(?:www\.)?instagram\.com/stories/([a-zA-Z0-9_.]+)/([0-9]+)'
]

def extract_instagram_url(text: str) -> str:
    """Extract Instagram URL from text"""
    for pattern in INSTAGRAM_PATTERNS:
        match = re.search(pattern, text)
        if match:
            # Return the full matched URL
            return match.group(0)
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued"""
    welcome_text = """
🤖 **Instagram Downloader Bot**

Send me any Instagram link and I'll download the media for you!

**Supported links:**
• Posts (photos & videos)
• Reels
• IGTV
• Stories

**How to use:**
Just paste an Instagram URL and send it to me.

**Example:**
`https://www.instagram.com/p/Cxample123/`

Made with ❤️ - Free & Open Source
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when /help is issued"""
    help_text = """
📖 **Help Guide**

1️⃣ Copy an Instagram link
2️⃣ Paste it here and send
3️⃣ Wait a few seconds
4️⃣ Receive your media!

**Supported formats:**
• Photos 📸
• Videos 🎥
• Carousels (multiple images) 🖼️
• Reels ⚡
• IGTV 📺
• Stories 📖

**Note:** Private accounts cannot be downloaded.

**Commands:**
/start - Welcome message
/help - This guide
/about - About the bot

Questions? Open an issue on GitHub.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send about information"""
    about_text = """
ℹ️ **About this bot**

Version: 2.0
Language: Python 3.11+
Library: python-telegram-bot v20+

**Features:**
• No watermarks
• Original quality
• Free forever
• Open source

**GitHub:** github.com/kamankeshalireza/Instagram-bot

**License:** MIT
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Download Instagram media from URL"""
    text = update.message.text
    url = extract_instagram_url(text)
    
    if not url:
        await update.message.reply_text("❌ No valid Instagram link found. Please send a correct Instagram URL.")
        return
    
    # Send processing message
    processing_msg = await update.message.reply_text("⏳ Downloading... Please wait a moment.")
    
    try:
        # Initialize instaloader
        loader = instaloader.Instaloader(
            download_videos=True,
            download_pictures=True,
            compress_json=False,
            save_metadata=False,
            post_metadata_txt=False,
            max_connection_attempts=3
        )
        
        # Extract shortcode from URL
        shortcode_match = re.search(r'/p/([a-zA-Z0-9_-]+)|/reel/([a-zA-Z0-9_-]+)|/tv/([a-zA-Z0-9_-]+)', url)
        
        if shortcode_match:
            shortcode = shortcode_match.group(1) or shortcode_match.group(2) or shortcode_match.group(3)
            
            # Get post
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            
            # Handle different post types
            if post.typename == 'GraphImage':
                # Single photo
                await update.message.reply_photo(
                    photo=post.url,
                    caption=f"📸 {post.owner_username}\n❤️ {post.likes} likes"
                )
                
            elif post.typename == 'GraphVideo':
                # Video post
                await update.message.reply_video(
                    video=post.video_url,
                    caption=f"🎥 {post.owner_username}\n❤️ {post.likes} likes"
                )
                
            elif post.typename == 'GraphSidecar':
                # Multiple images/videos (carousel)
                media_count = 0
                for node in post.get_sidecar_nodes():
                    media_count += 1
                    if node.is_video:
                        await update.message.reply_video(video=node.video_url)
                    else:
                        await update.message.reply_photo(photo=node.display_url)
                    if media_count >= 10:  # Limit to 10 media per post
                        break
                await update.message.reply_text(f"📚 Sent {media_count} media from this carousel post.")
                
            else:
                await update.message.reply_text("⚠️ This post type is not supported yet.")
                
        else:
            # Try story download
            story_match = re.search(r'/stories/([a-zA-Z0-9_.]+)/([0-9]+)', url)
            if story_match:
                username = story_match.group(1)
                story_id = story_match.group(2)
                
                # Get story
                profile = instaloader.Profile.from_username(loader.context, username)
                for story in profile.get_stories():
                    if story.id == int(story_id):
                        for item in story.get_items():
                            if item.is_video:
                                await update.message.reply_video(video=item.video_url)
                            else:
                                await update.message.reply_photo(photo=item.display_url)
                        break
                await update.message.reply_text(f"📖 Story from @{username}")
            else:
                await update.message.reply_text("❌ Could not process this link. Make sure it's a valid Instagram URL.")
        
        # Delete processing message
        await processing_msg.delete()
        
    except instaloader.exceptions.ProfileNotExistsException:
        await update.message.reply_text("❌ Profile not found or is private.")
    except instaloader.exceptions.InstaloaderException as e:
        logger.error(f"Instaloader error: {e}")
        await update.message.reply_text("⚠️ Download failed. The post might be private, deleted, or Instagram is blocking the request.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await update.message.reply_text("❌ An unexpected error occurred. Please try again later.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text("⚠️ Something went wrong. Please try again.")

def main():
    """Start the bot"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable not set!")
        return
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_instagram))
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    # Start polling
    logger.info("Bot started...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()