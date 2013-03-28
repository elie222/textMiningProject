import csv
import re


class gradeTwit:

<<<<<<< HEAD
    veryPositiveScore = 1000
	veryNegativeScore = -1000
	

=======
>>>>>>> nothing
	def __init__(self):
		self.MU=set()
		self.C=set()
		self.MLNX=set()
		self.GOOG=set()
		self.GS=set()
		self.POT=set()
		self.AAPL=set()
		self.LVS=set()
		self.INTC=set()
		self.MSFT=set()
		self.companies=[self.MU,self.C,self.MLNX,self.GOOG,self.GS,self.POT,self.AAPL,self.LVS,self.INTC,self.MSFT]
		self.twit=""

	def readDic(self,name):
		sum=0
		with open(name, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in reader:
				sent=row[0].replace("0","\d*")
				#print(sent)
				sum+=self.points(sent)
		return sum

	def points(self,sent):
		match = re.search(sent, self.twit)
		# If-statement after search() tests if it succeeded
	 	if match:                      
	    	print 'found', match.group() ## 'found word:cat'
			return 1
	 	else:
	    	return 0
	
	def insertToList(self,stock,twit):
		if stock == 'MU':
			self.MU.add(twit)
		elif stock == 'C':
			self.C.add(twit)
		elif stock == 'MLNX':
			self.MLNX.add(twit)	
		elif stock == 'GOOG':
			self.GOOG.add(twit)
		elif stock == 'GS':
			self.GS.add(twit)
		elif stock == 'POT':
			self.POT.add(twit)
		elif stock == 'AAPL':
			self.AAPL.add(twit)
		elif stock == 'LVS':
			self.LVS.add(twit)
		elif stock == 'INTC':
			self.INTC.add(twit)
		elif stock == 'MSFT':
			self.MSFT.add(twit)

	def scoreTwit(self,twit,curGrade):#to change according our dission for grading
		if curGrade>veryPositiveScore:
            return "<very positive> "+twit+" </very positive>"
        elif curGrade>0:
			return "<positive> "+twit+" </positive>"
        elif curGrade<veryNegativeScore:
            return "<very negative> "+twit+" </very negative>"
		elif curGrade<0:
			return "<negative> "+twit+" </negative>" 
		return "<neutral> "+twit+" </neutral>" 

	def grade(self,twitData,company):
		if (company!= None):
			self.twit=twitData
			print self.twit
			pos=self.readDic('Positive.xml.csv')
			print pos

			neg=self.readDic('Negative.xml.csv')
			print neg
			total=pos - neg
			print total
			finalTwit=self.scoreTwit(self.twit,total)
			self.insertToList(company,finalTwit)
			for com in self.companies:
				print com
