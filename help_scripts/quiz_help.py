from dataclasses import dataclass

from discord import Embed


@dataclass
class QuizHelp:

    _help: str = '''
    
    !quiz help - shows this help
    !quiz [category] - starts a quiz with the specified category
    !quiz - starts a quiz with a random category
    '''

    _categories: str = '''
    General Knowledge (general)
    Entertainment: Books (books)
    Entertainment: Film (film)
    Entertainment: Music (music)
    Entertainment: Musicals & Theatres (mnt)
    Entertainment: Television (tv)
    Entertainment: Video Games (video)
    Entertainment: Board Games (board)
    Science & Nature (science)
    Science: Computers (pc)
    Science: Mathematics (math)
    Mythology (mythology)
    Sports (sports)
    Geography (geography)
    History (history)
    Politics (politics)
    Art (art)
    Celebrities (celeb)
    Animals (animals)
    Vehicles (cars)
    Entertainment: Comics (comics)
    Science: Gadgets (gadgets)
    Entertainment: Japanese Anime & Manga (jp)
    Entertainment: Cartoon & Animations (cartoon)
    '''

    def __post_init__(self):
        self._embed = Embed(title="Quiz Help", description=self._help)
        self._embed.add_field(name="Categories", value=self._categories)

    def get_embed(self) -> Embed:
        return self._embed
