import urllib2
import re


class sequence(object):

	def getPage(self):
		filename = 'oeis/A%06d.txt' % self.id
		try:
			txt = open(filename, 'r').read()
		except IOError:
			print 'getting from ' + self.apiUrl
			txt = urllib2.urlopen(self.apiUrl).read(20000)
			open(filename, 'w').write(txt)
		return txt

	def __init__(self, i, name = None, numbers = None):

		self.id = i
		if name == None:
			self.name = 'name not found'
		else:
			self.name = name
		self.url = 'http://oeis.org/A%06d' % self.id
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
				self.numbers = nums
				self.sequence = map(int, nums.split(','))

		else:
			self.numbers = numbers

		self.sequence = map(int, self.numbers.split(','))



def cacheFile(id, mode):
	return open('cache/%d' % id, mode)

def cacheLines(id):
	return cacheFile(id, 'r').read(10000000).split('\n')

def all(skip = 0):

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
	cacheId = 0
	cache = cacheLines(0)
	line = 0
	for i in xrange(skip + 1, count + 1):
		if (i % 1000) == 0:
			cacheId += 1
			try:
				cache = cacheLines(cacheId)
			except:
				cache = None
			line = 0
		try:
			yield sequence(i, \
				cache[line], \
				cache[line + 1])
			line += 2
		except:
			yield sequence(i)

def cacheFrom(start = 0):

	cacheId = start
	cacheText = ''
	for seq in all(start * 1000):
		i = seq.id
		cacheText += seq.name + '\n' + seq.numbers + '\n'
		if (i % 1000) == 0:
			cacheFile(cacheId, 'w').write(cacheText)
			cacheId += 1
			cacheText = ''

	# catch the last few we missed before
	cacheFile(cacheId, 'w').write(cacheText)

