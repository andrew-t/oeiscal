from list2dates import *
from oeis import *
from datetime import *
from dateclass import *

#from twitter import *
from re import *
from subprocess import call
import urllib

from time import *

import os

def tryDate(hourIndex):
	# pretty sure all this global abuse is allowed in python.
	try:
		if hourIndex > yearIndex:
			format = '%02d/%02d/%02d %01d:%02d:%02d'
			minIndex = hourIndex - 3
		else:
			format = '%1d:%02d:%02d %02d/%02d/%02d'
			minIndex = hourIndex

		year = seq.sequence[yearIndex]
		if year < 100:
			year += today.year - (today.year % 100)

		d = seqDate(seq, format % tuple(seq.sequence[minIndex:minIndex + 6]), \
				datetime(year, seq.sequence[month], seq.sequence[day], \
					seq.sequence[hourIndex], seq.sequence[hourIndex + 1], seq.sequence[hourIndex + 2]))
		times.append(d)
		print 'haha, found a great one: %s (%s)' % (d.formatted, d.seq.name)

	except Execption:
		pass


os.chdir('/home/pi/oeiscal')

# i've premade some credentials for this.
twitter = Twitter(auth=OAuth('1879496899-i0mC4OBfPKEGZn5g0NXiSXMsO8DARfqHKxItJr6', 'G9qmGtEr3PsiGwJjpOnKqL03G4TZaPm7ThnbcWB05k', "xCDjsWwMfu3J2Kp5eN8QQ", "nf5oGUGr0IuoTY5G8WJvY8d184m3lFpBrib9KWcU"))

# pull out all the interesting times for today

# this is a dirty hack to make sure we don't do the wrong date in daylight savings time:
today = (datetime.today() + timedelta(0.25)).date()
times = []
for seq in all():
	if (seq.id % 1000) == 0:
		print 'processing sequence %d' % seq.id
	if len(seq.sequence) < 6:
		continue

	# try the first six in any order:
	dates = list2dates(seq)
	for d in dates:
		if d.value.date() == today:
			times.append(d)

	# for good measure, pull out anything at all, from anywhere in the sequence,
	# that uses all six parts of the date:
	yearIndices = [i for i, x in enumerate(seq.sequence) if x == today.year or x == today.year % 100]
	if len(yearIndices) == 0:
		continue
	monthIndices = [i for i, x in enumerate(seq.sequence) if x == today.month]
	if len(monthIndices) == 0:
		continue
	dayIndices = [i for i, x in enumerate(seq.sequence) if x == today.day]
	if len(dayIndices) == 0:
		continue

	for yearIndex in yearIndices:
		for month in monthIndices:
			for day in dayIndices:
				# ISO format:
				if day == month + 1 and month == yearIndex + 1:
					tryDate(day + 1)
					tryDate(yearIndex - 3)
				# UK format:
				if yearIndex == month + 1 and month == day + 1:
					tryDate(yearIndex + 1)
					tryDate(day - 3)
				# US format:
				if yearIndex == day + 1 and month == day - 1:
					tryDate(yearIndex + 1)
					tryDate(month - 3)

print '%d dates found' % len(times)

# one per sequence
usedSeqs = []
t = 0
while t < len(times):
	this = times[t]
	if this.seq.id in usedSeqs:
		for t2 in times:
			if t2.seq.id == this.seq.id:
				if this.beats(t2):
					times.remove(t2)
				else:
					times.remove(this)
				break
	else:
		usedSeqs.append(this.seq.id)
		t = t + 1
print '%d unique sequences' % len(times)

# let's not piss people off though
if len(times) > 10:
	t = 0
	while t < len(times):
		if len(times[t].formatted) < 12:
			times.remove(times[t])
		else:
			t = t + 1
print '%d dates accepted' % len(times)

# get them in order
times.sort(key = lambda x: x.value)

# tweet them!
for time in times:
	# wait for the first one
	wait = (time.value - datetime.now()).total_seconds()
	if wait < 0:
		# missed it, move on with life.
		continue
	sleep(wait)
	text = time.formatted + ' http://oeis.org/A%06d ' % time.seq.id
	lengthLeft = 140 - len(text)
	if len(time.seq.name) <= lengthLeft:
		text = text + time.seq.name
	else:
		text = text + time.seq.name[0:(lengthLeft - 4)] + '...'
	try:
		twitter.statuses.update(status=text)
	except:
		print 'bummed up a tweet'
