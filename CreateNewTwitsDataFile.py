import sys

NO_OF_LINES = 600
TICKER = 'MLNX'

output = ''

f = open('2Year-StockTwits-Data.csv', 'r')

i = 0
for line in f:
	if '$' + TICKER in line:
		output += line
		i += 1
		# print i
		if i == NO_OF_LINES:
			break

f.close()

g = open('StockTwitsData' + TICKER + str(NO_OF_LINES) + '.csv', 'w')
g.write(output)
g.close()