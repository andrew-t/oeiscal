class seqDate(object):

	def __init__(self, seq, formatted, value):
		self.seq = seq
		self.formatted = formatted
		self.value = value
		self.score = len(formatted) * 1000 + seq.id * 0.001

	def toString(self):
		try:
			string = '%s (score: %d) -- ' % (self.seq.name, self.score)
		except:
			string = 'unnamed -- '
		string += self.formatted
		return string

	def writeICal(self, calFile):

		tstring = '%04d%02d%02dT%02d%02d%02dZ' % \
			(self.value.year, self.value.month, self.value.day, \
			self.value.hour, self.value.minute, self.value.second)

		calFile.write('BEGIN:VEVENT\n')
		calFile.write('DTEND;VALUE=DATE-TIME:%s\n' % tstring)
		calFile.write('DTSTART;VALUE=DATE-TIME:%s\n' % tstring)
		calFile.write('SUMMARY:%s\n' % self.formatted)
		calFile.write('DESCRIPTION:A%06d: %s\n' % (self.seq.id, self.seq.name))
		calFile.write('END:VEVENT\n')