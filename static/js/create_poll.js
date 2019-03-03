var variants = [];
variants[0] = true;
variants[1] = true;
for (var i=2; i<10; ++i){
	variants[i] = false;
}

check_state();

function get_filled(){
	for (var i=0; i<10; ++i){
		if (variants[i] == false) return false
	}
	return true
}

function add_variant(){
	var n = 0;
	for (var i=2; i<10; ++i){
		if (variants[i] == false){
			variants[i] = true;
			n = i+1;
			break;
		}
	}
	document.getElementById(n+'').style.display = 'block';
	if (get_filled())
		document.getElementById('add_btn').style = 'display: none;';
	console.log(variants);
}

function delete_variant(id){
	variants[id-1] = false;
	document.getElementById('id_variant_'+id).value = '';
	document.getElementById(id+'').style = 'display: none;';
	if (!get_filled())
		document.getElementById('add_btn').style = 'display: inline-table;';
}

function check_state(){
	if(document.getElementById('id_one_variant').checked){
		document.getElementById('ch_t').style = 'background-color: #429c42;';
		document.getElementById('ch_f').style = 'background-color: transparent;';
	} else {
		document.getElementById('ch_t').style = 'background-color: transparent;';
		document.getElementById('ch_f').style = 'background-color: #429c42;';
	}
}

