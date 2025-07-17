
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7351444454:AAESOGSebXeQn4wI7Xvxbz_WLBCj4tqUnxE"
REQUIRED_CHANNELS = ['@YourChannel1', '@YourChannel2']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    user_id = user.id
    user_name = user.full_name
    username = user.username or "Not Set"

    try:
        photos = await context.bot.get_user_profile_photos(user_id)
        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            await context.bot.send_photo(chat_id=chat_id, photo=file_id)
    except:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ প্রোফাইল ফটো পাওয়া যায়নি।")

    msg = f"""👤 আপনার তথ্য:
🔹 নাম: {user_name}
🔹 ইউজারনেম: @{username}
🔹 ইউজার আইডি: `{user_id}`"""
    await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')

    all_joined = True
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                all_joined = False
                break
        except:
            all_joined = False
            break

    if all_joined:
        await context.bot.send_message(chat_id=chat_id, text="✅ ধন্যবাদ! আপনি সব চ্যানেলে যুক্ত হয়েছেন। নিচে আপনার ফাইল:")
        file = InputFile("my_file.pdf")
        await context.bot.send_document(chat_id=chat_id, document=file)
    else:
        channel_list = "\n".join(REQUIRED_CHANNELS)
        await context.bot.send_message(chat_id=chat_id,
            text=f"❌ অনুগ্রহ করে নিচের সব চ্যানেলে জয়েন করুন:\n\n{channel_list}\n\nতারপর /start আবার দিন।")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
