console.log('before');
setTimeout(() => {
	console.log('firing');
	x = 4;
	x.foo();
	console.log('done firing');
}, 3000);
console.log('after');
