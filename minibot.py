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
today = date.today()
times = []
for s in xrange(223750,223869):
	seq = sequence(s)
	if len(seq.sequence) < 6:
		continue
	dates = list2dates(seq)
	for d in dates:
		if d.value.date() == today:
			times.append(d)
print '%d dates found' % len(times)

# let's not piss people off though
if len(times) > 10:
	t = 0
	while t < len(times):
		if len(times[t].formatted) < 12:
			times.remove(times[t])
		else:
			t = t + 1
print '%d dates accepted' % len(times)

if len(times) == 0:
	times.append(seqDate(sequence(140000), 'test post', datetime.now() + timedelta(0,5)))
	a = times[0].seq
	a.name = a.name+a.name
	a.name = a.name+a.name
	a.name = a.name+a.name
	a.name = a.name+a.name

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
