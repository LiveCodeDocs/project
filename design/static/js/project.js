//config.extraPlugins = 'CodeMirror';

$(document).ready(function() {

	var addEventListeners = function() {
		$("#new-file-add-button").on("click", function() {
			var filename = $("#new-file-name").val();
			var projectId = 2;
			addNewFile(filename, projectId);
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
			});
		} else {
			$(".console-toggle").on("click", function() {
				$(".console-toggle").css("bottom", "200px");
				$(".console").show();
				addConsoleHandler(true);
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
				loadFiles(query[0]["projectId"]);
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
				print("return from file add succeeded");
				var id;
				for (id in data) {
					var html = "<li class='list-group-item' data-id=" + id + ">" + data[id] + "</li>";
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

	//TEST FOR CODEMIRROR CHANGES EVENT. NOT FINAL
	var testArray = [];
	myCodeMirror.on("changes", function(myCodeMirror, changeArray) {
		testArray.push(changeArray);
		console.log(testArray);
	});
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
