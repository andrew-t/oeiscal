import oeis
import datetime
from dateclass import date

def defaultYear(month, day):
	today = datetime.date.today()
	if month < today.month:
		return today.year + 1
	if month > today.month:
		return today.year
	if day < today.day:
		return today.year + 1
	return today.year

def list2dates(seq, score):

	name = seq.name
	numbers = seq.sequence
	multiplier = score

	dates = []
	timefirst = 0.7;

	# date-first formats

	## iso format
	d = date(seq, 'iso', multiplier, \
			numbers[0], numbers[1], numbers[2], \
			numbers[3], numbers[4], numbers[5])
	if d.score > 0:
		dates.append(d)

	## uk format
	d = date(seq, 'uk date/time', multiplier, \
			numbers[2], numbers[1], numbers[0], \
			numbers[3], numbers[4], numbers[5])
	if d.score > 0:
		dates.append(d)

	## us format
	d = date(seq, 'us date/time', multiplier, \
			numbers[2], numbers[0], numbers[1], \
			numbers[3], numbers[4], numbers[5])
	if d.score > 0:
		dates.append(d)

	# time-first formats
	multiplier *= 0.7

	## uk format
	d = date(seq, 'uk time/date', multiplier * timefirst, \
			numbers[5], numbers[4], numbers[3], \
			numbers[0], numbers[1], numbers[2])
	if d.score > 0 and d.hours != []:
		dates.append(d)

	## us format
	d = date(seq, 'us time/date', multiplier * timefirst, \
			numbers[4], numbers[5], numbers[3], \
			numbers[0], numbers[1], numbers[2])
	if d.score > 0 and d.hours != []:
		dates.append(d)

	# date-first formats with no year

	## iso format
	d = date(seq, 'iso no year', multiplier, \
			defaultYear(numbers[0], numbers[1]), numbers[0], numbers[1], \
			numbers[2], numbers[3], numbers[4])
	if d.score > 0:
		dates.append(d)

	## uk format
	d = date(seq, 'uk date/time no year', multiplier, \
			defaultYear(numbers[1], numbers[0]), numbers[1], numbers[0], \
			numbers[2], numbers[3], numbers[4])
	if d.score > 0:
		dates.append(d)

	## us format
	d = date(seq, 'us date/time no year', multiplier, \
			defaultYear(numbers[0], numbers[1]), numbers[0], numbers[1], \
			numbers[2], numbers[3], numbers[4])
	if d.score > 0:
		dates.append(d)

	# time-first formats

	## uk format
	d = date(seq, 'uk time/date no year', multiplier * timefirst, \
			defaultYear(numbers[4], numbers[3]), numbers[4], numbers[3], \
			numbers[0], numbers[1], numbers[2])
	if d.score > 0 and d.seconds != []:
		dates.append(d)

	## us format
	d = date(seq, 'us time/date no year', multiplier * timefirst, \
			defaultYear(numbers[3], numbers[4]), numbers[3], numbers[4], \
			numbers[0], numbers[1], numbers[2])
	if d.score > 0 and d.seconds != []:
		dates.append(d)

	## time-first, no seconds. pretty rubbish by now.

	## uk format
	d = date(seq, 'uk time/date no year or seconds', multiplier * timefirst, \
			defaultYear(numbers[3], numbers[2]), numbers[3], numbers[2], \
			numbers[0], numbers[1], -1)
	if d.score > 0 and d.hours != []:
		dates.append(d)

	## us format
	d = date(seq, 'us time/date no year or seconds', multiplier * timefirst, \
			defaultYear(numbers[2], numbers[3]), numbers[2], numbers[3], \
			numbers[0], numbers[1], -1)
	if d.score > 0 and d.hours != []:
		dates.append(d)

	return dates

