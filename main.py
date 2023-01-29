#Libraries necessary to import
import telegram
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CallbackContext,CommandHandler,CallbackQueryHandler,ConversationHandler
from telegram.ext.updater import Updater
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from translate import Translator
import logging
import random
import qrcode

#Logging functions allow developers to track the actions and events that occur within the bot.
#It is a crucial tool for maintaining and improving the functionality of Telegram bots.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
lang=""

#Function to generate a QR Code to join FluoLingo Community
def create_qr(update, context):
    link = 'https://t.me/+tRwdGI1KD-o3MDRl'
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('qr_code.png')
    with open('qr_code.png', 'rb') as f:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)

#This function generates buttons to choose the language
def select_lang(update:Update,context:CallbackContext)->None:
    keyboard=[
        [
            InlineKeyboardButton("German",callback_data="German"),
            InlineKeyboardButton("French",callback_data="French")
        ],[
            InlineKeyboardButton("Japanese",callback_data="Japanese"),
            InlineKeyboardButton("Hindi",callback_data="Hindi"),
        ]
    ]
    reply_keyboard=InlineKeyboardMarkup(keyboard,one_time_keyboard=True)
    update.message.reply_text('Which language do u want to learn in?',reply_markup=reply_keyboard)

#Function to translate and return user input sentences in language selected by user.     
def lang_translator(user_input):
    global lang
    translator=Translator(from_lang="english",to_lang=lang)
    translation = translator.translate(user_input)
    return translation

#Function which stores the data generated on selecting a button.
def button(update:Update,context:CallbackContext)->None:
    global lang
    lang=update.callback_query.data.lower()
    query=update.callback_query
    query.answer()
    query.edit_message_text(text=f"{query.data},has been selected for learning! Let's start!")
 
#Takes user input and displays the translated sentence.
def reply(update, context):
    user_input=update.message.text
    update.message.reply_text(lang_translator(user_input))
    
#Function containing all video resources of languages required for learning.    
def french_resources(update,context):
    update.message.reply_text('''
    Beginner's level tutorial resources:
    https://www.youtube.com/watch?v=91lIllsNR6c&list=PLfDmeEHel1x3o_e4UjWXR4kClH7ZfAgZ9
    
    intermediate level tutorial resources:
    https://www.youtube.com/watch?v=IBOY7qY-hhU&list=PLfDmeEHel1x3VnQSxqgjY1ZgZbF4u34P0
   
    advanced level tutorial resources:
    https://www.youtube.com/watch?v=IwMjSFXhG34&list=PLfDmeEHel1x0Ta1jNYTpAO8fhyLgllt7q
       ''')   
def japanese_resources(update, context):
    update.message.reply_text('''
    Beginner's level tutorial resources:
    https://www.youtube.com/watch?v=4bbWx7VVGAU&list=PLqzIFY9f_F_75pRpAV3iO_RRje0fwVo8Y
    
    intermediate level tutorial resources:
    https://www.youtube.com/watch?v=JUqh9PuuOjM&list=PLgoGx_gLcCZwRwQmrOhw-aFBNfPhn2b00
   
    advanced level tutorial resources:
    https://www.youtube.com/watch?v=W3DhBZwfL2M&list=PLgoGx_gLcCZyNMqXeTCN4kIjgAYoIf2zl
       ''')    
def german_resources(update, context):
    update.message.reply_text("""
    Beginner's level tutorial resources:
    https://www.youtube.com/watch?v=RuGmc662HDg&list=PLF9mJC4RrjIhS4MMm0x72-qWEn1LRvPuW
    https://www.learngermanonline.org/spelling-and-punctuation/
    https://www.learngermanonline.org/pronunciation/
    https://www.learngermanonline.org/free-grammar-exercises/
    
    intermediate level tutorial resources:
    https://www.youtube.com/watch?v=WGMXaRe6UKA&list=PLF9mJC4RrjIhhEGuI2x4_WWaIyn9q7MzV
    
    advanced level tutorial resources:
    https://www.youtube.com/watch?v=FcbI5gIhxFU&list=PLk1fjOl39-53pjPz2VLCeu5vjOUMKZ22O
       """)
    
