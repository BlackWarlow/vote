var variants = []
for (var i=2; i<10; ++i){
	variants[i] = false;
}
function add_variant(){
	if (variants[9] == true){
		document.getElementById('add_btn').style = 'display: none;';
	}
	var n = 0;
	for (var i=2; i<10; ++i){
		if (variants[i] == false){
			variants[i] = true;
			n = i+1;
			break;
		}
	}
	document.getElementById(n+'').style.display = 'block';
}

function delete_variant(id){
	if (variants[9] == true){
		document.getElementById('add_btn').style = 'display: inline-table;';
	}
	variants[id-1] = false;
	document.getElementById('id_variant_'+id).value = '';
	document.getElementById(id+'').style = 'display: none;';
}