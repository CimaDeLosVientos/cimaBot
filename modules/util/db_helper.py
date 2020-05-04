# coding=utf-8
####################################
##############CIMABOT###############
###ASOCIACIÓN CIMA DE LOS VIENTOS###
####### @Luis_gar # @Seind #########
####################################

import sqlite3


class DBHelper:
    """Database manager
    
    All possible request that may be doing to database are a function of this object.
    """
    def __init__(self, finances, adventurers, quests, triggers, log, registrations):
        self.finances      = sqlite3.connect(finances)          
        self.adventurers   = sqlite3.connect(adventurers)    
        self.quests        = sqlite3.connect(quests)              
        self.triggers      = sqlite3.connect(triggers)          
        self.logs          = sqlite3.connect(log)                    
        self.registrations = sqlite3.connect(registrations)
        self.setup()


    def setup(self):
        """Setup all databases
        
        The object DBHelper is a manager with several databases.
        This function setup all of them and prepares it for to using.
        """
        self.setup_finances()
        self.setup_adventurers()
        self.setup_quests()
        self.setup_triggers()
        self.setup_logs()
        self.setup_enrollment()
        print("Databases already!")

# Finances functions
    def setup_finances(self):
        """Setup finances database
        
        Setup finances database and prepares it for to using.
        """
        tblstmt = "CREATE TABLE IF NOT EXISTS cuentas (concept text,member text,day integer,month integer,year integer,quantity float)"
        self.finances.execute(tblstmt)
        self.finances.commit()

    def add_transaction(self, concept, member, day, month, year, quantity):
        stmt = "INSERT INTO cuentas (concept, member, day, month, year, quantity) VALUES (?, ?, ?, ?, ?, ?)"
        args = (concept, member, day, month, year, quantity)
        self.finances.execute(stmt, args)
        self.finances.commit()

    def get_transactions(self, member):
        stmt = "SELECT * FROM 'cuentas' WHERE member = ?"
        args = (member,)
        return [x for x in self.finances.execute(stmt, args)]

    def get_last(self):
        stmt = "SELECT * FROM 'cuentas' DESC LIMIT 15"
        return [x for x in self.finances.execute(stmt)]

    def del_last(self):
        stmt = "DELETE * FROM 'cuentas' DESC LIMIT 1"
        self.finances.execute(stmt)
        self.finances.commit()        

    def get_total(self):
        saldo = 0
        stmt = "SELECT quantity FROM 'cuentas'"
        for x in self.finances.execute(stmt):
            saldo = saldo + x[0]
        return saldo

# Adventurers database
    def setup_adventurers(self):
        """Setup adventurers database
        
        Setup adventurers database and prepares it for to using.
        """
        tblstmt = "CREATE TABLE IF NOT EXISTS pjs (jugador text, personaje text, nivel integer, rango text, experiencia integer, dinero float, PRIMARY KEY(personaje))"
        self.adventurers.execute(tblstmt)
        self.adventurers.commit()

    def add_adventurer(self, player, adventurer, level, rank, xp, money):
        stmt = "INSERT INTO pjs (jugador, personaje, nivel, rango, experiencia, dinero) VALUES (?, ?, ?, ?, ?, ?)"
        args = (player, adventurer, level, rank, xp, money)
        self.adventurers.execute(stmt, args)
        self.adventurers.commit()

    def level_up(self, adventurer, level):
        stmt = "UPDATE pjs SET nivel = (?) WHERE personaje = (?)"
        args = (level, adventurer)
        self.adventurers.execute(stmt, args)
        self.adventurers.commit() 

    def get_xp(self, adventurer):
        stmt = "SELECT experiencia FROM 'pjs' WHERE personaje = ?"
        args = (adventurer,)
        return [x for x in self.adventurers.execute(stmt, args)]   

    def update_xp(self, adventurer, xp):
        stmt = "UPDATE pjs SET experiencia = (?) WHERE personaje = (?)"
        args = (xp, adventurer)
        self.adventurers.execute(stmt, args)
        self.adventurers.commit()

    def get_money(self, adventurer):
        stmt = "SELECT dinero FROM 'pjs' WHERE personaje = ?"
        args = (adventurer,)
        return [x for x in self.adventurers.execute(stmt, args)] 

    def update_money(self, adventurer, wage):
        stmt = "UPDATE pjs SET dinero = (?) WHERE personaje = (?)"
        args = (wage, adventurer)
        self.adventurers.execute(stmt, args)
        self.adventurers.commit()

    def rank_up(self, adventurer, rank):
        stmt = "UPDATE pjs SET rango = (?) WHERE personaje = (?)"
        args = (rank, adventurer)
        self.adventurers.execute(stmt, args)
        self.adventurers.commit()

    def get_characters(self, player):
        stmt = "SELECT * FROM 'pjs' WHERE jugador = ?"
        args = (player,)
        return [x for x in self.adventurers.execute(stmt, args)]
    
    def get_ranks(self, rank):
        stmt = "SELECT * FROM 'pjs' WHERE rango = ?"
        args = (rank,)
        return [x for x in self.adventurers.execute(stmt, args)] 

    def get_pj(self, name):
        stmt = "SELECT * FROM 'pjs' WHERE personaje = ?"
        args = (name,)
        return [x for x in self.adventurers.execute(stmt, args)]         

