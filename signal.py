from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random, asyncio

TOKEN = "8718142315:AAGC6HJIohd61szN8LFzKSPH1rtz5-12iUg"

PAIRS = [
"GBP/JPY OTC","EUR/USD OTC","AUD/USD OTC","AUD/NZD OTC",
"USD/BRL OTC","USD/ARS OTC","EUR/CHF OTC","EUR/JPY OTC"
]
TIMES = ["3 sec","5 sec","10 sec","15 sec","1 minute","5 minutes","15 minutes"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb=[[InlineKeyboardButton(p,callback_data=f"pair|{p}")] for p in PAIRS]
    await update.message.reply_text("Select Pair:",reply_markup=InlineKeyboardMarkup(kb))

async def cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()
    kind,val=q.data.split("|",1)
    if kind=="pair":
        context.user_data["pair"]=val
        kb=[[InlineKeyboardButton(t,callback_data=f"time|{t}")] for t in TIMES]
        await q.edit_message_text(f"Pair: {val}\n\nSelect Time:",reply_markup=InlineKeyboardMarkup(kb))
    else:
        pair=context.user_data["pair"]
        await q.edit_message_text("🔍 Scanning...")
        await asyncio.sleep(2)
        sig=random.choice(["BUY 📈","SELL 📉"])
        await q.message.reply_text(f"🧭 Signal: {sig}\n\n💠 Asset: {pair}\n⏱ Timeframe: {val}")

app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CallbackQueryHandler(cb))
app.run_polling()
