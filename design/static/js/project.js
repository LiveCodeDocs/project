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
			dataType: "json",
			success: function(data) {
				console.log(data);
				loadFiles(query[0]["projectId"]);
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
			data: JSON.stringify(query, null, '\t'),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function(data) {
				console.log(data);
			}
		});
	}

	addFilesHandler(true);
	addConsoleHandler(true);
	addEventListeners();
	loadFiles(2);
});