import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
from adjustText import adjust_text
import numpy as np
from scipy import stats


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
	if len(rows) == 0:
		return None
	print("team:             ", team)
	# print("season:           ", season)
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
	# print("games played:     ", games_count)
	# print("wins:             ", win_count)
	# print("losses (not wins):", games_count - win_count)
	# print("total margin:     ", cume_margin)
	# print("margin per game:  ", round(cume_margin/games_count, 2))
	# print("margin per win:   ", round(cume_margin/win_count, 2))
	return cume_margin/games_count  # margin per game


def get_playoff_position(conn, team, season):
	# todo add marker (5) for champion
	# todo handle 't' value in playoff field
	cur = conn.cursor()
	cur.execute("SELECT DISTINCT playoff from games where playoff IS NOT NULL and season = {0} and (team1 = '{1}' OR team2 = '{1}');".format(str(season), team))
	rows = cur.fetchall()
	if len(rows) == 0:
		return 0  # did not make playoffs
	if any([row[0] == 'f' for row in rows]):  # finals
		return 4  # made finals (round of 2)
	if any([row[0] == 'c' for row in rows]):  # conference
		return 3  # made conference (round of 4)
	if any([row[0] == 's' for row in rows]):  # semis
		return 2  # made semifinals (round of 8)
	if any([row[0] == 'q' for row in rows]):  # quarters
		return 1  # made quarterfinals (round of 16)
	return rows


def graph_team_data(teams, margins, positions, season):
	fig, ax = plt.subplots(figsize=(20,10))
	ax.scatter(margins, positions, alpha=0.4)
	# texts = [plt.text(margins[i], positions[i], teams[i], ha='center', va='center') for i in range(len(teams))]
	texts = [plt.text(margins[i], positions[i], teams[i]) for i in range(len(teams))]
	print('adjusting labels...')
	adjust_text(texts)


	plt.title("Average Point Win Margin vs. Playoff Postions ({0})".format(season))
	plt.ylabel("Playoff Value*")
	plt.xlabel("Avg. Win Margin")
	plt.show()


def graph_multi_year_data(teams_list, margins_list, positions_list, seasons_list):
	fig, ax = plt.subplots()
	# fig, ax = plt.subplots(figsize=(18,9))
	colors = ['b', 'g', 'r', 'c', 'm', 'y']
	for i in range(0, len(seasons_list)):
		label = seasons_list[i]
		ax.scatter(
			margins_list[i],
			positions_list[i],
			c=colors[i],
			alpha=0.6,
			label=seasons_list[i]
		)
		[plt.text(margins_list[i][j], positions_list[i][j], teams_list[i][j]) for j in range(len(teams_list[i]))]  # add labels

		gradient, intercept, r_value, p_value, std_err = stats.linregress(margins_list[i], positions_list[i])
		mn = np.min(margins_list[i])
		mx = np.max(margins_list[i])
		x1 = np.linspace(mn, mx, 500)
		y1 = gradient * x1 + intercept
		plt.plot(x1, y1, colors[i])


	plt.legend(loc='upper left')
	plt.title("Average Point Win Margin vs. Playoff Postions ({0}-{1})".format(min(seasons_list), max(seasons_list)))
	plt.ylabel("Playoff Value*")
	plt.xlabel("Avg. Win Margin")
	plt.show()


def main():
	database = "C:\\Users\\werdn\\Documents\\NBA-math-IA\\nba-data.db"

	# create a database connection
	conn = create_connection(database)
	season_min = 2017
	season_max = 2018
	teams_list = []
	margins_list = []
	playoff_positions_list = []
	seasons_list = []
	with conn:
		for season in range(season_min, season_max + 1):
			teams_to_graph = []
			margins_to_graph = []
			playoff_postions = []
			print('in season ', season, '...')
			for team in teams:
				rows = get_team_games(conn, team, season)
				if rows is not None:
					margin = get_winning_margins(rows, team)
					teams_to_graph.append(team)
					margins_to_graph.append(margin)
					playoff_pos = get_playoff_position(conn, team, season)
					playoff_postions.append(playoff_pos)
					# print("playoff position: ", playoff_pos)
					# print("========================")
			teams_list.append(teams_to_graph)
			margins_list.append(margins_to_graph)
			playoff_positions_list.append(playoff_postions)
			seasons_list.append(season)
	graph_multi_year_data(teams_list, margins_list, playoff_positions_list, seasons_list)


if __name__ == '__main__':
	main()
