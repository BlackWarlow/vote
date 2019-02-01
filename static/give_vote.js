function add_vote(){
	var input = document.getElementsByName('optionsRadios');
	for (var i = 0; i < input.length; i++) {
		if (input[i].type == "radio" && input[i].checked) {
		
			var prog = document.getElementById(input[i].id+"progress");
			prog.value = a.value + 1;
			prog.max = a.max + 1;
			
			var count = document.getElementById(input[i].id+"counter");
			count.innerHTML = parseInt(b.innerHTML)+1;
			
			var vote = document.getElementById(input[i].id+"vote");
			vote.innerHTML =  "|ВАШ ГОЛОС УСПЕШНО ОТДАН ЗА ДАННЫЙ ВАРИАНТ|";
		}
	}
}

function disableIt(id){
	document.getElementById(id).setAttribute('disabled', true);
}