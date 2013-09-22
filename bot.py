from list2dates import *
from oeis import *
from datetime import *
from dateclass import *

from twitter import *
from re import *
from subprocess import call
import urllib

from time import *

# i've premade some credentials for this.
twitter = Twitter(auth=OAuth('1879496899-i0mC4OBfPKEGZn5g0NXiSXMsO8DARfqHKxItJr6', 'G9qmGtEr3PsiGwJjpOnKqL03G4TZaPm7ThnbcWB05k', "xCDjsWwMfu3J2Kp5eN8QQ", "nf5oGUGr0IuoTY5G8WJvY8d184m3lFpBrib9KWcU"))

# pull out all the interesting times for today

# this is a dirty hack to make sure we don't do the wrong date in daylight savings time:
today = (datetime.today() + timedelta(0.25)).date()
times = []
for seq in all():
	seq = sequence(s)
	if len(seq.sequence) < 6:
		continue
	dates = list2dates(seq)
	for d in dates:
		if d.value.date() == today:
			times.append(d)
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
	twitter.statuses.update(status=text)
