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

    def setup_adventurers(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS pjs (jugador text, personaje text, nivel integer, rango text, PRIMARY KEY(personaje))"
        self.conn.execute(tblstmt)
        self.conn.commit()

    def add_adventurer(self, player, adventurer, level, rank):
        stmt = "INSERT INTO pjs (jugador, personaje, nivel, rango) VALUES (?, ?, ?, ?)"
        args = (player, adventurer, level, rank)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def level_up(self, adventurer, level):
        stmt = "UPDATE pjs SET nivel = (?) WHERE personaje = (?)"
        args = (level, adventurer)
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




