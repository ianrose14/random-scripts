function wrapper() {
	blowup();
}

console.log('before');
setTimeout(() => {
	console.log('firing');
	wrapper();
	console.log('done firing');
}, 3000);
console.log('after');
