function btnset_add_styles(code) {
	var elem = document.createElement("style");
	elem.type = "text/css";
	elem.textContent = code;
	document.head.appendChild(elem);
}
btnset_add_styles('\
.btnset button {\
	position: relative;\
	background-color: #277822;\
	border: none;\
	color: white;\
	font: 15px "Monaco","Menlo","Ubuntu Mono","Consolas","source-code-pro",monospace;\
	margin: 5px;\
}\
.btnset button.btnset_disabled {\
	background-color: #772822;\
}');
function btnset_bind(docid) {
	var doc = document.getElementById(docid);
	doc.classList.add("btnset");
	var buttons = [];
	function update() {
		for (var i=0; i<buttons.length; i++) {
			var en = buttons[i].enabled;
			if (en) {
				if (en(buttons[i].name)) {
					buttons[i].elem.classList.remove("btnset_disabled");
				} else {
					buttons[i].elem.classList.add("btnset_disabled");
				}
			}
		}
	}
	return {update: update, add: function(name, cb, enabled) {
			var elem = document.createElement("button");
			elem.type = "button";
			elem.onclick = cb;
			elem.textContent = name;
			doc.appendChild(elem);
			buttons.push({name: name, cb: cb, enabled: enabled, elem: elem});
			update();
		}
	};
}

