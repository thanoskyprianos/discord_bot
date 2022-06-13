import sqlite3 as sql
from dataclasses import dataclass
from typing import Optional


@dataclass
class Database:
    con: sql.Connection = sql.connect('user_database/users.db')
    cur: sql.Cursor = con.cursor()

    def check_if_exist(self, user) -> bool:
        return self.cur.execute("SELECT * FROM Users WHERE UserID = ?",
                                (user, )).fetchone() is not None

    def write_user(self, user, extra_points: Optional[int] = 0):
        if self.check_if_exist(user):
            points = self.cur.execute(
                "SELECT Points FROM Users WHERE UserID = ?",
                (user, )).fetchone()[0]
            self.cur.execute("UPDATE Users SET Points = ? WHERE UserID = ?",
                             (points + extra_points, user))
            self.con.commit()
        else:
            self.cur.execute(
                "INSERT INTO Users (UserID, Points) VALUES (?, ?)",
                (user, extra_points))
            self.con.commit()

    def get_points(self, user) -> int:
        return self.cur.execute("SELECT Points FROM Users WHERE UserID = ?",
                                (user, )).fetchone()[0]
