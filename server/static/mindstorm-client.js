function uhlala() {
	console.log('uhlala');
}

function buildControlElement(idOfParentRow, header, values) {
	var row = document.getElementById(idOfParentRow);
	var wrapper = document.createElement('div');
	wrapper.classList.add('card');
	wrapper.classList.add('mb-4');
	wrapper.classList.add('shadow-sm');
	var header = document.createElement('div');
	header.classList.add('card-header')
	header.innerText = header; 
	var body = document.createElement('div');
	body.classList.add('card-body');
	body.innerText = 'New and fancy body!';

	wrapper.appendChild(header);
	wrapper.appendChild(body);

	var writable = values['__writable']
	if (typeof(writable) === 'undefined') { writable = [] }
	console.log('__writable', writable);

	for(var key in values) {
		if (key === '__writable') { continue; }
		if (key in writable) {
			var input = document.createElement('input');
			input.value = values[key]
			body.appendChild(input);
		} else {
			var div = document.createElement('div');
			div.innerText = values[key];
			body.appendChild(div);
		}
	}

	row.appendChild(wrapper);
}

function getDataFor(wrapperId, path, title) {
	let xhr = new XMLHttpRequest();

	xhr.open('GET', path);

	xhr.responseType = 'json';

	xhr.send();

	xhr.onload = function() {
		let responseObj = xhr.response;
		buildControlElement(wrapperId, title, responseObj);		
	};
}
