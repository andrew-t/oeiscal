from list2dates import *
from oeis import *
import datetime
from dateclass import date

today = datetime.date.today()
start = date([],'',0, today.year,today.month,today.day, -1,-1,-1)
end = date([],'',0, today.year+1,today.month,today.day, -1,-1,-1)

# todo - nicely
calendar = []
for m in xrange(0,12):
	calendar.append([])
	for n in xrange(0,31):
		calendar[m].append([])

for s in xrange(1,10000):
	print 'processing sequence %d' % s
	seq = sequence(s)
	if len(seq.sequence) < 6:
		continue
	print 'sequence name: %s' % seq.name
	for date in list2dates(seq, 1000 * (0.5 ** (s * 0.001)) + 500):
		if date.after(start) and date.before(end):
			calendar[date.month-1][date.day-1].append(date)

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
			output.write('BEGIN:VEVENT\n')
			try:
				if bestdate.seconds > -1:
					raise TypeError
				tstring = '%04d%02d%02dT%02d%02d%02dZ' % (bestdate.year, bestdate.month, bestdate.day, bestdate.hours, bestdate.minutes, bestdate.seconds)
			except TypeError:
				try:
					tstring = '%04d%02d%02dT%02d%02d00Z' % (bestdate.year, bestdate.month, bestdate.day, bestdate.hours, bestdate.minutes)
				except TypeError:
					tstring = '%04d%02d%02dT000000Z' % (bestdate.year, bestdate.month, bestdate.day)
			output.write('DTEND;VALUE=DATE-TIME:%s\n' % tstring)
			output.write('DTSTART;VALUE=DATE-TIME:%s\n' % tstring)
			output.write('SUMMARY:%s\n' % bestdate.seq.name)
			output.write('DESCRIPTION:Sequence A%06d\n' % bestdate.seq.id)
			output.write('END:VEVENT\n')
			print bestdate.toString()
output.write('END:VCALENDAR\n')