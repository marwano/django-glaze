
function glaze_table(source) {
	var keys = Object.keys(source[0]["fields"]);
	var keys = ["pk"].concat(keys.sort());
	var rows = [];
	for (var i = 0; i < source.length; i++) {
		var row = [];
		var fields = source[i]["fields"];
		fields["pk"] = source[i]["pk"];
		for (var j = 0; j < keys.length; j++) {
			row[keys[j]] = fields[keys[j]]
		}
		rows[i] = row;
	}
	return rows;
}

function GlazeToggleDetails(id) {
	var e = document.getElementById(id);
	e.style.display = (e.style.display == 'block') ? 'none' : 'block';
	return false;
}

