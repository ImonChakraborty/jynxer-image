import telebot
import google.generativeai as genai
import PIL.Image

TELEGRAM_BOT_TOKEN = 'enter your telegram bot token'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

genai.configure(api_key='Enter your gemini token')

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# Create a GenerativeModel instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Welcome fellow jynxer user!\nThis example will be able to explain image contents")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        img = PIL.Image.open(io.BytesIO(downloaded_file))
        response = model.generate_content(["summarize what is shown in this image.", img])
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")
print("Jynxer is Running!")

# Start the bot
bot.polling()
