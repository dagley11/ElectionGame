import pandas as pd
import smtplib
import numpy as np
import random
import operator

def compute_rank(int_list):
	'''Determines rank of list with values, e.g. [9,5,8,2] --> [1,3,2,4]
	---BROKEN---
	'''
	pass



class Election:
	''' Election keeps a hidden record of states stance on issues, 
		handles research requests, and manages polling.
	'''
	def __init__(self, num_players = 4):
		'''Run when object is created''''
		self.num_players = 4
		self._set_state_stance()
		self._get_player_info()
		self._parse_emails()
		self._init_email()
		self._compute_score()
    
	def _init_email(self):
		'''Build email server and log into Gmail account'''
		self.server = smtplib.SMTP('smtp.gmail.com', 587)
		self.server.starttls()
		self.server.login("alexander.s.dagley@gmail.com", "filibuster")
	
	def _parse_emails(self):
		'''Convert emails stored in player_info dictionary to list of strings'''
	    pass
	
	def _compute_score(self):
		'''Score each player and update scores attribute (dictionary)'''
		for player in self.players:
			# Make a column in states_df (Pandas DataFrame) for each player's score, e.g. 1_score for player 1.
			# Run _compute_state_score method on each row for a given player to fill this column.
			self.states_df[player + '_score'] = self.states_df.apply(
				lambda x: self._compute_state_score(x, player)
				)
		for player in self.players:
			# Make a column in states_df (Pandas DataFrame) for each player's rank, e.g. 1_rank for player 1.
			# Run compute_rank runction on each row for a given player to fill this column.
			self.states_df[player + '_rank'] = self.states_df.apply(
				lambda x: compute_rank(x[player + '_score'] +  [x[other_player + '_score'] 
										for other_player in self.players 
										if other_player != player])[0]
						  )
		self.scores = {}
		for player in self.players:
			# Sum all Electoral Votes for a given player where the player is currently ranked 1 in the state.
			self.scores[player] = sum(self.states_df.Votes[self.states_df[player + '_rank'] == 1])

	def _get_player_info(self):
		'''Capture user input (player name, email, & stance on issues) and store in dictionary'''
		self.player_info = {}
		for player in range(1,self.num_players):
			print('PLAYER {}'.format(player))
			key = 'p{}'.format(player)
			self.player_info[key] = {}
			self.player_info[key]['Name'] = input("Enter name: ")
			self.player_info[key]['Email'] = input("Enter Email Address")
			self.player_info[key]['M'] = input("Enter Stance on Money: <-3,3>")
			self.player_info[key]['S'] = input("Enter Stance on Social: <-3,3>")
			self.player_info[key]['F'] = input("Enter Stance on Foreign Affairs: <-3,3>")
		self.players = self.player_info.keys()

	def _set_state_stance(self):
		'''Randomly initialize state's stance on issues.  This is run once at beginning of game.'''
		self.states_df = pd.read_csv('States.csv')
		for issue in ['M','S','FA']:
			self.states_df[issue] = np.random.randint(-3,4,size = 50)
	
	def _compute_state_score(self, df, player):
		'''Determine player score in a given state.'''
		# Your score is the sum of the absolute difference of your stance on issues and a state's stance on an issue.
		raw_score = sum([abs(df[issue] - self.player_info[player][issue]) for issue in ['M','S','FA']])
		# Adjust for slander tokens used against you in this state.
		raw_score += df[player + '_slander']
		# Adjust for ad tokens spent in this state.
		raw_score += -df[player + '_ad']
		# Your score can't be negative
		if raw_score < 0:
			raw_score = 0
		return raw_score
	
	def _send_polls(self):
		'''Send polling data via email to all players.  Requires adjusting state parameters based on campaigns and computing scores.'''
		mod_states_df = pd.read_csv('States.csv')
		self._adjust_state_params(mod_states_df)
		self._compute_score()
		self._author_email()

	def _author_email(self, msg = "YOUR MESSAGE!"):
		'''Send email.'''
		self.server.sendmail(self.emails, "THE EMAIL ADDRESS TO SEND TO", msg)

	def _adjust_state_params(self, mod_states_df):
		'''Adjust state parameters (stance on issues) to account for player campaigns, since last round of polling.'''
		for state in self.states_df.State:
			# sorted_players = list(sorted(self.scores, key=self.scores.get, reverse = True))
			for player in self.players:
				# If a player has campaigned in the state.
				if mod_states_df[player][self.states_df.state==state] == 1:
					# Find most aligned issue using Diff_Dict, a dictionary with isseus as key and alignment difference between player and state as value.
					Diff_Dict = {}
					for key in ['M','S','FA']:
						Diff_Dict[key] = abs(self.states_df[key][self.states_df.State==state] - self.player_info[player][key])
					Diff_Dict = {k:v for k, v in Diff_Dict.items() if v != 0}
					# If there are alignment differences greater than 0
					if len(Diff_Dict) > 0:
						# Find the minimum alignment difference
						min_val = np.min(Diff_Dict.values())
						# Find all issues that match the minimum alignment difference (usually just one but could be a tie between two or three issues)
						Matches = [k for k, v in Diff_Dict.items() if v == min_val]
						# Settle tie by randomly picking an issue to adjust
						issue_to_adjust = random.choice(Matches)
						# If the player's stance on issues is more liberal than state, adjust state so that it is more liberal
						if self.states_df[issue_to_adjust][self.states_df.State==state] - self.player_info[player][issue_to_adjust] > 0:
							self.states_df[issue_to_adjust][self.states_df.State==state] += -1
						# Else the player's stance on issues is more conservative than state, adjust state so that it is more conservative
						else:
							self.states_df[issue_to_adjust][self.states_df.State==state] += 1


	def _handle_research_request(self):
		'''Read user research request and send email with info'''
		pass

	def _is_research_request(self, inp):
		'''Check if user input is research request'''
		if len(inp) == 4 and inp[2]=='-' and inp[0:2] in self.states_df.State and inp[3] in ['M','S','F']:
			return True
		else:
			print('Check formatting')

	def _is_player_adjustment(self):
		'''Check if user input is player adjustment request''' 
		pass

	def _adjust_player_stance(self):
		'''Update player_info dictionary with player's new stance'''
		pass

	def _is_slander(self):
		'''Check if user input is slander request'''
		if inp[0:7]=='slander':
			return True
	
	def _slander_opponent(self):
		'''Update states_df (Pandas DataFrame) player-specific slander column randomly (by state) if slander token is played'''
		args = inp.split('-')
		player = args[1]
		ad_spend = args[2]
		for i in range(ad_spend):
			state = random.choice(self.states_df.state)
			# Player 1 column would be 1_slander
			self.states_df[player + '_slander'][self.states_df.state == state] += 1

	def _is_ad(self, inp):
		'''Check if user input is ad request'''
		if inp[0:2]=='ad':
			return True

	def _collect_ad_bonus(self, inp):
		'''Update states_df (Pandas DataFrame) player-specific ad column randomly (by state) if ad token is played'''
		args = inp.split('-')
		player = args[1]
		ad_spend = args[2]
		for i in range(ad_spend):
			state = random.choice(self.states_df.state)
			# Player 1 column would be 1_ad
			self.states_df[player + '_ad'][self.states_df.state == state] += 1 

	def listen(self):
		'''
		CPU stands by ready to send polls or handle research requests
		'''
		print('''Please enter research requests in the following format:
			ex. MA-F

			To send out polling, be sure spreadsheet has been updating and enter 'poll'
			''')
		while True:
			inp = input("Enter Request: ()")
			if inp == 'poll':
				self._send_polls()
			elif self._is_research_request(inp):
				self._handle_research_request()
			elif self._is_player_adjustment(inp):
				self._adjust_player_stance()
			elif self._is_slander(inp):
				self._slander_opponent()
			elif self._is_ad(inp):
				self._collect_ad_bonus(inp)
		self.server.quit()
