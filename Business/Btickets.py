import sqlite3 as sql
import json


def flight_status_search():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = f""" SELECT * FROM tickets LIMIT 5"""

        cursor.execute(query)

        data = cursor.fetchall()

        albums = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                if key == "model":
                    temp[key] = json.loads(row[key])["en"]
                else:
                    temp[key] = row[key]
            albums.append(temp)

        return albums

def check_ticket_existence(ticket_no, ID):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = f""" SELECT * FROM tickets WHERE ticket_no = '{ticket_no}' AND passenger_id = '{ID}'"""

        cursor.execute(query)

        data = cursor.fetchall()

        albums = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                if key == "model":
                    temp[key] = json.loads(row[key])["en"]
                else:
                    temp[key] = row[key]
            albums.append(temp)

        return len(albums) == 1
    
def check_ticket_existence_without_ID(ticket_no):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = f""" SELECT * FROM tickets WHERE ticket_no = '{ticket_no}'"""

        cursor.execute(query)

        data = cursor.fetchall()

        albums = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                if key == "model":
                    temp[key] = json.loads(row[key])["en"]
                else:
                    temp[key] = row[key]
            albums.append(temp)

        return len(albums) != 0

def cancel_ticket(ticket_no):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")


        cursor.execute(""" BEGIN TRANSACTION """)

        try:
            query = f""" DELETE FROM ticket_flights WHERE ticket_no = '{ticket_no}' """
            cursor.execute(query)
        except:
            cursor.execute(""" ROLLBACK """)
            return False
        
        try:
            query = f""" DELETE FROM tickets WHERE ticket_no = '{ticket_no}' """
            cursor.execute(query)
            cursor.execute(""" COMMIT """)
            return True
        except:
            cursor.execute(""" ROLLBACK """)
            return False