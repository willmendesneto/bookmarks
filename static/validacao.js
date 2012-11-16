function stringVazia(pStr){
    var re = /^\s*$/g;
    var ret = pStr.match(re) ? true : false;
    return ret;
}

function radioButtonSelecionado(grp) {
	var ret = -1;
	for(var k = 0; k < grp.length; k++){
		if(grp[k].checked == '1'){
			ret = k;
			break;
		}
	}
	if(ret == -1 & grp.checked == '1'){ret = 0};
	return ret;
}

function checkBoxesMarcados(pGrp){
	var ret = [];
	for(var k = 0; k < pGrp.length; k++){
		if(pGrp[k].checked){			
			ret.push(pGrp[k].value);
		}
	}	
	return ret;
}

function numeroBrValido(pTxt, pCas) {
	var re = /[0-9,.]+/g;
	var ret = false;
	if(pTxt.match(re)){
		var num = pTxt.split(',');
		if(num.length == 1 || (num.length == 2 && num[1].length <= pCas)) {
			var intg = num[0].split('.');
			var flag = true;
			for(var k = 0; k < intg.length; k++) {
				if(k == 0){
					if(intg.length > 1 & intg[k].length < 1){
						flag = false;
						break
					}
				}
				else{
					if(intg[k].length != 3){
						flag = false;
						break
					}	
				}
			}
			ret = flag;
		}
	}	
	return ret;	
}

function dataBrValida(str){
	//revisada em 13/12/2006	
	ret = false;	
	vet = str.split('/');
	y1 = vet[2];
	y1 = '19' + y1;
	y1 = y1.substr(y1.length - 4, 4);
	m1 = vet[1];
	m1 = '0' + m1;
	m1 = m1.substr(m1.length - 2, 2);
	d1 = vet[0];
	d1 = '0' + d1;
	d1 = d1.substr(d1.length - 2, 2);
	dtus = m1 + '/' + d1 + '/' + y1;		
	dat = new Date(dtus);
	y2 = dat.getYear();
	if(y2 < 1900) y2 += 1900;
	y2 = '19' + y2;
	y2 = y2.substr(y2.length - 4, 4);
	m2 = dat.getMonth() + 1;
	m2 = '0' + m2;
	m2 = m2.substr(m2.length - 2, 2);
	d2 = dat.getDate();
	d2 = '0' + d2;
	d2 = d2.substr(d2.length - 2, 2);
	chk = m2 + '/' + d2 + '/' + y2;		
	if(dtus == chk) {ret = true};
	return ret;
}

function cnpjValido(pTxt){
    ret = false;
    if(pTxt.length == 14){
        ret = true;
            dig1 = 0;
            dig2 = 0;
            mult1 = '543298765432';
        mult2 = '6543298765432';
        for(x = 0; x <= 11; x++)
         dig1 = dig1 + (parseInt(pTxt.slice(x, x + 1)) * parseInt(mult1.slice(x, x + 1)));
        for(x = 0; x <= 12; x++)
         dig2 = dig2 + (parseInt(pTxt.slice(x, x + 1)) * parseInt(mult2.slice(x, x + 1)));
        dig1 = (dig1 * 10) % 11;
        dig2 = (dig2 * 10) % 11;
        if(dig1 == 10) {dig1 = 0;}
        if(dig2 == 10) {dig2 = 0;}
        if(dig1 != parseInt(pTxt.slice(12, 13)))
            ret = false;
        else
            if(dig2 != parseInt(pTxt.slice(13, 14)))
                  ret = false;
    }
    return ret;
}

function cpfValido(pTxt){
    ret = true;
    if (pTxt.length != 11 || pTxt == "00000000000" || pTxt == "11111111111" ||
    pTxt == "22222222222" ||    pTxt == "33333333333" || pTxt == "44444444444" ||
    pTxt == "55555555555" || pTxt == "66666666666" || pTxt == "77777777777" ||
    pTxt == "88888888888" || pTxt == "99999999999")
        ret = false;
    if(ret){
        soma = 0;
        for (i = 0; i < 9; i++)
            soma += parseInt(pTxt.charAt(i)) * (10 - i);
        resto = 11 - (soma % 11);
        if (resto == 10 || resto == 11)
            resto = 0;
        if (resto != parseInt(pTxt.charAt(9)))
            ret = false;
    }
    if(ret){
        soma = 0;
        for(i = 0; i < 10; i++)
            soma += parseInt(pTxt.charAt(i)) * (11 - i);
        resto = 11 - (soma % 11);
        if (resto == 10 || resto == 11)
            resto = 0;
        if (resto != parseInt(pTxt.charAt(10)))
            ret = false;
    }
    return ret;
}

//--------------------

function campoTextoValido(pNom, pMsg){	
	ret = true;
 	obj = document.getElementsByName(pNom);
 	if(obj[0] != null){
 		if(stringVazia(obj[0].value)){
 			ret = false;
 			alert(pMsg);
			obj[0].focus();
 		}
 	}
 	return ret;
}

function campoCheckboxValido(pNom, pMsg){	
	ret = true;
 	obj = document.getElementsByName(pNom);
 	if(obj != null){		
 		if(checkBoxesMarcados(obj).length < 1){
 			ret = false;
 			alert(pMsg);
			if(obj.length == 1){
				obj.focus();
			}
			else{
				obj[0].focus();
			}
 		}
 	}
 	return ret;
}

function campoRadioValido(pNom, pMsg){
	 ret = true;
	 obj = document.getElementsByName(pNom);
	 if(obj[0] != null){
		 if(radioButtonSelecionado(obj) < 0){
			 ret = false;
			 alert(pMsg);
			 obj[0,0].focus();
		 }
	}
	return ret;
}

function campoSelectValido(pNom, pIdx, pMsg){
	ret = true;
	obj = document.getElementsByName(pNom);
	if(obj[0] != null){
		if(obj[0].selectedIndex < pIdx){
			ret = false;
			alert(pMsg);
			obj[0].focus();
		}
	}
	return ret;
}

function campoNumericoValido(pNom, pCas, pMsg){
	ret = true;
	obj = document.getElementsByName(pNom);
	if(obj[0] != null){
		if(! numeroBrValido(obj[0].value, pCas)){
			ret = false;
			alert(pMsg);
			obj[0].focus();
		}
	}
	return ret;
}

function campoDataValido(pNom, pMsg){
	ret = true;
	obj = document.getElementsByName(pNom);
	if(obj[0] != null){
		if(! dataBrValida(obj[0].value)){
			ret = false;
			alert(pMsg);
			obj[0].focus();
		}
	}
	return ret;
}

function campoCpfValido(pNom, pMsg){
	ret = true;
	obj = document.getElementsByName(pNom);
	if(obj[0] != null){
		if(! cpfValido(obj[0].value)){
			ret = false;
			alert(pMsg);
			obj[0].focus();
		}
	}
	return ret;
}

function campoCnpjValido(pNom, pMsg){
	ret = true;
	obj = document.getElementsByName(pNom);
	if(obj[0] != null){
		if(! cnpjValido(obj[0].value)){
			ret = false;
			alert(pMsg);
			obj[0].focus();
		}
	}
	return ret;
}