#Functions containing flashcards(alphabets and numbers) of all languages.    
def French_Numbers(update, context):
    photo = r"french_numbers.png"
    chat_id = update.message.chat_id
    bot.send_photo(chat_id = chat_id, photo=open(photo, "rb"))
def French_Alphabets(update, context):
    photo = r"french_alphabets.png"
    chat_id = update.message.chat_id
    bot.send_photo(chat_id = chat_id, photo=open(photo, "rb"))
def German_Numbers(update, context):
    photo = r"german_numbers.png"
    chat_id = update.message.chat_id
    bot.send_photo(chat_id = chat_id, photo=open(photo, "rb"))
def German_Alphabets(update, context):
    photo = r"german_alphabets.png"
    chat_id = update.message.chat_id
    bot.send_photo(chat_id = chat_id, photo=open(photo, "rb"))
def Japanese_Numbers(update, context):
    photo = r"japanese_numbers.png"
    chat_id = update.message.chat_id
    bot.send_photo(chat_id = chat_id, photo=open(photo, "rb"))
def Japanese_Alphabets(update, context):
    photo = r"japanese_alphabets.png"
    chat_id = update.message.chat_id
    bot.send_photo(chat_id = chat_id, photo=open(photo, "rb"))    

#Function displaying flashcards(Alphabets and Numbers) based on language selected.    
def flashcard(update:Update,context:CallbackContext)->None:
    global lang
    if lang=="german":
        update.message.reply_text('Alphabets in German:')
        German_Alphabets(update,context)
        update.message.reply_text('Numbers in German:')
        German_Numbers(update,context)
    elif lang=="french":
        update.message.reply_text('Alphabets in French:')
        French_Alphabets(update,context)
        update.message.reply_text('Numbers in French:')
        French_Numbers(update,context)
    elif lang=="japanese":
        update.message.reply_text('Alphabets in Japanese:')
        Japanese_Alphabets(update,context)
        update.message.reply_text('Numbers in Japanese:')
        Japanese_Numbers(update,context)
    else:
        update.message.reply_text('Invalid')    

#Function displaying resources based on language selected.          
def resources(update:Update,context:CallbackContext)->None:
    global lang
    if lang=="german":
        german_resources(update,context)
    elif lang=="french":
        french_resources(update,context)
    elif lang=="japanese":
        japanese_resources(update,context)
    else:
        update.message.reply_text('Invalid')
        

# You can store the user's credentials in a database
# or in a file, for this example we will use a dictionary
users = {
    # username: password
    'username1': 'password1',
    'username2': 'password2',
    'username3': 'password3',
    'username4': 'password4',
}

