import urllib2

class sequence(object):

	def getPage(self):
		filename = 'oeis/A%06d.txt' % self.id
		try:
			txt = open(filename, 'r').read()
		except IOError:
			txt = urllib2.urlopen('http://oeis.org/search?q=id:A%06d&fmt=text' % self.id).read(20000)
			open(filename, 'w').write(txt)
		return txt.split('\n')

	def __init__(self, i):

		self.id = i
		self.name = 'name not found'

		nums = ''
		last = ord('R')

		for line in self.getPage():
			if len(line) < 2:
				continue
			lid = ord(line[1])
			line = line[11:]

			if lid == last + 1:
				#bit of a glitch in sequence 466 here if we don't work around it, so...
				if nums[-1:] == ',':
					nums += line
				else:
					nums = line
				last = lid
			elif nums != '':
				last = ord('Z')

			if lid == ord('N'):
				self.name = line
		
		if len(nums) == 0:
			self.sequence = []
		else:
			self.sequence = map(int, nums.split(','))