# Quests Database
    def setup_quests(self):
        """Setup quests database
        
        Setup quests database and prepares it for to using.
        """
        tblstmt = "CREATE TABLE IF NOT EXISTS quests (identificador text, diaSemana text, dia integer, mes integer, temporada integer, personajes text, resumen text, PRIMARY KEY(identificador))"
        self.quests.execute(tblstmt)
        self.quests.commit()

    def add_quest(self, ID, weekDay, day, month, year, characters, summary):
        stmt = "INSERT INTO quests (identificador, diaSemana, dia, mes, temporada, personajes, resumen) VALUES (?, ?, ?, ?, ?, ?, ?)"
        args = (ID, weekDay, day, month, year, characters, summary)
        self.quests.execute(stmt, args)
        self.quests.commit()

    def get_quest(self, ID):
        stmt = "SELECT * FROM 'quests' WHERE identificador = ?"
        args = (ID,)
        return [x for x in self.quests.execute(stmt, args)]

    def get_lastQuests(self):
        stmt = "SELECT * FROM 'quests' DESC LIMIT 10"
        return [x for x in self.quests.execute(stmt)]

# Triggers database
    def setup_triggers(self):
        """Setup triggers database
        
        Setup triggers database and prepares it for to using.
        """
        tblstmt = "CREATE TABLE IF NOT EXISTS triggers (trigger, tipo, contenido, PRIMARY KEY(trigger))"
        self.triggers.execute(tblstmt)
        self.triggers.commit()

    def add_trigger(self, newTrigger, contentType, content):
        stmt = "INSERT INTO triggers (trigger, tipo, contenido) VALUES (?, ?, ?)"
        args = (newTrigger, contentType, content)
        self.triggers.execute(stmt, args)
        self.triggers.commit()

    def get_trigger(self, trigger):
        stmt = "SELECT * FROM 'triggers' WHERE trigger = ?"
        args = (trigger,)
        return [x for x in self.triggers.execute(stmt, args)]

    def get_triggers(self):
        stmt = "SELECT * FROM 'triggers'"
        return [x for x in self.triggers.execute(stmt)]

# Log Database
    def setup_logs(self):
        """Setup log database
        
        Setup log database and prepares it for to using.
        """
        tblstmt = "CREATE TABLE IF NOT EXISTS changes (usuario, contenido)"
        self.logs.execute(tblstmt)
        self.logs.commit()

    def add_change(self, user, content):
        stmt = "INSERT INTO changes (usuario, contenido) VALUES (?, ?)"
        args = (user, content)
        self.logs.execute(stmt, args)
        self.logs.commit()

# Registrations database
    def setup_enrollment(self):
        """Setup registrations database
        
        Setup registrations database and prepares it for to using.
        """
        tblstmt = "CREATE TABLE IF NOT EXISTS enrollments (torneo, personaje, arma)"
        self.registrations.execute(tblstmt)
        self.registrations.commit()

    def add_enrollment(self, turney, character, weapon):
        print(turney, character, weapon)
        stmt = "INSERT INTO enrollments (torneo, personaje, arma) VALUES (?, ?, ?)"
        args = (turney, character, weapon)
        self.registrations.execute(stmt, args)
        self.registrations.commit()

    def get_enrollment(self, turney):
        stmt = "SELECT * FROM 'enrollments' WHERE torneo = ?"
        args = (turney,)
        return [x for x in self.registrations.execute(stmt, args)]

    def get_enrollments(self):
        stmt = "SELECT * FROM 'enrollments'"
        return [x for x in self.registrations.execute(stmt)]
