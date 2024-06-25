import logging
import os
import ast
import Levenshtein
import telebot

TOKEN = '7160847949:AAE3gPKrHw7pJQPGN2IkggWYdKZvCgBsws4'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    """Отправляет приветственное сообщение при старте бота."""
    bot.reply_to(message, 'Привет! Отправь мне два Python файла, и я проверю их на плагиат.')

@bot.message_handler(commands=['compare'])
def compare_files(message):
    """Сравнивает два Python файла на плагиат."""
    if len(message.text.split()) < 3:
        bot.reply_to(message, 'Пожалуйста, отправь два файла для сравнения.')
        return

    file_path1 = message.text.split()[1]
    file_path2 = message.text.split()[2]

    if not (file_path1.endswith('.py') and file_path2.endswith('.py')):
        bot.reply_to(message, 'Пожалуйста, отправь два файла с расширением .py.')
        return

    if not (os.path.exists(file_path1) and os.path.exists(file_path2)):
        bot.reply_to(message, 'Пожалуйста, убедитесь, что оба файла существуют.')
        return

    try:
        similarity = calculate_plagiarism_score(file_path1, file_path2)
        bot.reply_to(message, f'Сходство между файлами составляет {similarity:.2f}%.')

        if similarity > 70:
            bot.reply_to(message, 'Слишком большое сходство! Возможен плагиат.')
        else:
            bot.reply_to(message, 'Сходство в пределах допустимых значений.')

    except SyntaxError:
        bot.reply_to(message, 'Пожалуйста, убедитесь, что оба файла содержат корректный код Python.')

def calculate_plagiarism_score(file1, file2):
    with open(file1, "r") as f1:
        code1 = f1.read()

    with open(file2, "r") as f2:
        code2 = f2.read()

    distance = Levenshtein.distance(code1, code2)
    similarity = (1 - (distance / max(len(code1), len(code2)))) * 100

    try:
        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)
    except SyntaxError:
        raise SyntaxError("Синтаксическая ошибка.")

    ast_str1 = ast.dump(tree1)
    ast_str2 = ast.dump(tree2)

    return similarity

@bot.message_handler(func=lambda message: True)
def echo(message):
    """Обрабатывает все остальные сообщения."""
    bot.reply_to(message, 'Неизвестная команда. Пожалуйста, воспользуйтесь командой /start для начала.')

if __name__ == '__main__':
    bot.polling()