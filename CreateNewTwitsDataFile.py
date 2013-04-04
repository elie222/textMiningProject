import sys

NO_OF_LINES = 1000
TICKER = 'MU'

output = ''

f = open('2Year-StockTwits-Data.csv', 'r')

i = 0
for line in f:
	if '$' + TICKER in line or i == 0:
		output += line
		i += 1
		# print i
		if i == NO_OF_LINES:
			break

f.close()

g = open('StockTwitsData' + TICKER + str(i) + '.csv', 'w')
g.write(output)
g.close()