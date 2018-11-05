import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def get_winning_margins(conn, season):
    cur = conn.cursor()
    cur.execute("SELECT team1, team2, score1, score2 from games where season = "+str(season)+";")
    rows = cur.fetchall()
 
    for row in rows:
        score1 = row[2]
        score2 = row[3]
        if score1 > score2:
            winner = 0
        if score2 > score1:
            winner = 1

        margin = abs( int(row[2]) - int(row[3]) )

        print("winner: {0} (by {1} points)\t\t\t{2}".format(row[0+winner], margin, row))


def main():
    database = "C:\\Users\\werdn\\Documents\\NBA-math-IA\\nba-data.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        get_winning_margins(conn, 2018)
 
 
if __name__ == '__main__':
    main()