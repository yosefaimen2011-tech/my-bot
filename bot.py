from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "9282717190:AAFYRczja46euu5AttIzBY-0D9kCxZtfK2s"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏫 حكومي", callback_data="system_gov")],
        [InlineKeyboardButton("📊 إحصائياتي", callback_data="system_stats")],
        [InlineKeyboardButton("🎉 مسابقة", callback_data="system_comp")],
    ]
    await update.message.reply_text(f"أهلاً بيك يا {update.effective_user.first_name} 👋\n\nاختر نظام التعليم:", reply_markup=InlineKeyboardMarkup(keyboard))

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "system_gov":
        keyboard = [[InlineKeyboardButton("📚 أولى بكالوريا", callback_data="grade_1")],[InlineKeyboardButton("📚 تانية بكالوريا", callback_data="grade_2")]]
        await query.edit_message_text("✅ اخترت حكومي\n\nاختر الصف:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data in ["grade_1", "grade_2"]:
        context.user_data["grade"] = "أولى بكالوريا" if data == "grade_1" else "تانية بكالوريا"
        keyboard = [[InlineKeyboardButton("🎓 بكالوريا", callback_data="type_bac")],[InlineKeyboardButton("🏫 عام", callback_data="type_general")]]
        await query.edit_message_text(f"✅ اخترت {context.user_data['grade']}\n\nاختر النوع:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data in ["type_bac", "type_general"]:
        context.user_data["type"] = "بكالوريا" if data == "type_bac" else "عام"
        keyboard = [[InlineKeyboardButton("☕ JavaScript", callback_data="subject_js")]]
        await query.edit_message_text(f"✅ اخترت {context.user_data['type']}\n\nاختر المادة:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "subject_js":
        await query.edit_message_text(f"✅ اخترت JavaScript ({context.user_data.get('grade','')} - {context.user_data.get('type','')})\n\nتمام كده وقفنا هنا 👌")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.run_polling()
