import sqlite3
import os
from typing import Optional

DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(DIR, "usr_dat.db")

class DatabaseManager:
     _db: Optional[sqlite3.Connection] = None
     _cr: Optional[sqlite3.Cursor] = None
     __initialized: bool = False

     @classmethod
     def init_database(cls):
          if cls.__initialized:
               raise HasInitialized("The database had already initialized")
          
          cls._cr.execute("""
               CREATE TABLE IF NOT EXISTS watched_movies (
                    name VARCHAR(255) PRIMARY KEY
               )
          """)
          cls._cr.execute("""
               CREATE TABLE IF NOT EXISTS watched_episodes (
                    owner_movie VARCHAR(255) NOT NULL,
                    episode_num INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY(owner_movie) REFERENCES watched_movies(name)
               )
          """)
          cls._db.commit()

     @classmethod
     def watched_epi(cls, mv_name: str, epi_num: int):

          if not cls.__initialized:
               raise HasNotInitialized("The database did not initialize before")
          
          cls._cr.execute("INSERT OR REPLACE INTO watched_movies VALUES (?)", (mv_name,))
          cls._cr.execute("INSERT OR REPLACE INTO watched_episodes VALUES (?, ?)", (mv_name, epi_num))
          cls._db.commit()

     @classmethod
     def unwatched_epi(cls, mv_name: str, epi_num: int):

          if not cls.__initialized:
               raise HasNotInitialized("The database did not initialize before")

          cls._cr.execute("DELETE FROM watched_episodes WHERE owner_movie = ? AND episode_num = ?", (mv_name, epi_num))
          cls._cr.execute("SELECT * FROM watched_episodes INNER JOIN watched_movies ON watched_episodes.owner_movie = watched_movies.name")
          if not cls._cr.fetchall():
               cls._cr.execute("DELETE FROM watched_movies WHERE name = ?", (mv_name,))
          cls._db.commit()

     @classmethod
     def close_database(cls):
          if not cls.__initialized:
               raise HasNotInitialized("The database did not initialize before")
          cls._db.close()
          cls._db, cls._cr = None
          cls.__initialized = False


class DatabaseError(Exception): ...
class HasNotInitialized(DatabaseError): ...
class HasInitialized(DatabaseError): ...