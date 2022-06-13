from discord import Embed
from discord.ext import commands

from queston_maker import Quiz
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

        question = Quiz()
        msg = await ctx.send(embed=question.template_creation())

        for emoji in question.get_choices().keys():
            await msg.add_reaction(emoji)

        def check(reaction, user):
            return user.id == ctx.author.id\
                and reaction.message == msg\
                and reaction.message.channel.id == ctx.channel.id\
                and str(reaction.emoji) in question.get_choices().keys()

        reaction, _ = await bot.wait_for('reaction_add', check=check)

        if question.get_choices()[str(
                reaction.emoji)] == question.get_correct_answer():
            await msg.edit(embed=question.correct_embed())
            return
        await msg.edit(embed=question.incorrect_embed())
        return

    await ctx.send('API not currently working.')


bot.run(
    'OTg1MjE4ODI1OTIwMzI3NzEw.GFyfhP.I19NcCSL1UH4rPPXmTiP4unzKfsM7NQPEmFHBI')
