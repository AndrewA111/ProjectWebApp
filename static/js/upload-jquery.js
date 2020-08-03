$(document).ready(function(){

    // --- Question name input ---

    // if edit clicked, hide edit button and show input
    $("#editQName").click(function(){
        $("#editQName").hide();
        $("#qNameDiv").show();
    })

    // once input, hide input and show edit button
    $("#submitQName").click(function(){
        $("#qNameDiv").hide();
        $("#editQName").show();

        var title = $("#qNameInput").val();
        $("#questionTitle").text(title);
        $("#id_question_name").val(title);
    })

    // --- Question description input ---

    // if edit clicked, hide edit button and show input
    $("#editQDesc").click(function(){
        $("#editQDesc").hide();
        $("#qDescDiv").show();
    })

    // once input, hide input and show edit button
    $("#submitQDesc").click(function(){
        $("#qDescDiv").hide();
        $("#editQDesc").show();

        var title = $("#qDescInput").val();
        $("#questionDesc").text(title);
        $("#id_question_description").val(title);
    })

    // --- Tab functionality ---

    // when a tab is clicked
    $(".tabEdit").click(function(){

        // get the target text area
        var tabDiv = $(this).parent();

        var tabNo = $(this).attr('data-name');

        // show popup to take entry
        $("#popup").show();

        // set submit button to track which tab name is being edited
        $('#submitFileName').attr("data-tab", tabNo)

        // hide all edit buttons (only one change at a time)
        $(".tabEdit").hide();
    });

    // when a new file name is submitted
    $("#submitFileName").click(function(){

        // get the target text area
        var name = $("#fileNameInput").val();

        // get tab number
        var tabNo = $("#submitFileName").attr('data-tab');

        // identify elements
        var tabID = "#tab" + tabNo
        var textID = tabID + "text"

        // update tab name
        $(textID).text(name);

        // hide the popup
        $("#popup").hide();

        // show edits buttons again
        $(".tabEdit").show();

    });

});