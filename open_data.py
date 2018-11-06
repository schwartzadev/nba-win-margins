import sqlite3
from sqlite3 import Error

teams = [
	"ANA", "AND", "ATL", "BAL", "BLB", "BOS", "BRK", "BUF", "CAP", "CAR", "CHH", "CHI", "CHO", "CHP", "CHS", "CHZ", "CIN", "CLE", "CLR",
	"DAL", "DEN", "DET", "DLC", "DNA", "DNN", "DNR", "DTF", "FLO", "FTW", "GSW", "HOU", "HSM", "INA", "IND", "INJ", "INO", "KCK", "KCO",
	"KEN", "LAC", "LAL", "LAS", "MEM", "MIA", "MIL", "MIN", "MLH", "MMF", "MMP", "MMS", "MMT", "MNL", "MNM", "MNP", "NJA", "NJN", "NOB",
	"NOJ", "NOK", "NOP", "NYA", "NYK", "NYN", "OAK", "OKC", "ORL", "PHI", "PHO", "PHW", "PIT", "POR", "PRO", "PTC", "PTP", "ROC", "SAA",
	"SAC", "SAS", "SDA", "SDC", "SDR", "SDS", "SEA", "SFW", "SHE", "SSL", "STB", "STL", "SYR", "TEX", "TOR", "TRH", "TRI", "UTA", "UTS",
	"VAN", "VIR", "WAS", "WAT", "WSA", "WSB", "WSC"
]

def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)

	return None


def get_team_games(conn, team, season):
	cur = conn.cursor()
	cur.execute("SELECT team1, team2, score1, score2 from games where playoff IS NULL and season = {0} and (team1 = '{1}' OR team2 = '{1}');".format(str(season), team))
	rows = cur.fetchall()
	# for row in rows:
		# print(row)
	print("team:             ", team)
	print("season:           ", season)
	return rows


def get_winning_margins(rows, team):
	games_count = len(rows)
	win_count = 0
	cume_margin = 0
	for row in rows:
		team1 = row[0]
		team2 = row[1]
		score1 = int(row[2])
		score2 = int(row[3])
		if score2 > score1:
			winner = team2
			# print("    {} with {} points".format(team2, score2))
		elif score1 > score2:
			winner = team1
			# print("    {} with {} points".format(team1, score1))
		else:
			print("TIED!!!")

		if winner == team:
			# if the provided team won the game...
			win_count += 1
			margin = abs(score1 - score2)
			cume_margin += margin
	print("games played:     ", games_count)
	print("wins:             ", win_count)
	print("losses (not wins):", games_count - win_count)
	print("total margin:     ", cume_margin)
	print("margin per game:  ", round(cume_margin/games_count, 2))
	print("margin per win:   ", round(cume_margin/win_count, 2))

		# print("[{0} vs. {1}] winner: {2} (by {3} points)".format(row[0], row[1], row[0+winner], margin))


def main():
	database = "C:\\Users\\werdn\\Documents\\NBA-math-IA\\nba-data.db"

	# create a database connection
	conn = create_connection(database)
	with conn:
		team = "LAL"
		rows = get_team_games(conn, team, 2017)
		get_winning_margins(rows, team)


if __name__ == '__main__':
	main()