from typing import Final
import ollama 

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN: Final = "API API API TOKEN TOKEN TOKEN"
BOT_USERNAME: Final = "@qolda_pocket_bot"

async def get_ai_response(text: str) -> str:
    try:
        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'system',
                    'content': 'Ты — Qolda, умный ИИ помощник. Отвечай на языке пользователя (казахский или русский).'
                },
                {'role': 'user', 'content': text},
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Ошибка связи с Qolda: {e}"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сәлем! Qolda Pocket AI көмекшісі іске қосылды.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Просто напиши мне вопрос, и я отвечу с помощью Qolda.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
        else:
            return
    else:
        new_text = text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    response: str = await get_ai_response(new_text)

    print("Bot response:", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    print("Starting bot with Qolda AI (Ollama)...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=1)