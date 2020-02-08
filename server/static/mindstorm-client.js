function uhlala() {
	console.log('uhlala');
}

function populate() {
	populateMotors();
	populateSensors();
}

function populateSensors() {
	let xhr = new XMLHttpRequest();
	xhr.open('GET', '/sensors');
	xhr.responseType = 'json';
	xhr.send();

	xhr.onload = function() {
		let responseObj = xhr.response;
		for(var sensor in responseObj.sensors) {
			var name = responseObj.sensors[sensor];
			getDataFor('sensor_row', '/sensors/' + name, name);		
		}
	};
}

function populateMotors() {
	let xhr = new XMLHttpRequest();
	xhr.open('GET', '/motors');
	xhr.responseType = 'json';
	xhr.send();

	xhr.onload = function() {
		let responseObj = xhr.response;
		for(var motor in responseObj.motors) {
			var name = responseObj.motors[motor];
			getDataFor('motor_row', '/motors/' + name, name);		
		}
	};
}

function buildControlElement(idOfParentRow, headerText, values) {
	var row = document.getElementById(idOfParentRow);
	var wrapper = document.createElement('div');
	wrapper.classList.add('card');
	wrapper.classList.add('mb-4');
	wrapper.classList.add('shadow-sm');
	var header = document.createElement('div');
	header.classList.add('card-header')
	var h = document.createElement('h3');
	h.innerText = headerText;
	header.appendChild(h);
	var body = document.createElement('div');
	body.classList.add('card-body');

	wrapper.appendChild(header);
	wrapper.appendChild(body);

	var writable = values['__writable']
	if (typeof(writable) === 'undefined') { writable = [] }
	console.log('__writable', writable);

	for(var key in values) {
		console.log('wonder if', key, ' is in ', writable);
		if (key === '__writable') { continue; }
		var input = null;
		var value = values[key];
		if (Array.isArray(value)) {
			input = document.createElement('select');
			for(var item in value) {
				var option = document.createElement('option');
				option.text = value[item];
				option.value = value[item];
				input.appendChild(option);
			}
		} else {
			input = document.createElement('input');
			input.value = value;
		}

		input.enabled = writable.indexOf(key) >= 0;
		if (writable.indexOf(key) >= 0) {
			console.log('IT WAS :)');
		} else {
			console.log('it was not :(');
		}
		input.classList.add('form-control');
		input.id = key;
		input.name = key;
		var inputWrap = document.createElement('div');
		inputWrap.classList.add('col-sm-8');
		inputWrap.appendChild(input);
		var div = document.createElement('div');
		div.classList.add('form-group');
		div.classList.add('row');
		var label = document.createElement('label');
		label.classList.add('col-sm-4');
		label.classList.add('col-form-label');
		label.innerText = key;
		label.for = key;
		div.appendChild(label);
		div.appendChild(inputWrap);
		body.appendChild(div);
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


function getTemplateForMotor(wrapperId, motorName, continuation) {
	console.log('getting template for ', motorName);
	$.get('/motor-template', function(responseObj) { 
		var wrapper = $('#' + wrapperId);
		var container = document.createElement('div');
		$(container).attr('mindstorm-component', motorName);
		console.log(container);
		console.log(responseObj);
		$(container).append($.parseHTML(responseObj));
		wrapper.append(container);
		if (typeof(continuation) !== "nothing") {
			continuation();
		}
	});
}

function getDataFor(motorName, dataPath) {
	console.log('getting data for ', motorName, dataPath);
	$.get(dataPath, function(responseObject) {
		console.log('received', responseObject);
		var wrapper = $('[mindstorm-component="' + motorName + '"] [data-bind]')
			.each(function(ix, me) {
				console.log('Attempt to bind ', motorName, $(me).attr('data-bind'));
				var value = responseObject[$(me).attr('data-bind')];
				var attr = $(me).attr('data-attr');
				if (attr === "innerText") {
					$(me).html(value);

				} else {
					$(me).attr(attr, value);
				}
				for(var aix = 0; aix < me.attributes.length; aix++) {
					var attr = me.attributes[aix];
					if (!attr.name.startsWith('data-bind-attr-')) {
						continue;
					}
					var propertyname = attr.value.startsWith('-')
						? attr.value.substr(1) 
						: attr.value; 
					var negative = attr.value.startsWith('-')
						? -1 : 1;
					
					var attributeName = attr.name.substring('data-bind-attr-'.length);
					var value = negative * responseObject[propertyname];

					console.log("Binding" , attr, propertyname, negative, attributeName, value);
					$(me).attr(attributeName, value);
				}
			});

	}, 'json');	
}

$(document).ready(function() {
	$.get("/motors", function(response){
		for(var motor in response.motors) {
			let motorName = response.motors[motor];
			console.log('motor ', motor, motorName);
			getTemplateForMotor("motor_row", motorName, function() { getDataFor(motorName, '/motors/' + motorName) });
		}
	});
});
