# Telegram Quiz BOT
## You in the Potterverse
## @zahovaibot

### Description
A quiz to determine which of seven Harry Potter characters you would be, based on questions and options provided.

However, functionality is not limited to the Harry Potter theme, but can be extended to include other types of quizzes by simply including another question-answer file.

Written in Python with the use of aiogram, aiosqlite, and asyncio libraries.

The results from quiz completion are stored inside the associated database file as well as the current quiz progression.

### Commands
* /start — prompts the beginning of the programm cycle with a refreshed database table
* /quiz — prompts the beginning of the quiz
* /results — prompts the bot to show the saved results of any completed quizzes (note that if the current user completes the quiz multiple times all of the different results would be shown, without duplicates)

### Buttons
* Begin the quiz — corresponds to the /quiz inline command.
* See results — corresponds to the /results inline command.

