//config.extraPlugins = 'CodeMirror';

$(document).ready(function() {

	var addEventListeners = function(myCodeMirror) {
		$("#new-file-add-button").on("click", function() {
			var filename = $("#new-file-name").val();
			var projectId = 2;
			addNewFile(filename, projectId, myCodeMirror);
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
					currentFileId = fileId;
					if (data[id] != null) {
						myCodeMirror.setValue(data[id]);
						codeChangeArray.pop();
					} else {
						myCodeMirror.setValue("");
						codeChangeArray.pop();
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

	var addNewFile = function(filename, projectId, myCodeMirror) {
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
				//loadFiles(2);
				setEditorText(data["fileid"], myCodeMirror);
			},
			error: function(data) {
				console.log("Error: ", data);
			}
		});
	}

	var loadFiles = function(projectId) {
		console.log("LOADING FILES");
		setTimeout(function() { loadFiles(2); }, 5000);
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
	var codeChangeArray = [];
	myCodeMirror.on("changes", function(myCodeMirror, changeArray) {
		codeChangeArray.push(changeArray);
		console.log(codeChangeArray);
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
			myCodeMirror.replaceRange(replacement, from, to, "+input");
		}
	};
	
	//TODO: REPLACE WITH AJAX
	//var getCodeChanges = function() {
	//	codeChangeSocket.emit('pull_code_change', { data: currentFileId })
	//}
	var getCodeChanges = function() {
		var fileid = currentFileId;
		if (fileid == -1) {
			setTimeout(getCodeChanges, 5000);
			return;
		}
		$.ajax({
			type: "GET",
			url: "http://livecodedocs.csse.rose-hulman.edu:5000/clientPullCode",
			data: { "fileid": fileid },
			success: function(data) {
				console.log("SUCCESSFUL PULL", data);
				setTimeout(getCodeChanges, 5000);
				var cursorLocation = myCodeMirror.getCursor();
				var id;
				for (var id in data) {
					if (data[id] != null) {
						myCodeMirror.setValue(data[id]);
						myCodeMirror.setCursor(cursorLocation);
						codeChangeArray.pop();
					} else {
						myCodeMirror.setValue("");
						codeChangeArray.pop();
					}
				}
			},
			error: function(data) {
				console.log("ERROR: ", data);
			}
		});
	}
			 

	//TODO: REPLACE WITH AJAX
	var sendCodeChanges = function() {
		var testData = codeChangeArray;
		codeChangeArray = [];
		if (testData.length == 0 || currentFileId == -1) {
			setTimeout(sendCodeChanges, 5000);
			return;
		}
		$.ajax({
			type: "POST",
			url: "http://livecodedocs.csse.rose-hulman.edu:5000/updateCode",
			data: JSON.stringify({"changes": testData, "fileid": currentFileId}, null, '\t'),
			contentType: "application/json; charset-utf-8",
			success: function(data) {
				setTimeout(sendCodeChanges, 5000);
			},
			error: function(error) {
				console.log("error getting code changes: " + error);
				setTimeout(sendCodeChanges, 5000);
			}
		});
	}

	//TODO: IMPLEMENT CODE FOR THESE CALLS
	setTimeout(getCodeChanges, 5000);
	setTimeout(sendCodeChanges, 5000);
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

	//TODO: REMOVE OR UPDATE
	// var editor = CodeMirror.fromTextArea(document.getElementById("text_editor"), {
	//     // lineNumbers: true,
	//     // value: "function myScript(){return 100;}\n"
	//    	//viewportMargin: 25
	// });

});
