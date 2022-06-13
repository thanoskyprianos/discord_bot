from discord import Embed
from discord.ext import commands

from queston_maker import TrueFalseQuiz
from quizApi import QuizData

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged in!')


#not useful at the moment
# @bot.event
# async def on_message(message):
#     await bot.process_commands(message)
#     print(f'Message by {message.author} : {message.content}')


@bot.command()
async def ping(ctx):
    await ctx.send('pong!')


@bot.command()
async def clear(ctx, number=''):
    if not number or not number.isdigit() and number != 'all':
        await ctx.send('Please specify number of messages or "all".',
                       delete_after=2)
        return

    if number.lower() == 'all':
        await ctx.send(f'Clearing all messages in channel {ctx.channel}...',
                       delete_after=2)
        await ctx.channel.purge()
        return

    await ctx.send(
        f'Clearing {number} message(s) in channnel {ctx.channel}...',
        delete_after=2)
    await ctx.channel.purge(limit=int(number) + 2)


@bot.command()
async def quiz(ctx):

    quiz = QuizData()
    if quiz.get_response() == 0:  #check if api works

        question = TrueFalseQuiz()
        msg = await ctx.send(embed=question.question_template)
        await msg.add_reaction(['✅', '❌'])
        await msg.add_reaction('❌')

        def check(reaction, user):
            return user.id == ctx.author.id\
                and reaction.message == msg\
                and reaction.message.channel.id == ctx.channel.id\
                and str(reaction.emoji) in ['✅', '❌']

        reaction, _ = await bot.wait_for('reaction_add', check=check)

        if str(reaction.emoji) == '✅' and question.correct_answer == 'True'\
            or str(reaction.emoji) == '❌' and question.correct_answer == 'False':
            await msg.edit(embed=question.correct)
            return
        await msg.edit(embed=question.incorrect)
        return

    await ctx.send('API not currently working.')


bot.run(
    'OTg1MjE4ODI1OTIwMzI3NzEw.GFyfhP.I19NcCSL1UH4rPPXmTiP4unzKfsM7NQPEmFHBI')
