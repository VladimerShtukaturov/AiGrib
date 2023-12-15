import telebot
from PIL import Image
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('model_2')
bot = telebot.TeleBot('6802555276:AAHxvAdhyk0riV7jdH6pXyhvDGVOWOIOswE')

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Привет! Отправь мне фотографию гриба, и я скажу, ядовитый он или нет.')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('image.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    image = Image.open('image.jpg')
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0  # Нормализация значений пикселей

    prediction = model.predict(np.expand_dims(image_array, axis=0))
    print(prediction[0])


    toxic_probability = prediction[0][1]

    if toxic_probability > 0.8:
        bot.reply_to(message, 'Этот гриб не является ядовитым.')
    else:
        bot.reply_to(message, 'Этот гриб является ядовитым.')

bot.polling(none_stop=True)