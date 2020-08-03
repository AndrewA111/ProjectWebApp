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

});