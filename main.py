from discord import Embed
from discord.ext import commands
from matplotlib.pyplot import title

from quiz_maker import QuizMaker

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

    quiz = QuizMaker()
    if quiz.get_response() == 0:  #check if api works

        correct = Embed(title='Correct!', description='Good job!')
        inccorect = Embed(title='Incorrect!', desription='Try again!')

        question = Embed(title='Question', description=quiz.get_question())
        question.add_field(name='Difficutly', value=quiz.get_difficulty())

        sent = await ctx.send(embed=question)

        def check(message):
            return message.author == ctx.author\
                and message.channel == ctx.channel \
                and message.reference is not None\
                and message.reference.message_id == sent.id

        reply = await bot.wait_for('message', check=check)
        if reply.content.capitalize() == quiz.get_answer():
            await sent.edit(embed=correct)
            return
        await sent.edit(embed=inccorect)
        return

    await ctx.send('API not currently working.')


bot.run(
    'OTg1MjE4ODI1OTIwMzI3NzEw.GFyfhP.I19NcCSL1UH4rPPXmTiP4unzKfsM7NQPEmFHBI')
