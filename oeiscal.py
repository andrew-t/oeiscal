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

for seq in all():
	print 'processing sequence %d' % seq.id
	if len(seq.sequence) < 6:
		continue
	print 'sequence name: %s' % seq.name
	dates = list2dates(seq)
	print '%d dates found' % len(dates)
	for d in dates:
		if d.value > start and d.value < end:
			if not calendar[d.value.month-1][d.value.day-1] == []:
				if not d.beats(calendar[d.value.month-1][d.value.day-1]):
					continue
			calendar[d.value.month-1][d.value.day-1] = d

output = open('oeis.ics', 'w')
output.write('BEGIN:VCALENDAR\n')
for m in xrange(0,12):
	for n in xrange(0,31):
		if calendar[m][n] == []:
			continue
		calendar[m][n].writeICal(output)
		print '%d/%d %s' % (m, n, calendar[m][n].toString())
output.write('END:VCALENDAR\n')