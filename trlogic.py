# -----------------------------------------------------------------------------------------------
# Name: Basil Noor
#       This file contains code for the backend of the TeamRandomizer Bot.
#       Contains various functions for the logic of the weighted randomization/creation of teams
# -----------------------------------------------------------------------------------------------

import random

# accepted ranks
accepted_ranks = ["b1", "b2", "b3", "s1", "s2", "s3", "g1", "g2", "g3", "p1", "p2", "p3", "d1", "d2", "d3", "pro"]

# Used for /tr start to give value to rank
def find_rank(player_rank):
    ranks = {
        "b1": 1, "b2": 1, "b3": 2,
        "s1": 2, "s2": 3, "s3": 3,
        "g1": 4, "g2": 4, "g3": 5,
        "p1": 6, "p2": 7, "p3": 8,
        "d1": 10, "d2": 10, "d3": 12,
        "pro": 14
    }
    player_rank = ranks[player_rank]
    return player_rank

# Used for /tr start to generate 2 random teams
def randomize(list_of_players):

    # track which team gets next player
    team_counter = 1 
    # separate players into groups based on rank
    team_1 = [] # 9+
    team_2 = [] # 6-8
    team_3 = [] # 3-5
    team_4 = [] # 1-2
    for player in list_of_players:
        if player[1] >= 9:
            team_1.append(player)
        elif 6 <= player[1] <= 8:
            team_2.append(player)
        elif 3 <= player[1] <= 5:
            team_3.append(player)
        else:
            team_4.append(player)
    
    # randomize all teams
    random.shuffle(team_1)
    random.shuffle(team_2)
    random.shuffle(team_3)
    random.shuffle(team_4)

    # add players into 2 teams alternating teams starting from team_1
    final_team_1 = []
    final_team_2 = []
    team_1_power = 0
    team_2_power = 0

    for player in team_1:
        if team_counter == 1:
            final_team_1.append(player[0])
            team_1_power += player[1]
            team_counter = 2
        elif team_counter == 2:
            final_team_2.append(player[0])
            team_2_power += player[1]
            team_counter = 1
    for player in team_2:
        if team_counter == 1:
            final_team_1.append(player[0])
            team_1_power += player[1]
            team_counter = 2
        elif team_counter == 2:
            final_team_2.append(player[0])
            team_2_power += player[1]
            team_counter = 1
    for player in team_3:
        if team_counter == 1:
            final_team_1.append(player[0])
            team_1_power += player[1]
            team_counter = 2
        elif team_counter == 2:
            final_team_2.append(player[0])
            team_2_power += player[1]
            team_counter = 1
    for player in team_4:
        if team_counter == 1:
            final_team_1.append(player[0])
            team_1_power += player[1]
            team_counter = 2
        elif team_counter == 2:
            final_team_2.append(player[0])
            team_2_power += player[1]
            team_counter = 1

    return (final_team_1, final_team_2, team_1_power, team_2_power)

# Used for /tr players (formatting)
def list_players(list_of_players):
    players_string = ">>> "
    for player in list_of_players:
        rank_name = ""
        if player[1] == "pro":
            rank_name = "Pro"
        elif player[1][0] == "b":
            rank_name = "Bronze " + player[1][1]
        elif player[1][0] == "s":
            rank_name = "Silver " + player[1][1]
        elif player[1][0] == "g":
            rank_name = "Gold " + player[1][1]
        elif player[1][0] == "p":
             rank_name = "Platinum " + player[1][1]
        elif player[1][0] == "d":
            rank_name = "Diamond " + player[1][1]
        players_string += f"```{player[0]}: {rank_name}``` "
    return players_string

# used for /tr start
def find_title():
    list_of_final_titles = ["Goodluck Everyone", "My money's on Team 1", 
    "My money's on team 2", "Teams look pretty even", "Yikes", "I wouldn't want to be on Team 1", 
    "Lookin' good Team 2", "Lookin' good Team 1"]
    random.shuffle(list_of_final_titles)
    return list_of_final_titles[0]

# used for /tr pick_map
def pick_random_map(list_of_maps):
    random.shuffle(list_of_maps)
    found_map = list_of_maps[0][0]
    return found_map


def main():
    pass

if __name__ == "__main__":
    main()