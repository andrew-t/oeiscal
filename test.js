require('./oeis.js')
.get(123456)
.then(function(x) { console.log('result:'); console.dir(x); } )
.catch(function(x) { console.log('err:'); console.dir(x); } );