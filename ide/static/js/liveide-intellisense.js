/*
    LiveIDE
    Intellisense module.

    Online IDE for Python projects.
    Homepage and documentation: https://github.com/baseapp/liveide/

    Copyright (c) 2013, BaseApp, V. Sergeyev.
*/

(function(){
    var LiveIDE = this.LiveIDE || {},
        that = LiveIDE;

	LiveIDE.intellisense = {
		show: function(token, pos, ext) {
			// token - part of word
			// pos - {pageX, pageY} position of cursor
			// ext - file extension
			var menu = $(that.dom.intellisense),
				list = menu.find("select"),
				has_options = false;

			list.html("");

			// TODO: use file extension and appropriate lexemes
			has_options = this.python(list, token.replace(/^\s+|\s+$/g, '')); //trim spaces in token

			//if (has_options)
			menu.css("display", "block")
				.css("left", pos.pageX + 20)
				.css("top", pos.pageY)
				.show();

			//list.focus();

			return has_options;
		},

		hide: function() {
			$(that.dom.intellisense).hide();
		},

		/* -- Autocompletion rules ----------------------------------------- */

		python: function (list ,token) {
			var re = new RegExp(token, "gi"),
			has_options = false,
				keywords = ( /* This list taken from https://github.com/ajaxorg/ace-builds/blob/master/src/mode-python.js */
		        "and|as|assert|break|class|continue|def|del|elif|else|except|exec|" +
		        "finally|for|from|global|if|import|in|is|lambda|not|or|pass|print|" +
		        "raise|return|try|while|with|yield" +
		    	
		    	"True|False|None|NotImplemented|Ellipsis|__debug__" +
		    
		        "abs|divmod|input|open|staticmethod|all|enumerate|int|ord|str|any|" +
		        "eval|isinstance|pow|sum|basestring|execfile|issubclass|print|super|" +
		        "binfile|iter|property|tuple|bool|filter|len|range|type|bytearray|" +
		        "float|list|raw_input|unichr|callable|format|locals|reduce|unicode|" +
		        "chr|frozenset|long|reload|vars|classmethod|getattr|map|repr|xrange|" +
		        "cmp|globals|max|reversed|zip|compile|hasattr|memoryview|round|" +
		        "__import__|complex|hash|min|set|apply|delattr|help|next|setattr|" +
		        "buffer|dict|hex|object|slice|coerce|dir|id|oct|sorted|intern"
		    );

		    $.each(keywords.split("|"), function(i, v) {
		    	if ((v.search(re) > -1) || (!token) || (token == " ")) {
		    		list.append('<option value="' + v + '">' + v + '</option>');
		    		has_options = true;
		    	}
		    });

		    return has_options;
		}
	}

	this.LiveIDE = LiveIDE;
}).call(this);