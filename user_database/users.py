import sqlite3 as sql
from dataclasses import dataclass

from discord import Embed


@dataclass
class Database:
    con: sql.Connection = sql.connect('user_database/users.db')
    cur: sql.Cursor = con.cursor()

    def check_if_exist(self, user) -> bool:
        return self.cur.execute("SELECT * FROM Users WHERE UserID = ?",
                                (user, )).fetchone() is not None

    def write_user(self, user, extra_points=0):
        if self.check_if_exist(user):
            self.cur.execute(
                "UPDATE Users SET Points = Points + ? WHERE UserID = ?",
                (extra_points, user))
            self.con.commit()
        else:
            self.cur.execute(
                "INSERT INTO Users (UserID, Points, Wins, Losses) VALUES (?, ?, ?, ?)",
                (user, extra_points, 0, 0))
            self.con.commit()

    def get_points(self, user) -> int:
        return self.cur.execute("SELECT Points FROM Users WHERE UserID = ?",
                                (user, )).fetchone()[0]

    def add_win(self, user):
        self.cur.execute("UPDATE Users SET Wins = Wins + 1 WHERE UserID = ?",
                         (user, ))
        self.con.commit()

    def add_loss(self, user):
        self.cur.execute(
            "UPDATE Users SET Losses = Losses + 1 WHERE UserID = ?", (user, ))
        self.con.commit()

    def stats_embed(self, user) -> Embed:
        stats = self.cur.execute(
            "SELECT Points, Wins, Losses FROM Users WHERE UserID = ?",
            (user.id, )).fetchone()

        template = Embed(title=f"Stats of {user}")
        template.add_field(name="Points", value=str(stats[0]))
        template.add_field(name="Wins", value=str(stats[1]))
        template.add_field(name="Losses", value=str(stats[2]))
        try:
            template.add_field(
                name="Winrate",
                value=f"{stats[1] / (stats[1] + stats[2]) * 100:.2f}%")
        except ZeroDivisionError:
            template.add_field(name="Winrate", value="0.00%")

        return template
