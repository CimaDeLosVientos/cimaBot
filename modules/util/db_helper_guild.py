import sqlite3


class DBHelperGuild:
    """Database manager
    
    All possible request that may be doing to database are a function of this object.
    """
    def __init__(self, path):             
        self.db = sqlite3.connect(path)
        self.setup()


    def setup(self):
        """Setup finances database
        
        Setup finances database and prepares it for to using.
        """
        # Mirar si le puedo pasar el script de creación, se puede, pero dice que no más de una orden
        # Quizá si ponemos commits deje, si no habría que sacarlo en modo texto en un .py
        self.db.executescript(open("./modules/util/guild.sql", 'r').read()) # Hay que mirar si esta ruta está bien puesta
        self.db.commit()

    def add_adventurer(self, arguments):
        """Register a adventurer in database
        
        Throught web app and command_registration function  is builded a arguments map that is given to this function to insert the new rows in database.
        This function builds a runs the queries for the new rows.
        
        Arguments:
            arguments {Dictionary} -- Dictionary with all values for insert the new rows
        """
        # Add place
        id_from = [x for x in self.db.execute("SELECT id FROM Place WHERE name= (?)", (arguments["from"],))]
        if not id_from:
            query = "INSERT INTO Place (name) VALUES (?)"
            self.db.execute(query, (arguments["from"],))
            id_from = [x for x in self.db.execute("SELECT id FROM Place WHERE name= (?)", (arguments["from"],))]
        id_from = id_from[0][0] # This is rare but work

        # Add Tag
        for tag in arguments["tags"]:
            id_tag = [x for x in self.db.execute("SELECT id FROM Tag WHERE name= (?)", (tag,))]
            if not id_tag:
                query = "INSERT INTO Tag (name) VALUES (?)"
                self.db.execute(query, (tag,))
                id_tag = [x for x in self.db.execute("SELECT id FROM Tag WHERE name= (?)", (tag,))]
            id_tag = id_tag[0][0] # This is rare but i work (or not)
        # No lo uso aún

        # Add adventure
        query = "INSERT INTO Adventurer (name, complete_name, birth_date_day, birth_date_month, birth_date_year, registrer_date_day, registrer_date_month, registrer_date_year, sex, race, id_from, formation, especialiation, work_experience, testament, room, rank, on_service) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        args = (arguments["name"], arguments["complete_name"], arguments["birth_date_day"], arguments["birth_date_month"], arguments["birth_date_year"], arguments["registrer_date_day"], arguments["registrer_date_month"], arguments["registrer_date_year"], arguments["sex"], arguments["race"], id_from, arguments["formation"], arguments["especialiation"], arguments["work_experience"], arguments["testament"], 0,0,1)
        print(args)
        self.db.execute(query, args)

        id_adventurer = [x for x in self.db.execute("SELECT id FROM Adventurer WHERE name= (?)", (arguments["name"],))]
        id_adventurer = id_adventurer[0][0]

        # Add character
        query = "INSERT INTO Character (name, id_adventurer, player, experience_points, level, money) VALUES (?, ?, ?, ?, ?, ?)"
        args = (arguments["name"], id_adventurer, arguments["player"], arguments["experience_points"], get_level(arguments["experience_points"]), arguments["money"])
        self.db.execute(query, args)

        self.db.commit() 


def get_level(exp_points):
    return 0 # Fusilar el excel