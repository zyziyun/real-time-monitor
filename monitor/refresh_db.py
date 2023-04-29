#!/usr/bin/env python3
import sqlite3
import os

def main():
    os.system("rm -rf monitor.db")
    # create db
    conn = sqlite3.connect('monitor.db')
    cursor = conn.cursor()
    # create table
    # Summary, Switches, Start_time, End_time, Packet_size
    sql_create = '''CREATE TABLE IF NOT EXISTS ping_data
            (ID INTEGER primary key AUTOINCREMENT,
                Summary TEXT,
                Switches TEXT,
                Start_time INTEGER,
                End_time REAL,
                Packet_size INTEGER);'''
    cursor.execute(sql_create)
    print("refresh db successfully")
    conn.commit()
    conn.close()
    

if __name__ == '__main__':
    main()