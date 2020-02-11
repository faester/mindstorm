function uhlala() {
	console.log('uhlala');
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
