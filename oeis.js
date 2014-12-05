var Oeis = (function(){

	var fs = require('fs'),
		http = require('http'),
		q = require('q');

	fs.mkdir('cache', function(){});

	function Sequence(id, name, numbers) {
		this.id = id;
		this.name = name;
		this.numbers = numbers;
		fs.exists(cacheFilename(id), function (exists) {
			if (!exists)
				fs.writeFile(cacheFilename(id), JSON.stringify({
					id: id,
					name: name,
					numbers: numbers
				}, {
					encoding: 'utf8'
				}));
		});
	}

	Sequence.prototype.getUrl = function() {
		return 'http://oeis.org/' + a(this.id);
	}
	Sequence.prototype.a = function() {
		return a(this.id);
	}

	function a(id) {
		var id = '000000' + id;
		return 'A' + id.substr(id.length - 6);
	}

	function cacheFilename(id) {
		return 'cache/' + a(id) + '.json';
	}

	function get(id) {
		var d = q.defer();
		fs.exists(cacheFilename(id), function (exists) {
			if (exists)
				fs.readFile(cacheFilename(id), {
					encoding: 'utf8'
				}, function(err, data) {
					if (err)
						d.reject(err);
					else try {
						data = JSON.parse(data);
						d.resolve(new Sequence(data.id, data.name, data.numbers));
					} catch(e) {
						d.reject(e);
					}
				});
			else
				http.request({
					hostname: 'oeis.org',
					path: '/search?q=id:' + a(id) + '&fmt=text',
					method: 'GET'
				}, function(response) {
					if (response.statusCode != 200)
						d.reject(response);
					else try {
						var txt = '';
						response.on('data', function(chunk) {
							txt += chunk;
						});
						response.on('end', function() {
							try {
								var lines = txt.split(/[\r\n]+/g),
									numbers = [],
									S = 'S',
									name,
									startSequence = true,
									found = false;
								lines.forEach(function(line) {
									if (line[0] !== '%') return;
									found = true;
									switch (line[1]) {
										case S:
											if (name) break;
											S = String.fromCharCode(S.charCodeAt(0) + 1);
											var these = line.substr(11)
															.split(',')
															.map(function(n) {
																return parseInt(n, 10);
															});
											numbers = startSequence
												? these
												: numbers.concat(these);
											if (!isNaN(these[these.length - 1]))
												startSequence = true;
											else {
												startSequence = false;
												numbers.pop();
											}
											break;
										case 'N':
											name = line.substr(11);
											break;
									}
								});
								if (found)
									d.resolve(new Sequence(id, name || a(id), numbers));
								else
									d.reject('NO_SUCH_SEQUENCE');
							} catch(e) {
								d.reject(e);
							}
						});
					} catch(e) {
						d.reject(e);
					}
				}).end();
		});
		return d.promise;
	}

	return {
		Sequence: Sequence,
		get: get
	};

})();

module.exports = Oeis;