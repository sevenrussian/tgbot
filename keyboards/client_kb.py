from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_docs = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_reason = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_templates = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_email = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_choose_templates = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_admission_type = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_quest = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_promo = ReplyKeyboardMarkup(resize_keyboard=True)
kb_news_n_navigator = ReplyKeyboardMarkup(resize_keyboard=True)

# ===================== SUGAR MENU =====================

btn_back_to_main_menu = KeyboardButton('⬅ Вернуться в главное меню')

# ===================== REG MENU =====================

b12 = KeyboardButton('')
b13 = KeyboardButton('')
b14 = KeyboardButton('')
b15 = KeyboardButton('')
b16 = KeyboardButton('')

# ===================== MAIN MENU =====================

b11 = KeyboardButton('✍ Запросить справку / документ')
#b99 = KeyboardButton('💌')
btn_calendar = KeyboardButton('📅 Производственный календарь 2023')
btn_news_n_navigator = KeyboardButton('📲 Новости и Навигатор')

b32 = KeyboardButton('🎁 Наши плюшки')
btn_knowlage_base = KeyboardButton('🧠 База знаний')
btn_promo = KeyboardButton('👥 Программа Приведи Сотрудника')


kb_client.add(btn_news_n_navigator).add(btn_promo).add(b11).add(b32).insert(btn_knowlage_base)

# ===================== PROMO MENU =====================

#btn_send_resume = KeyboardButton('📄 Отправить резюме')
btn_cancel = KeyboardButton('❌ Отменить')
kb_client_promo.add(btn_cancel)

# ===================== GET DOCS MENU =====================

# b5 = KeyboardButton('✉ Сброс пароля от почты')
# btn_get_pass = KeyboardButton('✅ Оформить пропуск')
btn_ndfl = KeyboardButton('📃 Справка 2-НДФЛ')
btn_reference_with_income = KeyboardButton('📄 Справка с места работы с доходом')
btn_reference = KeyboardButton('📄 Справка с места работы без дохода')
btn_tk_copy_approved = KeyboardButton('📖 Копия ТК заверенная')
btn_tk_copy = KeyboardButton('📖 Копия ТК незаверенная')
btn_templates = KeyboardButton('📑 Шаблоны заявлений')

kb_client_docs.add(btn_tk_copy_approved).insert(btn_tk_copy)\
    .add(btn_reference_with_income).insert(btn_reference)\
    .add(btn_ndfl).insert(btn_templates)\
    .add(btn_back_to_main_menu)

# ===================== NAVIGATOR MENU =================
kb_news_n_navigator.add(btn_calendar).add(btn_back_to_main_menu)

# ===================== REASON MENU =====================

b17 = KeyboardButton('Получить новый пропуск')
b18 = KeyboardButton('Восстановить утерянный пропуск')
b19 = KeyboardButton('Продлить пропуск')

kb_client_reason.add(b17).add(b18).add(b19)

b33 = KeyboardButton('Постоянный пропуск')
b34 = KeyboardButton('Временный пропуск')

kb_client_admission_type.add(b33).insert(b34).add(btn_back_to_main_menu)

b21 = KeyboardButton('Оплачиваемый отпуск')
b22 = KeyboardButton('Неоплачиваемый отпуск')

kb_client_choose_templates.add(b21).add(b22).add(btn_back_to_main_menu)

# ===================== TEMPLATES MENU =====================

b30 = KeyboardButton('Почта @i-teco')
b31 = KeyboardButton('Почта @iteco-inno')

kb_client_email.add(b30).insert(b31).add(btn_back_to_main_menu)

# ===================== QUEST MENU =====================

b35 = KeyboardButton('🎁 Пройти квест')
b36 = KeyboardButton('❌ Отказаться от квеста')

kb_client_quest.add(b30, b36)

# ==================== REMOVED ========================
#b4 = KeyboardButton('🧠 База знаний')
#b5 = KeyboardButton('🌐 Соцсети')
#kb_client.add(b11).add(b88).add(b3).add(b1).insert(b32).add(b4).insert(b5)
#kb_client_docs.add(b9).add(b5).insert(b8).add(b7).insert(btn_get_pass).add(b76).add(b90).insert(b1).add(btn_back_to_main_menu)