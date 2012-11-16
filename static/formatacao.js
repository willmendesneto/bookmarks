function formatarDataBr(pDat){
	y2k = '2000';
	zrs = '00';
	prts = pDat.split('/');
	d = prts[0];
	d = zrs.substr(0, 2 - d.length) + d;	
	m = prts[1];
	m = zrs.substr(0, 2 - m.length) + m;	
	y = prts[2];
	y = y2k.substr(0, 4 - y.length) + y;	
	ret = d + '/' + m + '/' + y;	
	return ret;
}