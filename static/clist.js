function clist_add_styles(code) {
	var elem = document.createElement("style");
	elem.type = "text/css";
	elem.textContent = code;
	document.head.appendChild(elem);
}
clist_add_styles("\
.clist_list ul {\
	background-color: #272822;\
	color: #8f908a;\
	padding-left: 0px;\
	list-style-type: none;\
}\
.clist_list ul li.clist_selected {\
	padding-left: 0px;\
	list-style-type: none;\
	color: white;\
}\
.clist_list ul li {\
	margin-left: 0px;\
	background-color: #373832;\
	margin-bottom: 10px;\
	text-align: center;\
}\
.clist_list ul li:hover {\
	background-color: #474842;\
}\
.clist_list ul li:active {\
	background-color: #575852;\
}");
function clist_bind(docid, suffix, stringifier) {
	var doc = document.getElementById(docid);
	doc.classList.add("clist_list");
	var ul = document.createElement("ul");
	var elem = document.createElement("li");
	function update_readout() {
		elem.textContent = (ul.children.length - 1) + " " + suffix;
	}
	ul.appendChild(elem);
	doc.appendChild(ul);
	function unselect_all() {
		for (var i=0; i<ul.children.length; i++) {
			ul.children[i].classList.remove("clist_selected");
		}
	}
	update_readout();
	var listeners = [update_readout];
	function notify() {
		for (var i=0; i<listeners.length; i++) {
			listeners[i]();
		}
	}
	elem.onclick = function() {
		unselect_all();
		notify();
	};
	return {add: function(x) {
			var elem = document.createElement("li");
			elem.valueContent = x;
			elem.textContent = stringifier(x);
			elem.onclick = function() {
				if (this.classList.contains("clist_selected")) {
					unselect_all();
				} else {
					unselect_all();
					this.classList.add("clist_selected");
				}
				notify();
			}.bind(elem);
			ul.appendChild(elem);
			notify();
		}, remove: function(x) {
			for (var i=1; i<ul.children.length; i++) {
				if (ul.children[i].valueContent == x) {
					ul.removeChild(ul.children[i]);
					notify();
					return i-1;
				}
			}
			return -1;
		}, clear: function() {
			while (ul.children.length > 1) {
				ul.removeChild(ul.children[1]);
			}
			notify();
		}, length: function() {
			return ul.children.length - 1;
		}, get: function(i) {
			return (i < 0 || i >= ul.children.length - 1) ? null : ul.children[i+1].valueContent;
		}, set: function(i, v) {
			if (i < 0 || i >= ul.children.length - 1) { return; }
			ul.children[i+1].valueContent = v;
			ul.children[i+1].textContent = stringifier(v);
			notify();
		}, selected: function() {
			for (var i=1; i<ul.children.length; i++) {
				if (ul.children[i].classList.contains("clist_selected")) {
					return ul.children[i].valueContent;
				}
			}
			return null;
		}, unselect_all: function() {
			unselect_all();
			notify();
		}, listeners: listeners
	};
}

