function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

async function close_msg(id) {
	document.getElementById(id).style='opacity: 0; transition: ease-in-out 1.5s;';
	await sleep(1500);
	document.getElementById(id).style='display: none;';
}