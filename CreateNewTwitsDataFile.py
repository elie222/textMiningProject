NO_OF_LINES = 100000

output = ''

f = open('2Year-StockTwits-Data.csv', 'r')

i = 0
for line in f:
	output += line
	i += 1
	if i == NO_OF_LINES:
		break

f.close()

g = open('StockTwitsData' + str(NO_OF_LINES) + '.csv', 'w')
g.write(output)
g.close()