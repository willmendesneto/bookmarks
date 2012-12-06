/**
 * Jquery Text Resize plugin
 * @2012 Wilson Mendes ()
 */
/**
 * Modifica o tamanho de fonte do text; Aceita alguns parametros opcionais.
 *
 * @example $.textResize('#the_content', { 'array_option' });
 * @desc Descreve o conteúdo de ações do plugin.
 * @example $.textResize('#the_content', { 'variation': 2, 'containerInsert':
 *          '#myContent', 'optionInterface': 'button', 'cookie': 'value_cookie'
 *          });
 * @desc Descreve o conteúdo com os valores padrão.
 *
 * @param String
 *            com o valor referente ao nome do container ("nome do div" ou "nome
 *            da classe").
 * @param Array
 *            com os atrbutos do plugin para inicialização.
 * @type undefined
 * @name $.textResize
 * @cat Plugins/ Jquery Text Resize
 * @author Wilson Mendes/willmendesneto@gmail.com
 * @author Thiago Teles/thiagoteles.designer@gmail.com
 */
;
(function($) {
	$.textResize = function(selector, settings) {

		var configSelector = 'html, body';
		if (selector) {
			configSelector = selector;
		}
		// Array de configuracoes do Plugin Text Resize
		var config = {
			'variation' : 2, 				// Valor da Variacao dos elementos
			'animation' : false, 			// Animacao da transicao do elemento ("true" or "false")
			'delay' : 1000, 				// Temporizador da animacao ("DELAY"; Somente aceito no caso do valor da animacao ser "true")
			'reduceText' : 'A-', 			// Texto padrao para o campo de reducao da fonte
			'resetText' : 'A', 				// Texto padrao para o campo de tamanho padrao da fonte
			'enlargeText' : 'A+', 			// Texto padrao para o campo de acrescimo de fonte
			'classReduce' : 'reduceText', 	// Nome da classe de reducao da fonte
			'classReset' : 'resetText', 	// Nome da classe de reducao da fonte
			'classEnlarge' : 'enlargeText', // Nome da classe de reducao da fonte
			'clicks' : false, 				// Quantidade de clicks configurado ("false" ou inteiro referente a quantidade de clicks aceitos)
			'containerInsert' : false, 		// Container onde vao ser inseridos os elementos ("false" ou nome do elemento onde serao inseridos os elementos
											//EX: "#container-test" ou ".container-test")
			'optionInterface' : 'link', 	// Opcao de retorno de insercao dos elementos que trabalham com a fonte ("link" ou "button";
											// Aceitos somente se a opcao "containerInsert" for diferente de "false")
			'cookie' : true, 				// Verificacao para salvar fonte como COOKIE ("false" ou nome do elemento do array "COOKIE" configurado; Necessita do arquivo "jquery.cookie.js")
			'fontType' : 'px',
			'imageAnimation' : false, 				// Verificacao para salvar fonte como COOKIE ("false" ou nome do elemento do array "COOKIE" configurado; Necessita do arquivo "jquery.cookie.js")

		}
		if (settings) {
			$.extend(config, settings);
		}

		var obj = $(configSelector), // o objeto com base no container informado na inicializacao
			img = obj.find('img'), // Achando imagem dentro do container inicializado
			// Pegando a altura da imagem
			fontDefault = obj.css('font-size'), // Pegando o atributo "font-size" do container inicializado
			currentSize = parseInt(obj.css('font-size')), // Passando o valor "font-size" para um valor @int
			userClicksReduce = userClicksEnlarge = 0, // Inicializando o valor de quantidade de clicks para aumento com '0'
			percent = 100, // Valor para imagem
			fontEnlarge = fontReduce = cookieClicks = value = ''// Inicializando o valor de reducao com '' Valor do COOKIE
		;
		if(config.imageAnimation !== false){
			var imgDefault = img.width(),
				imgDefaultHeight = img.height();
			img.removeAttr('width').removeAttr('height').width(imgDefault).height(imgDefaultHeight);
		}
		// Pegando o valor do COOKIE, caso ele exista no NAVEGADOR insere o valor dele no container especificado
		if ((config.cookie !== false) && (config.cookie !== 'null') && (config.cookie !== null)) {
			cookieClicks = $.cookie(config.cookie);
			currentSize = (! isNaN(cookieClicks) &&  cookieClicks != null) ? parseInt(cookieClicks) : parseInt(fontDefault);
			console.log(currentSize);
			//	Verificando se o Tamanho em COOKIE e maior que o tamanho padrao
			if( currentSize != null && currentSize > fontDefault){
				userClicksEnlarge = ((currentSize-fontDefault)/2);
				console.log('aumentado reduce: '+userClicksReduce+ 'current: '+currentSize+', default: '+fontDefault+', cookie: '+cookieClicks);
			}//	Verificando se o Tamanho em COOKIE e maior que o tamanho padrao
			if( currentSize != null && currentSize < fontDefault){
				userClicksReduce = ((fontDefault-currentSize)/2);
				console.log('aumentado clicks: '+userClicksEnlarge+ 'current: '+currentSize+', default: '+fontDefault+', cookie: '+cookieClicks);
			}
			obj.css('font-size', cookieClicks + config.fontType);
		}

		// Verificacao da configuracao do container onde sera inserido os botoes/links do plugin, verificando a configuracao do plugin
		if (config.containerInsert !== false) {
			// Verificacao para a opcao de interface como LINK ou BUTTON
			if (config.optionInterface == 'link') {
				$(config.containerInsert).html(
						'<a href="#" class="' + config.classReduce
								+ '" title="reduce text">' + config.reduceText
								+ '</a><a href="#" class="' + config.classReset
								+ '" title="reset text">' + config.resetText
								+ '</a><a href="#" class="'
								+ config.classEnlarge
								+ '" title="enlarge text">'
								+ config.enlargeText + '</a>');
			} else if (config.optionInterface == 'button') {
				$(config.containerInsert).html(
						'<input type="button" value="' + config.reduceText
								+ '" class="' + config.classReduce
								+ '" /><input type="button" value="'
								+ config.resetText + '" class="'
								+ config.classReset
								+ '" /><input type="button" value="'
								+ config.enlargeText + '" class="'
								+ config.classEnlarge + '" />');
			}

		}
		// Funcao para reducao do texto
		$('.' + config.classReduce).live('click', function() {

			if (config.clicks > userClicksReduce) {

				percent -= config.variation;
				fontReduce = currentSize - config.variation;

				if (config.animation == true) {
					obj.animate({
						'font-size' : fontReduce + config.fontType
					}, config.delay);

					if(config.imageAnimation !== false){
						img.animate({
							'width' : parseInt((imgDefault * percent) / 100),
							'height' : parseInt((imgDefaultHeight * percent) / 100)
						}, config.delay);
					}

				} else {
					obj.css('font-size', fontReduce);
				}
				// Incremento no contador REDUCE
				++userClicksReduce;
				// Decremento no contador ENLARGE
				if (userClicksEnlarge > 0)
					--userClicksEnlarge;

				currentSize = fontReduce;
				// COOKIE Verification
				if ((config.cookie != false)) {
					cookieClicks = $.cookie(config.cookie);
					cookieClicks = currentSize;
					$.cookie(config.cookie, cookieClicks, {path : '/', expires : 5 });
				}
			}
		});
		// Funcao para ampliar o texto
		$('.' + config.classEnlarge).live('click', function() {
			if (config.clicks > userClicksEnlarge) {

				percent += config.variation;
				fontEnlarge = currentSize + config.variation;
				if (config.animation == true) {
					obj.animate({
						'font-size' : fontEnlarge + config.fontType
					}, config.delay);

					if(config.imageAnimation !== false){
						img.animate({
							'width' : parseInt((imgDefault * percent) / 100),
							'height' : parseInt((imgDefaultHeight * percent) / 100)
						}, config.delay);
					}
				} else {
					obj.css('font-size', fontEnlarge);
				}
				// Decremento no contador ENLARGE
				++userClicksEnlarge;
				// Decremento no contador REDUCE
				if (userClicksReduce > 0)
					--userClicksReduce;

				currentSize = fontEnlarge;
				// COOKIE Verification
				if ((config.cookie !== false)) {

					cookieClicks = $.cookie(config.cookie);
					cookieClicks = currentSize;
					$.cookie(config.cookie, currentSize, { path : '/', expires : 5 });
				}
			}
		});
		// Funcao para retornar o texto ao tamanho padrÃ£o
		$('.' + config.classReset).live('click', function() {

			if (config.animation == true) {
				obj.animate({
					'font-size' : fontDefault
				}, config.delay);

				if(config.imageAnimation !== false){
					img.animate({
						'width' : imgDefault,
						'height' : imgDefaultHeight
					}, config.delay);
				}
			} else {
				obj.css('font-size', fontDefault);
			}
			// Reiniciando os valores
			userClicksReduce = userClicksEnlarge = 0;
			currentSize = parseInt(fontDefault);
			// COOKIE Verification
			if ((config.cookie !== false)) {
				cookieClicks = 'null';
				$.cookie(config.cookie, cookieClicks, { path : '/', expires : 5 });
			}
		});
		return this;
	}
})(jQuery);
/**
 * Finalizando o plugin Jquery Text Resize @name = jquery.text.resize.js
 *  @author = Wilson Mendes Neto / Thiago Teles
 */