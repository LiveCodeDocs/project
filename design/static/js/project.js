//config.extraPlugins = 'CodeMirror';

$(document).ready(function() {

	var addEventListeners = function(myCodeMirror) {
		$("#new-file-add-button").on("click", function() {
			var filename = $("#new-file-name").val();
			var projectId = 2;
			addNewFile(filename, projectId);
		});
		$("#project-files-list").on("click", ".list-group-item", function() {
			var fileId = $(this).attr("data-id");
			setEditorText(fileId, myCodeMirror);
		});
	}

	var setEditorText = function(fileId, myCodeMirror) {
		$.ajax({
			type: "GET",
			url: "http://livecodedocs.csse.rose-hulman.edu:5000/getFileContent",
			data: { "fileId": fileId },
			success: function(data) {
				var id;
				for (id in data) {
					if (data[id] != null) {
						myCodeMirror.setValue(data[id]);
					} else {
						myCodeMirror.setValue("");
					}
				}
				console.log("Successful content load: ", data);
			},
			error: function(data) {
				console.log("ERROR: ", data);
			}
		});			
	}

	var addFilesHandler = function(isVisible) {
		$(".files").unbind("click");
		if (isVisible) {
			$(".files").on("click", function() {
				$(".files").css("right", "0px");
				$(".file-list").hide();
				addFilesHandler(false);
			});
		} else {
			$(".files").on("click", function() {
				$(".files").css("right", "200px");
				$(".file-list").show();
				addFilesHandler(true);
			});
		}
	}

	var addConsoleHandler = function(isVisible) {
		$(".console-toggle").unbind("click");
		if (isVisible) {
			$(".console-toggle").on("click", function() {
				$(".console-toggle").css("bottom", "0px");
				$(".console").hide();
				addConsoleHandler(false);
				document.getElementById("filesid").style.height = "730px";
				document.getElementById("text_editor_div").style.height = "730px";	
			});
		} else {
			$(".console-toggle").on("click", function() {
				$(".console-toggle").css("bottom", "200px");
				$(".console").show();
				addConsoleHandler(true);
				document.getElementById("filesid").style.height = "530px";
				document.getElementById("text_editor_div").style.height = "530px";
			});
		}
	}

	var addNewFile = function(filename, projectId) {
		if (filename == "") {
			return;
		}
		var query = [{
			"fileName": filename,
			"projectid": projectId
		}];

		$.ajax({
			type: "POST",
			url: "http://livecodedocs.csse.rose-hulman.edu:5000/newFile",
			data: JSON.stringify(query, null, '\t'),			
			contentType: "application/json; charset=utf-8",
			success: function(data) {
				console.log("Data is: ", data);
				//loadFiles(query[0]["projectId"]);
				loadFiles(2);
			},
			error: function(data) {
				console.log("Error: ", data);
			}
		});
	}

	var loadFiles = function(projectId) {
		console.log("LOADING FILES");
		var query = [{
			"projectid": projectId
		}];

		$.ajax({
			type: "GET",
			url: "http://livecodedocs.csse.rose-hulman.edu:5000/getProjectFiles",
			data: {
				"projectid": projectId
			},
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function(data) {
				console.log(data);
				var id;
				var file_list = $("#project-files-list");
				while (file_list.children()[0])
				{
					file_list.children()[0].remove();
				}
				for (id in data) {
					var html = "<button class='list-group-item' data-id=" + id + ">" + data[id] + "</button>";
					$("#project-files-list").append(html);
				}
			},
			error: function(data) {
				console.log("Error: ", data);
			} 
		});
	}


	var sendCodeToServerHandler = function(myCodeMirror) {
		$('#runButton').on("click", function () 
		{
		var codeToRun = myCodeMirror.getDoc().getValue();
		$.ajax({
			type: "POST",
			url: "http://livecodedocs.csse.rose-hulman.edu:5000/runCode",
			data: JSON.stringify({"code": codeToRun}, null, '\t'),
			contentType: "application/json; charset-utf-8",
			success: function(data) {
				addTextToConsole(data);
			},
			error: function(data) {
				addTextToConsole(data);
			}
		});
		});
	}

	var addTextToConsole = function(text) {
		var console = document.getElementsByClassName("console")[0];
		var newDiv = document.createElement("div");
		newDiv.innerHTML = text;
		console.appendChild(newDiv);
	}

	var myCodeMirror = CodeMirror(document.getElementById('text_editor_div'), {
		lineNumbers: true,
        	extraKeys: {"Ctrl-Space": "autocomplete"},
	        mode: {name: "javascript", globalVars: true}
	});

	//TEST FOR CODEMIRROR CHANGES EVENT AND REPLACE RANGE, NOT FINAL
	var testChangeArray = [
		{
			"from": {
				"ch": 0,
				"line": 0
			},
			"to": {
				"ch": 0,
				"line": 0
			},
			"text": ["c"]
		}
	];
	var testArray = [];
	myCodeMirror.on("changes", function(myCodeMirror, changeArray) {
		testArray.push(changeArray);
		console.log(testArray);
	});
	$(".navbar-brand").on("click", function() {
		updateCodeMirror(testChangeArray, myCodeMirror);
		console.log("testChangeArray: ", testChangeArray);
	});

	var updateCodeMirror = function(testChangeArray, myCodeMirror) {
		var i;
		for (i in testChangeArray) {
			var replacement = testChangeArray[i]["text"].join("");
			var from = {
				"line": testChangeArray[i]["from"]["line"],
				"ch": testChangeArray[i]["from"]["ch"]
			};
			var to = {
				"line": testChangeArray[i]["to"]["line"],
				"ch": testChangeArray[i]["to"]["ch"] + 1
			};
			var origin = myCodeMirror.getRange(from, to);
			myCodeMirror.replaceRange(replacement, from, to, origin);
		}
	};
	//END TEST

	
	//GLOBALS
	var currentFileId = -1;
	//END GLOBALS

	sendCodeToServerHandler(myCodeMirror);
	addFilesHandler(true);
	addConsoleHandler(true);
	addEventListeners(myCodeMirror);
	loadFiles(2);

	document.getElementById('logOutButton').addEventListener("click", function () {window.location.href = "../"});
	document.getElementById('help').addEventListener("click", function () {window.location.href = "../help"});

	// var editor = CodeMirror.fromTextArea(document.getElementById("text_editor"), {
	//     // lineNumbers: true,
	//     // value: "function myScript(){return 100;}\n"
	//    	//viewportMargin: 25
	// });

});
