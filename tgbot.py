import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import requests

# Add the Bot Token (Token provided by BotFather)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_TOKEN"  # For security, store the token as an environment variable
WEBAPP_URL = "WEBURL"  # Enter the URL of your Telegram WebApp here for test you can use ngrok
API_URL = "APIURL" # 

async def start(update: Update, context: CallbackContext):
    # EXAMPLE FOR CREATE USER AFTER /start COMMAND
    
    telegram_user = update.message.from_user
    user_data = {
        "telegram_id": telegram_user.id,
        "username": telegram_user.username or str(telegram_user.id),
        "first_name": telegram_user.first_name,
        "last_name": telegram_user.last_name or "" 
    }
    
    try:
        response = requests.post(f"{API_URL}/users/register", json=user_data)
        if response.status_code == 200 or response.status_code == 201:
            await update.message.reply_text(f"Hello {telegram_user.first_name}, your registration was successful!")
        else:
            await update.message.reply_text(f"There was a problem creating your registration. Please try again.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")
    # Show the user a button to access the WebApp
    
    keyboard = [
        [InlineKeyboardButton("Your Description", web_app={"url": WEBAPP_URL})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Welcome to the XYZ! You can open the WebApp by clicking the button below.", reply_markup=reply_markup)

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("This bot allows you to access the Learn2Earn WebApp. You can start by using the /start command.")

if __name__ == "__main__":
    # Start the bot application
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Define commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Listen and start the bot
    print("Starting the bot...")
    app.run_polling()