class date(object):
		
	def monthLength(self):
		if self.month == 2:
			if self.year % 4 == 0 and \
			   self.year % 100 != 0 or \
			   self.year % 400 == 0:
				return 29
			return 28
		return (31,0,31,30,31,30,31,31,30,31,30,31)[self.month - 1]

	def toString(self):
		try:
			string = '%s (score: %d) -- ' % (self.seq.name, self.score)
		except:
			string = 'unnamed -- '
		if self.hours == [] or self.minutes == []:
			string += '%04g/%02g/%02g' % (self.year, self.month, self.day)
		elif self.seconds == []:
			string += '%04g/%02g/%02g %02g:%02g' % (self.year, self.month, self.day, self.hours, self.minutes)
		else:
			string += '%04g/%02g/%02g %02g:%02g:%02g' % (self.year, self.month, self.day, self.hours, self.minutes, self.seconds)
		return string

	def __init__(self, seq, formatted, score, year, month, day, hours, minutes, seconds):
		self.seq = seq
		self.formatted = formatted
		self.score = score
		self.year = year
		self.month = month
		self.day = day
		self.hours = hours
		self.minutes = minutes
		self.seconds = seconds

		if self.year < 100:
			# todo: get current date
			year = 2013
			month = 9
			day = 2
			self.year += 2000
			if self.year < year or \
			   (self.year == year and self.month < month) or \
			   (self.year == year and self.month == month and self.day < day):
				self.year += 100

		if self.month < 1 or self.month > 12 or \
		   self.day < 1 or self.day > self.monthLength() or \
		   self.year < 0 or \
		   self.year < 2012 or self.year > 2113: # bit of a judgement call here
			self.score = -1
			return

		if self.hours < 0 or self.hours > 23 or \
		   self.minutes < 0 or self.minutes > 59:
			self.hours = []
			self.minutes = []
			self.seconds = []
			score *= 0.5
			return

		# ignore leap seconds for now:
		if self.seconds < 0 or self.seconds > 59:
			seconds = []
			score *= 0.9
			return

	def equals(self, other):
		return other.year == self.year and \
		       other.month == self.month and \
		       other.day == self.day and \
		       other.hours == self.hours and \
		       other.minutes == self.minutes and \
		       other.seconds == self.seconds

	def before(self, other):
		if other.year > self.year:
			return True
		if other.year < self.year:
			return False
		if other.month > self.month:
			return True
		if other.month < self.month:
			return False
		if other.day > self.day:
			return True
		if other.day < self.day:
			return False
		if other.hours == []:
			return False
		if self.hours == []:
			return True
		if other.hours > self.hours:
			return True
		if other.hours < self.hours:
			return False
		if other.minutes > self.minutes:
			return True
		if other.minutes < self.minutes:
			return False
		if other.seconds == []:
			return False
		if self.seconds == []:
			return True
		if other.seconds > self.seconds:
			return True
		return False

	def after(self, other):
		return not (self.equals(other) or self.before(other))