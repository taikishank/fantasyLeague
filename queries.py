import os
import sqlite3

class Queries:
    def getRoster(user):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = "SELECT * FROM Players WHERE FantasyUser LIKE ?"
        search_string = f"%{user}"
        cursor.execute(query, (search_string,))
        rows = cursor.fetchall()
        return rows
        
    def displayLeaguePlayers(league):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = "SELECT * FROM Players WHERE League LIKE ?"
        search_string = f"%{league}%"
        cursor.execute(query, (search_string,))
        rows = cursor.fetchall()
        return rows
    
    def sortBy(league, stat):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if (league != "None"):
            query = "SELECT * FROM Players WHERE League LIKE ? ORDER BY {} DESC;".format(stat)
            search_string = f"%{league}%"
            cursor.execute(query, search_string)
        else:
            query = "SELECT * FROM Players ORDER BY {stat} DESC;"
            cursor.execute(query)
        rows = cursor.fetchall()
        return rows
            
            
                