import pandas as pd

class Election:
	''' Election keeps a hidden record of states stance on issues, 
	    handles research requests, and manages polling.
	'''
	def __init__(self, num_players = 4):
		self.num_players = 4
		self._set_state_stance()
		self._get_player_info()
    
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


    def _set_state_stance(self):
    	self.states_df = pd.read_csv('States.csv')
    	if self.states_df.M.isnull().sum()>0:
    		self.states_df.M = np.random.randint(-3,4,size = len(self.states_df))
    	if self.states_df.S.isnull().sum()>0:
    		self.states_df.S = np.random.randint(-3,4,size = len(self.states_df))
    	if self.states_df.FA.isnull().sum()>0:
    		self.states_df.FA = np.random.randint(-3,4,size = len(self.states_df))

    def _send_polls(self):
    	self.campaign_df = pd.read_csv('Campaign.csv')
    	self._adjust_state_params()
    	self._author_email()

    def _author_email(self):
    	pass

    def _adjust_state_params():
    	for state in self.states_df.State:
    		for player in self.player_info.keys():
    			if self.campaign_df[player][self.campaign_df.state==state] == 1:
    				# Find most aligned issue
    				Diff_Dict = {}
    				for key in ['M','S','FA']:
    					Diff_Dict[key] = abs(self.states_df[key][self.states_df.State==state] - self.player_info[player][key])
 					Diff_Dict = { k:v for k, v in Diff_Dict.items() if v != 0}
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

        		
