{
	var elem = document.createElement("style");
	elem.type = "text/css";
	elem.textContent = '\
.msgreadout_flash {\
	color: red;\
}';
	document.head.appendChild(elem);
}
function msgreadout_bind(x) {
	var elem = document.getElementById(x);
	var flash_id = 0;
	function flash(timeout) {
		elem.classList.add("msgreadout_flash");
		var local_id = ++flash_id;
		function reset_flash() {
			if (local_id == flash_id) {
				elem.classList.remove("msgreadout_flash");
			}
		}
		setTimeout(reset_flash, timeout || 500);
	}
	return {flash: flash, set: function(msg, doflash) {
		elem.textContent = msg;
		if (doflash) {
			flash();
		}
	}};
}

