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

def toDate(seq, year, month, day, useTime, timeFirst, useSeconds):

	useYear = year >= 0

	if not useTime:
		if year >= 0:
			return seqDate(seq, '%02d/%02d/%02d' % tuple(seq.sequence[0:3]), \
				datetime(seq.sequence[year], seq.sequence[month], seq.sequence[day]))
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
		if year >= 0:
			timeOffset = 3
		else:
			timeOffset = 2

	month = seq.sequence[month + dateOffset]
	day = seq.sequence[day + dateOffset]
	if useYear:
		year = seq.sequence[year]
	else:
		year = defaultYear(month, day)
	hour = seq.sequence[timeOffset]
	minute = seq.sequence[timeOffset + 1]
	if useSeconds:
		second = seq.sequence[timeOffset + 2]
	else:
		second = 0

	return seqDate(seq, formatted, datetime(year, month, day, hour, minute, second))


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
					l.append(toDate(seq, 3,1,2, useTime, timeFirst, useSeconds))
				except ValueError:
					pass
				except OverflowError:
					pass
				try:
					l.append(toDate(seq, 3,2,1, useTime, timeFirst, useSeconds))
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