#Function to authenticate user credentials. 
def login(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Please enter your username:")
    return 'USERNAME'

def username(update, context):
    username = update.message.text
    if username in users:
        context.user_data['username'] = username
        context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks! Please enter your password:")
        return 'PASSWORD'
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid username. Please try again.")
        return 'USERNAME'
def password(update, context):
    password = update.message.text
    username = context.user_data['username']
    if password == users[username]:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome, you are logged in!")
        # Perform some action after login
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid password. Please try again.")
        return 'PASSWORD'
def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Login process canceled.")
    return ConversationHandler.END

#Function for greeting.
def greet(update, context):
    logger.info("User {} started the bot".format(update.message.from_user.username))
    #user_input=update.message.text
    #if user_input.lower() in ["Hello",:
    update.message.reply_text("Hello, I'm FluoLingo your guide in the journey of learning new language.")

#Functions to create a quiz for user, based on language selected.
#Validating user score based on performance. 
def start_quiz(update, context):
    global lang
    if lang=='french':
        quiz_questions={'Which one of the following means "red":':'rouge',
                        'Which one of the following means the number "six"?':'six',
                        'What is "nose" in French?':'nez',
                        'How would you write "father"?':'pere',
                        'How would you write "raining"?':'pleut'}
    elif lang=='german':
        quiz_questions={'Translate "Wo ist da salz"':'where is the salt',
                        'Translate "die speisekarte bitte"':'The menu please',
                        'Translate "Guten abend"':'good evening',
                        'What is called "Salat" in German?':'salad',
                        'What is called "Excuse me" in German?':'Entschuldigung'}
    elif lang=='japanese':
        quiz_questions={'Translate "ご飯"':'rice',
                        'Translate "すし"':'sushi',
                        'Translate "お願いします"':'please',
                        'What is called "Water" in Japanese?':'水',
                        'What is called "Hello" in German?':'こんにちは'}
    else:
        return -1
    context.user_data['quiz_questions'] = quiz_questions
    context.user_data['score'] = 0
    ask_question(update, context)
    return 1

def ask_question(update, context):
    quiz_questions = context.user_data['quiz_questions']
    if quiz_questions:
        question = random.choice(list(quiz_questions.keys()))
        correct_answer = quiz_questions[question]
        update.message.reply_text(question)
        context.user_data['correct_answer'] = correct_answer
        context.user_data['question'] = question
    else:
        update.message.reply_text("No more questions.")
        end_quiz(update, context)
        return ConversationHandler.END

def check_answer(update, context):
    user_answer = update.message.text
    try:
        correct_answer = context.user_data['correct_answer']
    except:
        return -1
    question = context.user_data['question']
    score = context.user_data['score']
    if user_answer == correct_answer:
        update.message.reply_text("Correct!")
        score += 1
    else:
        update.message.reply_text("Incorrect. The correct answer is: " + correct_answer)
    context.user_data['score'] = score
    context.user_data['quiz_questions'].pop(question)
    ask_question(update, context)
    return 1

def end_quiz(update, context):
    score = context.user_data['score']
    update.message.reply_text("Quiz Ended, Your final score is: " + str(score))
    context.user_data.clear()
    return ConversationHandler.END

#Function taking feedback from user
def feedback(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the feedback form! What's your name?")
    return 'NAME'

def name(update, context):
    user_name = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Thanks, {user_name}! How would you rate our service on a scale of 1-10?")
    context.user_data['name'] = user_name
    return 'RATING'

def rating(update, context):
    user_rating = update.message.text
    context.user_data['rating'] = user_rating
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks for your feedback! Can you please tell us what we can improve on?")
    return 'IMPROVEMENT'

def improvement(update, context):
    user_improvement = update.message.text
    context.user_data['improvement'] = user_improvement
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks for your feedback! We appreciate your input.")
    feedback_data = context.user_data
    # save feedback_data to database or file
    return ConversationHandler.END

def cancel1(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks for your feedback!.We appreciate your input.")
    return ConversationHandler.END


bot = telegram.Bot(token="YOUR BOT_TOKEN")
def main():
    api="YOUR BOT_TOKEN"
    updater=Updater(api,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',greet))
    dp.add_handler(CommandHandler('select_lang',select_lang))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('resources',resources))
    dp.add_handler(CommandHandler('flashcard',flashcard))
    dp.add_handler(CommandHandler('create_qr', create_qr))
    conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start_quiz", start_quiz)],
    states={1: [MessageHandler(Filters.text, check_answer)]},
    fallbacks=[CommandHandler("end_quiz", end_quiz)],
    )
    dp.add_handler(conversation_handler)
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('login', login)],
    states={
        'USERNAME': [MessageHandler(Filters.text, username)],
        'PASSWORD': [MessageHandler(Filters.text, password)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    
    conversation = ConversationHandler(
    entry_points=[CommandHandler('feedback', feedback)],
    states={
        'NAME': [MessageHandler(Filters.text, name)],
        'RATING': [MessageHandler(Filters.text, rating)],
        'IMPROVEMENT': [MessageHandler(Filters.text, improvement)],
    },
    fallbacks=[CommandHandler('cancel1',cancel1)]
    )
    dp.add_handler(conversation)
    
    dp.add_handler(MessageHandler(Filters.text, reply))
    dp.add_handler(CommandHandler("translate", lang_translator))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

