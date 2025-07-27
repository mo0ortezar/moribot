# bot.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, CARD_NUMBER, ADMIN_ID

app = Client("morivpn_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

plans = {
    "20": 60,
    "30": 80,
    "40": 100,
    "60": 135,
    "80": 160,
    "100": 185,
}

# وقتی کاربر /start می‌زند
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "**👋 خوش اومدی به morivpn!**\n"
        "✨ اینجا بسته‌ها محدودیت زمانی ندارن، فقط محدودیت حجمی دارن.\n"
        "برای دیدن طرح‌ها و انتخاب، لطفاً از دستور /plan استفاده کن."
    )

# وقتی کاربر /plan می‌زند
@app.on_message(filters.command("plan"))
async def show_plans(client, message):
    buttons = []
    for gb, price in plans.items():
        buttons.append(
            [InlineKeyboardButton(f"{gb} گیگ - {price} تومن", callback_data=f"plan_{gb}")]
        )
    await message.reply(
        "💰 لطفاً یکی از طرح‌ها رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# وقتی کاربر یکی از دکمه‌ها رو می‌زند
@app.on_callback_query(filters.regex(r"^plan_\d+"))
async def handle_plan_selection(client, callback_query):
    gb = callback_query.data.split("_")[1]
    price = plans[gb]
    await callback_query.message.reply(
        f"✅ شما طرح {gb} گیگ رو انتخاب کردید.\n"
        f"لطفاً مبلغ *{price}* تومن به شماره کارت زیر واریز کنید:\n"
        f"`{CARD_NUMBER}`\n\n"
        "📸 سپس رسید واریز رو به صورت عکس ارسال کنید."
    )

# وقتی کاربر عکس رسید رو می‌فرسته
@app.on_message(filters.photo & filters.private)
async def handle_receipt(client, message):
    user_id = message.from_user.id
    caption = f"🧾 کاربر [{user_id}](tg://user?id={user_id}) رسید واریز فرستاد."
    await message.forward(ADMIN_ID)
    await client.send_message(ADMIN_ID, caption)
    await message.reply("✅ رسیدت ارسال شد! منتظر بررسی توسط ادمین باش.")

app.run()
