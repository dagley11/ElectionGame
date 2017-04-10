import pandas as pd
import smtplib
import numpy as np
import random
import operator

def compute_rank(int_list):
    temp = int_list.argsort()
    ranks = np.empty(len(int_list), int)
    return np.arange(len(int_list))

class Election:
	''' Election keeps a hidden record of states stance on issues, 
	    handles research requests, and manages polling.
	'''
	def __init__(self, num_players = 4):
		self.num_players = 4
		self._set_state_stance()
		self._get_player_info()
		self._init_email()
		self._compute_score()

    def _init_email(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login("alexander.s.dagley@gmail.com", "filibuster")
    
    def _compute_score(self):
    	for player in self.players:
    		self.states_df[player + '_score'] = self.states_df.apply(
    			lambda x: sum([abs(x[i] - self.player_info[key][i]) for i in ['M','S','FA']])
    			)
    	for player in self.players:
    		self.states_df[player + '_rank'] = self.states_df.apply(
    			lambda x: compute_rank(x[player + '_score'] +  [x[other_player + '_score'] 
    				                    for other_player in self.players 
    				                    if other_player != player])[0]
    			          )
    	self.scores = {}
    	for player in self.players:
    		self.scores[player] = sum(self.states_df.Votes[self.states_df[player + '_rank'] == 1])

    def self._get_player_info():
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
    	self.states_df = pd.read_csv('States.csv')
    	for issue in ['M','S','FA']:
    		self.states_df[issue] = np.random.randint(-3,4,size = 50)

    def _send_polls(self):
    	mod_states_df = pd.read_csv('States.csv')
    	self._adjust_state_params(mod_states_df)
    	self._compute_score()
    	self._author_email()

    def _author_email(self):
    	msg = "YOUR MESSAGE!"
        self.server.sendmail(self.emails, "THE EMAIL ADDRESS TO SEND TO", msg)

    def _adjust_state_params(self, mod_states_df):
    	for state in self.states_df.State:
    		sorted_players = list(reversed(sorted(self.scores, key=self.scores.get)))
    		for player in self.players:
    			if mod_states_df[player][self.states_df.state==state] == 1:
    				# Find most aligned issue
    				Diff_Dict = {}
    				for key in ['M','S','FA']:
    					Diff_Dict[key] = abs(self.states_df[key][self.states_df.State==state] - self.player_info[player][key])
 					Diff_Dict = {k:v for k, v in Diff_Dict.items() if v != 0}
 					if len(Diff_Dict) > 0:
						min_val = np.min(Diff_Dict.values())
						Matches = [k for k, v in Diff_Dict.items() if v == min_val]
						issue_to_adjust = random.choice(Matches)
						if self.states_df[issue_to_adjust][self.states_df.State==state] - self.player_info[player][issue_to_adjust] > 0:
							self.states_df[issue_to_adjust][self.states_df.State==state] += -1
						else:
							self.states_df[issue_to_adjust][self.states_df.State==state] += 1


    def _handle_research_request(self):
    	pass

    def _is_research_request(self, inp):
    	if len(inp) == 4 and inp[2]=='-' and inp[0:2] in self.states and inp[3] in ['M','S','F']:
    		return True
    	else:
    		print('Check formatting')

    def _is_player_adjustment(self):
    	pass

    def _adjust_player_stance(self):
    	pass

    def _is_slander(self):
    	pass
    
    def _slander_opponent(self):
    	pass

    def _is_ad(self):
    	pass

    def _collect_ad_bonus(self):
    	pass

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
        		self._collect_ad_bonus()
        self.server.quit()
