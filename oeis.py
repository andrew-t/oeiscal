import urllib2
import re


class sequence(object):

	def getPage(self):
		filename = 'oeis/A%06d.txt' % self.id
		try:
			txt = open(filename, 'r').read()
		except IOError:
			txt = urllib2.urlopen(self.apiUrl).read(20000)
			open(filename, 'w').write(txt)
		return txt

	def __init__(self, i, name = None, numbers = None):

		self.id = i
		if name == None:
			self.name = 'name not found'
		else:
			self.name = name
		self.url = 'http://oeis.org/%06d' % self.id
		self.apiUrl = 'http://oeis.org/search?q=id:A%06d&fmt=text' % self.id

		if numbers == None:
			nums = ''
			last = ord('R')

			for line in self.getPage().split('\n'):
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

		else:
			self.sequence = numbers


def all():

	# find latest number of sequences
	try:
		try:
			countString = open('count', 'r').read()
		except:
			countString = re.search('Contains (\\d+) sequences', \
				urllib2.urlopen(self.url).read(20000)).group(0)
			try:
				open('count', 'w').write(countString)
			except:
				pass
		count = int(countString)
	except:
		count = 228922

	# iterate through them
	for id in xrange(1, count + 1):
		yield sequence(id)