import random
import sys

data_file_name = "Player_Data_1985.csv"

#checks whether two strings are equal, with case and spaces removed
def strings_mostly_equal(str1, str2):
  return str1.lower().replace(" ","")==str2.lower().replace(" ","")

class Player:
  def __init__(self, name="No Name", plate_appearances=1, homeruns=0, triples=0, doubles=0, singles=0, walks=0):
    #check that all numerical arguments are nonnegative, and plate appearances !=0
    assert (plate_appearances>0 and homeruns>=0 and triples>=0 and doubles>=0 and singles >=0 and walks>=0), "Arguments to Player are invalid"
    self.name = name
    #calculate player probability data
    self.homer = homeruns/plate_appearances
    #the value for triple includes homeruns because of how the random roll in at_bat() works.
    #if the roll in at_bat() is less than homer, home run. If the roll is in [homer, triple], triple.
    self.triple = (homeruns+triples)/plate_appearances
    self.double = (homeruns+triples+doubles)/plate_appearances
    self.single = (homeruns+triples+doubles+singles)/plate_appearances
    self.walk = (homeruns+triples+doubles+singles+walks)/plate_appearances
    #check that probability of walking does not exceed 1
    assert self.walk<=1, "Probability must not exceed 1"
  
  def __str__(self):
    return "Player name is: "+self.name+"\n HR: "+str(self.homer) + "\n 3B: "+str(self.triple)+"\n 2B: "+str(self.double)+"\n 1B: "+str(self.single) + "\n BB: "+str(self.walk)
  
  def at_bat(self):
    roll = random.random()
    if roll<self.homer:
      return "home run"
    elif roll<self.triple:
      return "triple"
    elif roll<self.double:
      return "double"
    elif roll<self.single:
      return "single"
    elif roll<self.walk:
      return "walk"
    else:
      return "out"

def create_player(target_player_name):
  data_file = open(data_file_name)
  for player in data_file:
    player_parsed = player.split(",")
    #if the player name matches, return a Player object
    if strings_mostly_equal(target_player_name,player_parsed[1]):
      name = player_parsed[1]
      plate_appearances = int(player_parsed[5])
      singles = int(player_parsed[7])
      doubles = int(player_parsed[8])
      triples = int(player_parsed[9])
      homeruns = int(player_parsed[10])
      walks = int(player_parsed[13]) + int(player_parsed[16]) #count a hit by pitch as a walk, since they do the same thing
      player = Player(name, plate_appearances, homeruns, triples, doubles, singles, walks)
      data_file.close()
      return player
  data_file.close()
  return None


def create_team(file_name):
  team = []
  with open(file_name, 'r') as file:
    for line in file:
      player = create_player(line.strip())
      assert player is not None, f"Couldn't create player {line}"
      team.append(player)
  return team

#used for debugging
def print_team(team):
  for player in team:
    print(player)

# Game simulation code taken from dice baseball draft game
#But refactored into a function with teams as an argument

#Simulate one baseball game
def sim_game(teams): #teams[0] is away, teams[1] is home
  #Game state variables to keep track of
  game_over = False
  score = [0,0] #away, home
  inning = 1
  team_batting = 0 # 0 represents away. 1 represents home
  place_in_lineup = [0,0] #away, home. 
  outs = 0
  base_runners = [0,0,0] #first, second, third. 0 represents no runner. 1 represents a runner

  while (not game_over):
    #determine who is batting and perform an at bat
    batter = teams[team_batting][place_in_lineup[team_batting]]
    outcome = batter.at_bat()
    place_in_lineup[team_batting]+=1
    place_in_lineup[team_batting]%=9
    if outcome == "out":
      outs+=1
    if outcome == "home run":
      score[team_batting]=score[team_batting]+base_runners[2]+base_runners[1]+base_runners[0]+1
      base_runners = [0,0,0]
    if outcome == "triple":
      score[team_batting]=score[team_batting]+base_runners[2]+base_runners[1]+base_runners[0]
      base_runners = [0,0,1]
    if outcome == "double":
      score[team_batting]=score[team_batting]+base_runners[2]+base_runners[1]
      base_runners[2]=base_runners[0]
      base_runners[1]=1
      base_runners[0]=0
    if outcome == "single":
      score[team_batting]=score[team_batting]+base_runners[2]
      base_runners[2]=base_runners[1]
      base_runners[1]=base_runners[0]
      base_runners[0]=1
    if outcome == "walk":
      #add 1 to score if the bases are loaded
      if base_runners==[1,1,1]:
        score[team_batting]+=1
      #If there are runners on first and second before the walk, there will be a runner on third after the walk
      #Otherwise, third will be the same as it was before the walk
      if base_runners[0] and base_runners[1]:
        base_runners[2]=1
      if base_runners[0]:
        base_runners[1]=1
      base_runners[0]=1
      
    if outs==3:
      base_runners = [0,0,0]
      inning += team_batting #if the home team is batting, inning_number is incremented by 1
      #update which team is batting
      team_batting += 1
      team_batting %= 2
      outs = 0
      #check if game is over
      if score[1]>score[0] and inning>=9 and team_batting==1:
        winner = "home"
        game_over = True
      if score[0]>score[1] and inning>=10 and team_batting==0:
        winner = "away"
        game_over = True
      if inning>100:
        print("The game went 100 innings. Something has gone wrong. Exiting.")
        sys.exit()
  return winner

#create teams
liam_team = create_team("liam.txt")
dad_team = create_team("dad.txt")
mom_team = create_team("mom.txt")
audrey_team = create_team("audrey.txt")
standings = {"Liam":0, "Mom": 0, "Audrey":0, "Dad":0}

#Sim 162 games: 54 round robins
for _ in range(54):
  result = sim_game([liam_team, mom_team])
  standings["Liam"] += (result=="away")
  standings["Mom"] += (result=="home")
  result = sim_game([liam_team, audrey_team])
  standings["Liam"] += (result=="away")
  standings["Audrey"] += (result=="home")
  result = sim_game([liam_team, dad_team])
  standings["Liam"] += (result=="away")
  standings["Dad"] += (result=="home")
  result = sim_game([mom_team, audrey_team])
  standings["Mom"] += (result=="away")
  standings["Audrey"] += (result=="home")
  result = sim_game([mom_team, dad_team])
  standings["Mom"] += (result=="away")
  standings["Dad"] += (result=="home")
  result = sim_game([audrey_team, dad_team])
  standings["Audrey"] += (result=="away")
  standings["Dad"] += (result=="home")

#display results
sorted_standings = sorted(standings.items(), key= lambda item: item[1], reverse=True)
print("Final Standings:")
for entry in sorted_standings:
  print(f"{entry[0]}\t{entry[1]}")