import oeis
from datetime import *
from dateclass import *

def defaultYear(month, day):
	today = date.today()
	if month < today.month:
		return today.year + 1
	if month > today.month:
		return today.year
	if day < today.day:
		return today.year + 1
	return today.year

def toYear(year, month, day):
	if year < 0 or year >= 100:
		return year
	dyear = defaultYear(month, day)
	return year + dyear - (dyear % 100)

def toDate(seq, year, month, day, useTime, timeFirst, useSeconds):

	useYear = year >= 0

	if not useTime:
		if useYear:
			return seqDate(seq, '%02d/%02d/%02d' % tuple(seq.sequence[0:3]), \
				datetime(toYear(seq.sequence[year], seq.sequence[month], seq.sequence[day]), \
				seq.sequence[month], seq.sequence[day]))
		else:
			return seqDate(seq, '%02d/%02d' % tuple(seq.sequence[0:2]), \
				datetime(defaultYear(seq.sequence[month], seq.sequence[day]), seq.sequence[month], seq.sequence[day]))

	if (not timeFirst) and useSeconds and useYear:
		formatted = '%02d/%02d/%02d %02d:%02d:%02d' % tuple(seq.sequence[0:6])
	elif (not timeFirst) and useSeconds and (not useYear):
		formatted = '%02d/%02d %02d:%02d:%02d' % tuple(seq.sequence[0:5])
	elif (not timeFirst) and (not useSeconds) and useYear:
		formatted = '%02d/%02d/%02d  %02d:%02d' % tuple(seq.sequence[0:5])
	elif (not timeFirst) and (not useSeconds) and (not useYear):
		formatted = '%02d/%02d %02d:%02d' % tuple(seq.sequence[0:4])
	elif timeFirst and useSeconds and useYear:
		formatted = '%02d:%02d:%02d %02d/%02d/%02d' % tuple(seq.sequence[0:6])
	elif timeFirst and useSeconds and (not useYear):
		formatted = '%02d:%02d:%02d %02d/%02d' % tuple(seq.sequence[0:5])
	elif timeFirst and (not useSeconds) and useYear:
		formatted = '%02d:%02d  %02d/%02d/%02d' % tuple(seq.sequence[0:5])
	elif timeFirst and (not useSeconds) and (not useYear):
		formatted = '%02d:%02d %02d/%02d' % tuple(seq.sequence[0:4])

	if timeFirst:
		timeOffset = 0
		if useSeconds:
			dateOffset = 3
		else:
			dateOffset = 2
	else:
		dateOffset = 0
		if useYear:
			timeOffset = 3
		else:
			timeOffset = 2

	month = seq.sequence[month + dateOffset]
	day = seq.sequence[day + dateOffset]
	if useYear:
		year = seq.sequence[year + dateOffset]
	else:
		year = defaultYear(month, day)
	hour = seq.sequence[timeOffset]
	# use 12 hour clock if it avoids crappy morning toimes
	if hour > 0 and hour < 7:
		hour += 12
	minute = seq.sequence[timeOffset + 1]
	if useSeconds:
		second = seq.sequence[timeOffset + 2]
	else:
 		second = 0

	return seqDate(seq, formatted, datetime(toYear(year, month, day), month, day, hour, minute, second))


def list2dates(seq):

	# apparently this is how we remove sequences from the db:
	if "Erroneous" in seq.name:
		return []

	l = []

	for timeFirst in [False, True]:
		for useSeconds in [False, True]:
			for useTime in [False, True]:
				try:
					l.append(toDate(seq, 0,1,2, useTime, timeFirst, useSeconds))
				except ValueError:
					pass
				except OverflowError:
					pass
				try:
					l.append(toDate(seq, -1,0,1, useTime, timeFirst, useSeconds))
				except ValueError:
					pass
				except OverflowError:
					pass
				try:
					l.append(toDate(seq, 2,0,1, useTime, timeFirst, useSeconds))
				except ValueError:
					pass
				except OverflowError:
					pass
				try:
					l.append(toDate(seq, 2,1,0, useTime, timeFirst, useSeconds))
				except ValueError:
					pass
				except OverflowError:
					pass
				try:
					l.append(toDate(seq, -1,1,0, useTime, timeFirst, useSeconds))
				except ValueError:
					pass
				except OverflowError:
					pass

	return l
