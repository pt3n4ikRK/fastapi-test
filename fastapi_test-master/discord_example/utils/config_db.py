from discord_example.database.core import Database
from discord_example.utils.verifySystem import VerifySystem

db = Database()
verify = VerifySystem(db=db)