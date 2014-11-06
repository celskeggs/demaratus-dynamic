var d_creds = [];
function d_encrypt(password, plaintext) {
	return sjcl.encrypt(password, plaintext, {iter:2000, ts:128, ks: 256});
}
function d_decrypt(password, plaintext) {
	try {
		return sjcl.decrypt(password, plaintext);
	} catch(e) {
		return null;
	}
}
function d_decrypt_any(plaintext) {
	for (var i=0; i<d_creds.length; i++) {
		var decry = d_decrypt(d_creds[i], plaintext);
		if (decry !== null) {
			return {success: true, key_id: i, key: d_creds[i], out: decry};
		}
	}
	return {success: false};
}
function d_add_credential(cred) {
	d_creds.push(cred);
}
function d_remove_credential(cred) {
	var index = d_creds.indexOf(cred);
	d_creds.splice(index, 1);
}
function d_count_credentials() {
	return d_creds.length;
}
function d_list_credentials(cb) {
	for (var i=0; i<d_creds.length; i++) {
		cb(d_creds[i]);
	}
}
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

