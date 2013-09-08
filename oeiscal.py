from list2dates import *
from oeis import *
from datetime import *
from dateclass import *

start = datetime.now()
end = start + timedelta(366)

# todo - nicely?
calendar = []
for m in xrange(0,12):
	calendar.append([])
	for n in xrange(0,31):
		calendar[m].append([])

for s in xrange(1,228465):
	print 'processing sequence %d' % s
	seq = sequence(s)
	if len(seq.sequence) < 6:
		continue
	print 'sequence name: %s' % seq.name
	dates = list2dates(seq)
	print '%d dates found' % len(dates)
	for d in dates:
		if d.value > start and d.value < end:
			calendar[d.value.month-1][d.value.day-1].append(d)

output = open('oeis.ics', 'w')
output.write('BEGIN:VCALENDAR\n')
for m in xrange(0,12):
	for n in xrange(0,31):
		dates = calendar[m][n]
		if len(dates) > 0:
			bestdate = []
			for date in dates:
				if bestdate == []:
					bestdate = date
					continue
				if date.score > bestdate.score:
					bestdate = date
			bestdate.writeICal(output)
			print bestdate.toString()
output.write('END:VCALENDAR\n')