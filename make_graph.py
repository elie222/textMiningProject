import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl

import datetime as dt

monthsMap = {'Jan': '01', 'Feb': '02', 'Mar': '03','Apr': '04','May': '05','Jun': '06','Jul': '07','Aug': '08','Sep': '09','Oct': '10','Nov': '11','Dec': '12'}

def converDate(strDate):
    splitted = strDate.split(' ')
    month= monthsMap[splitted[1]]
    return splitted[2] + '/' + month + '/' + splitted[5]

mpl.rcParams['axes.color_cycle'] = ['r', 'b']

dates = ['01/02/1991','01/03/1991','01/04/1991','01/05/1991','03/05/1991','04/06/1991','06/06/1991','17/06/1991','22/06/1991']
x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]

posY = [3,7,90,3,55,78,99,3,25]
negY = [2,6,77,8,98,12,32,5,17]

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plot = plt.plot(x,negY,x,posY)
plt.show(plot)


#print converDate('Wed Dec 23 16:12:37 UTC 2009')