class Action:
	def __init__(self, userid,contentid,actiontype,actioncomment,date):
		self.userid = userid
		self.contentid = contentid
		self.actiontype = actiontype #this might commenting on play or thinking of going that play
		self.actioncomment = actioncomment 
		self.date = date
#this table hold all post that user do
#all comments, likes of user do are in that table