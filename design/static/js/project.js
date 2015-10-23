$(document).ready(function() {

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
	addFilesHandler(false);
	addConsoleHandler(false);

	document.getElementById('logOutButton').addEventListener("click", function () {window.location.href = "../templates/HomePage.html"});
	document.getElementById('help').addEventListener("click", function () {window.location.href = "../templates/Help.html"});

	// var editor = CodeMirror.fromTextArea(document.getElementById("text_editor"), {
	//     // lineNumbers: true,
	//     // value: "function myScript(){return 100;}\n"
	//    	//viewportMargin: 25
	// });

}

);

