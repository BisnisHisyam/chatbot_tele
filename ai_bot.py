import telebot
import google.generativeai as genai
import os

# --- KONFIGURASI ---
# Mengambil kunci rahasia dari Environment Variables di Render
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Hentikan skrip jika kunci tidak ditemukan
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("Error: Pastikan TELEGRAM_TOKEN dan GEMINI_API_KEY sudah diatur di Environment Variables.")
    exit()

# --- INISIALISASI BOT DAN AI ---
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- FUNGSI UNTUK MEMANGGIL AI ---
def get_ai_response(prompt):
    """Mengirim prompt ke Gemini dan mengembalikan responsnya."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error saat memanggil Gemini: {e}")
        return "Maaf, AI sedang mengalami gangguan. Coba lagi nanti."

# --- HANDLER PESAN TELEGRAM ---
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_prompt = message.text
    print(f"Menerima pesan: '{user_prompt}'")

    bot.send_chat_action(message.chat.id, 'typing')
    
    ai_reply = get_ai_response(user_prompt)
    
    bot.reply_to(message, ai_reply)

# --- MENJALANKAN BOT 24/7 ---
print("Bot AI telah aktif dan sedang mendengarkan...")
bot.infinity_polling()
