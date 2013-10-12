class seqDate(object):

	def __init__(self, seq, formatted, value, offset = 0):
		self.seq = seq
		self.formatted = formatted
		self.value = value
		self.offset = offset

		self.searchUrl = ('http://oeis.org/search?q=id:A%06d+seq:' % seq.id) + \
			formatted.replace(':', '%2C').replace('/', '%2C').replace(' ', '%2C').replace('%2C0', '%2C').lstrip('0')

	def toString(self):
		try:
			string = self.seq.name
		except AttributeError:
			string = 'unnamed'
		string += ' -- ' + self.formatted
		return string

	def writeICal(self, calFile):

		tstring = '%04d%02d%02dT%02d%02d%02dZ' % \
			(self.value.year, self.value.month, self.value.day, \
			self.value.hour, self.value.minute, self.value.second)

		calFile.write('BEGIN:VEVENT\n')
		calFile.write('DTEND;VALUE=DATE-TIME:%s\n' % tstring)
		calFile.write('DTSTART;VALUE=DATE-TIME:%s\n' % tstring)
		calFile.write('SUMMARY:%s - %s\n' % (self.formatted, self.seq.name))
		calFile.write('DESCRIPTION:http://oeis.org/A%06d\\n%s\n' % (self.seq.id, self.seq.getPage().replace('\n', '\\n')))
		calFile.write('END:VEVENT\n')

	def beats(self, other):

		# rule one: if the formatted date is longer, it's a win.
		if len(self.formatted) > len(other.formatted):
			return True
		if len(self.formatted) < len(other.formatted):
			return False
		
		# rule two: prefer times after 7am
		if self.value.hour >= 7 and other.value.hour < 7:
			return True
		if self.value.hour < 7 and other.value.hour >= 7:
			return False

		# rule three: prefer early IDs as they're probably less arcane
		if self.seq.id < other.seq.id:
			return True
		if self.seq.id > other.seq.id:
			return False

		# rule four: prefer extracts from near the beginning.
		if self.offset < other.offset:
			return True
		if self.offset > other.offset:
			return False

		# neither beats the other
		return False
