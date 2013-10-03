from list2dates import *
from oeis import *
from datetime import *
from dateclass import *

from twitter import *
from re import *
from subprocess import call
import urllib

from time import *

import os

def isValidDate(hour, minute, second, year, month, day):

	if year < 0 or month < 1 or day < 1 or hour < 0 or minute < 0 or second < 0 or \
			year > 3000 or month > 12 or day > 31 or hour > 23 or minute > 59 or second > 59:
		return False

	if month == 2:
		if year < 100:
			year += today.year - (today.year % 100)
		if year % 400 == 0:
			return day <= 29
		if year % 100 == 0:
			return day <= 28
		if year % 4 == 0:
			return day <= 29
		return day <= 28

	return day <= (31 - (((month - 1) % 7) % 2))

def tryDate(hourIndex):

	if hourIndex > yearIndex:
		format = '%02d/%02d/%02d %01d:%02d:%02d'
		minIndex = hourIndex - 3
	else:
		format = '%1d:%02d:%02d %02d/%02d/%02d'
		minIndex = hourIndex

	if hourIndex < 0 or hourIndex + 2 >= len(seq.sequence):
		return

	hour = seq.sequence[hourIndex]
	minute = seq.sequence[hourIndex + 1]
	second = seq.sequence[hourIndex + 2]
	year = seq.sequence[yearIndex]
	month = seq.sequence[monthIndex]
	day = seq.sequence[dayIndex]

	if not isValidDate(hour, minute, second, year, month, day):
		return

	if year < 100:
		year += today.year - (today.year % 100)

	d = seqDate(seq, format % tuple(seq.sequence[minIndex:minIndex + 6]), \
			datetime(year, month, day, \
				hour, minute, ))
	times.append(d)
	print 'haha, found a great one: %s (%s)' % (d.formatted, d.seq.name)

def onePerSequence(l):
	usedSeqs = []
	t = 0
	while t < len(l):
		this = l[t]
		if this.seq.id in usedSeqs:
			for t2 in l:
				if t2.seq.id == this.seq.id:
					if this.beats(t2):
						l.remove(t2)
					else:
						l.remove(this)
					break
		else:
			usedSeqs.append(this.seq.id)
			t = t + 1
	print '%d unique sequences' % len(l)
	return l

os.chdir('/home/pi/oeiscal')

# i've premade some credentials for this.
twitter = Twitter(auth=OAuth('1879496899-i0mC4OBfPKEGZn5g0NXiSXMsO8DARfqHKxItJr6', 'G9qmGtEr3PsiGwJjpOnKqL03G4TZaPm7ThnbcWB05k', "xCDjsWwMfu3J2Kp5eN8QQ", "nf5oGUGr0IuoTY5G8WJvY8d184m3lFpBrib9KWcU"))

# pull out all the interesting times for today

# this is a dirty hack to make sure we don't do the wrong date in daylight savings time:
today = (datetime.today() + timedelta(0.25)).date()
times = []
backupTimes = []
for seq in all():
	if (seq.id % 1000) == 0:
		print 'processing sequence %d' % seq.id
	if len(seq.sequence) < 6:
		continue

	# try the first six in any order:
	dates = list2dates(seq)
	for d in dates:
		if d.value.date() == today:
			backupTimes.append(d)

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
		for monthIndex in monthIndices:
			for dayIndex in dayIndices:
				# ISO format:
				if dayIndex == monthIndex + 1 and monthIndex == yearIndex + 1:
					tryDate(dayIndex + 1)
					tryDate(yearIndex - 3)
				# UK format:
				if yearIndex == monthIndex + 1 and monthIndex == dayIndex + 1:
					tryDate(yearIndex + 1)
					tryDate(dayIndex - 3)
				# US format:
				if yearIndex == dayIndex + 1 and monthIndex == dayIndex - 1:
					tryDate(yearIndex + 1)
					tryDate(monthIndex - 3)

print '%d excellent dates found' % len(times)
print '%d backup dates found' % len(backupTimes)

onePerSequence(times)

if len(times) < 10:
	print 'adding in backups.'
	times.extend(backupTimes)
	onePerSequence(times)

# let's not piss people off though
if len(times) > 10:
	times.sort(key = lambda x: -len(x.formatted))
	t = 10
	while t < len(times):
		if len(times[t].formatted) < 17:
			times = times[0:t]
			break
		t += 1
print '%d dates accepted:' % len(times)

for t in times:
	print '  %s -- A%06d (%s)' % (t.formatted, t.seq.id, t.seq.name)

# get them in order
times.sort(key = lambda x: x.value)

# tweet them!
for time in times:
	# wait for the first one
	wait = (time.value - datetime.now()).total_seconds()
	print 'next tweet in %d seconds' % wait
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
