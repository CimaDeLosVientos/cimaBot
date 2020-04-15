# coding=utf-8
####################################
##############CIMABOT###############
###ASOCIACIÓN CIMA DE LOS VIENTOS###
####### @Luis_gar # @Seind #########
####################################

import sqlite3


class DBHelper:

    def __init__(self, dbname="table.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    #Base de datos del banco
    def setup_finantial(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS cuentas (concept text,member text,day integer,month integer,year integer,quantity float)"
        #itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
        #ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        #self.conn.execute(itemidx)
        #self.conn.execute(ownidx)
        self.conn.commit()

    def add_transaction(self, concept, member, day, month, year, quantity):
        stmt = "INSERT INTO cuentas (concept, member, day, month, year, quantity) VALUES (?, ?, ?, ?, ?, ?)"
        args = (concept, member, day, month, year, quantity)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_transactions(self, member):
        stmt = "SELECT * FROM 'cuentas' WHERE member = ?"
        args = (member,)
        return [x for x in self.conn.execute(stmt, args)]

    def get_last(self):
        stmt = "SELECT * FROM 'cuentas' DESC LIMIT 15"
        return [x for x in self.conn.execute(stmt)]

    def del_last(self):
        stmt = "DELETE * FROM 'cuentas' DESC LIMIT 1"
        self.conn.execute(stmt)
        self.conn.commit()        

    def get_total(self):
        saldo = 0
        stmt = "SELECT quantity FROM 'cuentas'"
        for x in self.conn.execute(stmt):
            saldo = saldo + x[0]
        return saldo

    #Base de datos de aventureros
    def setup_adventurers(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS pjs (jugador text, personaje text, nivel integer, rango text, experiencia integer, dinero float, PRIMARY KEY(personaje))"
        self.conn.execute(tblstmt)
        self.conn.commit()

    def add_adventurer(self, player, adventurer, level, rank, xp, money):
        stmt = "INSERT INTO pjs (jugador, personaje, nivel, rango, experiencia, dinero) VALUES (?, ?, ?, ?, ?, ?)"
        args = (player, adventurer, level, rank, xp, money)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def level_up(self, adventurer, level):
        stmt = "UPDATE pjs SET nivel = (?) WHERE personaje = (?)"
        args = (level, adventurer)
        self.conn.execute(stmt, args)
        self.conn.commit() 

    def get_xp(self, adventurer):
        stmt = "SELECT experiencia FROM 'pjs' WHERE personaje = ?"
        args = (adventurer,)
        return [x for x in self.conn.execute(stmt, args)]   

    def update_xp(self, adventurer, xp):
        stmt = "UPDATE pjs SET experiencia = (?) WHERE personaje = (?)"
        args = (xp, adventurer)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_money(self, adventurer):
        stmt = "SELECT dinero FROM 'pjs' WHERE personaje = ?"
        args = (adventurer,)
        return [x for x in self.conn.execute(stmt, args)] 

    def update_money(self, adventurer, wage):
        stmt = "UPDATE pjs SET dinero = (?) WHERE personaje = (?)"
        args = (wage, adventurer)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def rank_up(self, adventurer, rank):
        stmt = "UPDATE pjs SET rango = (?) WHERE personaje = (?)"
        args = (rank, adventurer)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_characters(self, player):
        stmt = "SELECT * FROM 'pjs' WHERE jugador = ?"
        args = (player,)
        return [x for x in self.conn.execute(stmt, args)]
    
    def get_ranks(self, rank):
        stmt = "SELECT * FROM 'pjs' WHERE rango = ?"
        args = (rank,)
        return [x for x in self.conn.execute(stmt, args)] 

    def get_pj(self, name):
        stmt = "SELECT * FROM 'pjs' WHERE personaje = ?"
        args = (name,)
        return [x for x in self.conn.execute(stmt, args)]         

    #Base de datos de misiones realizadas
    def setup_quests(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS quests (identificador text, diaSemana text, dia integer, mes integer, temporada integer, personajes text, resumen text, PRIMARY KEY(identificador))"
        self.conn.execute(tblstmt)
        self.conn.commit()

    def add_quest(self, ID, weekDay, day, month, year, characters, summary):
        stmt = "INSERT INTO quests (identificador, diaSemana, dia, mes, temporada, personajes, resumen) VALUES (?, ?, ?, ?, ?, ?, ?)"
        args = (ID, weekDay, day, month, year, characters, summary)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_quest(self, ID):
        stmt = "SELECT * FROM 'quests' WHERE identificador = ?"
        args = (ID,)
        return [x for x in self.conn.execute(stmt, args)]

    def get_lastQuests(self):
        stmt = "SELECT * FROM 'quests' DESC LIMIT 10"
        return [x for x in self.conn.execute(stmt)]

    #Base de datos de triggers
    def setup_triggers(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS triggers (trigger, tipo, contenido, PRIMARY KEY(trigger))"
        self.conn.execute(tblstmt)
        self.conn.commit()

    def add_trigger(self, newTrigger, contentType, content):
        stmt = "INSERT INTO triggers (trigger, tipo, contenido) VALUES (?, ?, ?)"
        args = (newTrigger, contentType, content)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_trigger(self, trigger):
        stmt = "SELECT * FROM 'triggers' WHERE trigger = ?"
        args = (trigger,)
        return [x for x in self.conn.execute(stmt, args)]

    def get_triggers(self):
        stmt = "SELECT * FROM 'triggers'"
        return [x for x in self.conn.execute(stmt)]

    #Base de datos del change log
    def setup_changes(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS changes (usuario, contenido)"
        self.conn.execute(tblstmt)
        self.conn.commit()

    def add_change(self, user, content):
        stmt = "INSERT INTO changes (usuario, contenido) VALUES (?, ?)"
        args = (user, content)
        self.conn.execute(stmt, args)
        self.conn.commit()

    #Base de datos de inscripciones a torneos
    def setup_enrollment(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS enrollments (torneo, personaje, arma)"
        self.conn.execute(tblstmt)
        self.conn.commit()

    def add_enrollment(self, turney, character, weapon):
        print(turney, character, weapon)
        stmt = "INSERT INTO enrollments (torneo, personaje, arma) VALUES (?, ?, ?)"
        args = (turney, character, weapon)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_enrollment(self, turney):
        stmt = "SELECT * FROM 'enrollments' WHERE torneo = ?"
        args = (turney,)
        return [x for x in self.conn.execute(stmt, args)]

    def get_enrollments(self):
        stmt = "SELECT * FROM 'enrollments'"
        return [x for x in self.conn.execute(stmt)]
