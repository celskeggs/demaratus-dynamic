function d_list(success, failure) {
	var xhr = new XMLHttpRequest();
	xhr.open('get', '/data?list=true', true);
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			// 200 is a successful return
			if (xhr.status === 200) {
				success(JSON.parse(xhr.responseText));
			} else {
				failure(xhr.status);
			}
		}
	}
	xhr.send(null);
}
function d_get(key, success, failure) {
	var xhr = new XMLHttpRequest();
	xhr.open('get', '/data?key=' + key, true);
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			// 200 is a successful return
			if (xhr.status === 200) {
				success(xhr.responseText);
			} else {
				failure(xhr.status);
			}
		}
	}
	xhr.send(null);
}
function d_put(data, success, failure) {
	var xhr = new XMLHttpRequest();
	xhr.open('post', '/data', true);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			// 200 is a successful return
			if (xhr.status === 200) {
				success(xhr.responseText);
			} else {
				failure(xhr.status);
			}
		}
	}
	xhr.send("data=" + encodeURIComponent(data));
}
function d_dashed(x) {
	x = d_undashed(x);
	var out = "";
	for (var i=0; i<x.length; i+=8) {
		if (out) { out += " "; }
		out += x.substr(i, 8);
	}
	return out;
}
function d_undashed(x) {
	return x.replace(/ /g, "");
}
