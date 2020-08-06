var tabCount = 1;

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

//    $(".tabEdit").click(function(){
    $(document).on("click", ".tabEdit", function(){


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
        var inputName = $("#fileNameInput").val();

        // disallow spaces and append with .java if required
        var name = inputName.split(/[\s.]/)[0] + ".java"

        // get tab number
        var tabNo = $("#submitFileName").attr('data-tab');

        // identify elements
        var tabID = "#tab" + tabNo;
        var textID = tabID + "text";
        var inputID = "#id_form-" + tabNo + "-name";

        // update tab name
        $(textID).text(name);

        // update input field
        $(inputID).val(name);

        // hide the popup
        $("#popup").hide();

        // show edits buttons again
        $(".tabEdit").show();

    });

    // --- adding a new tab ---

    $("#addTab").click(function(){

        // increment tab count
        tabCount++;

        var tabName = "tab" + tabCount

        var tabTitle = "File" + tabCount + ".java";

        // clone hidden template
//        var clone = $("#tabTemplateDiv").clone().attr("id", tabName);
        var clone = $("#tabTemplateDiv").clone().attr({
                                                'id': tabName,
                                                'data-no': tabCount});

        // remove 'displayNone' to show
        clone.removeClass("displayNone");

        clone.appendTo("#tabs");



        // set IDs
        var tabText = $($("#" + tabName).find("p")[0]).attr("id", "tab" + tabCount + "text");

        var tabEdit = $($("#" + tabName).find("a")[0]).attr("id", "tab" + tabCount + "Edit");
        var tabEdit = $($("#" + tabName).find("a")[0]).attr("data-name", tabCount);

        // update tab text
        $("#tab" + tabCount + "text").text(tabTitle);

        // hide all text areas
        $(".textarea").hide();

        // add code box
        var codeClone = $("#id_form-0-contents").clone().attr("id", "id_form-" + tabCount + "-contents");
        codeClone.appendTo("#textareaholder")
        $("#id_form-" + tabCount + "-contents").attr("name", "form-" + tabCount + "-contents");
        $("#id_form-" + tabCount + "-contents").wrap("<div id='textarea" + tabCount + "' class='textarea'></div>");

        // convert textarea to codemirror display
        myTextArea = document.getElementById("id_form-" + tabCount + "-contents")
        var myCodeMirror = CodeMirror.fromTextArea(myTextArea, {
                        lineNumbers: true,
                        mode: "text/x-java",
                        autoRefresh: true,
                      });

        // add file name hidden input field
        var nameClone = $("#id_form-0-name").clone().attr("id", "id_form-" + tabCount + "-name");
        nameClone.appendTo("#hiddenInputs");
        $("#id_form-" + tabCount + "-name").val(tabTitle);
        $("#id_form-" + tabCount + "-name").attr("name", "form-" + tabCount + "-name");

        // update formset data
        $("#id_form-TOTAL_FORMS").val(tabCount + 1);


    });

    // --- tab switching ---
        // when a tab is clicked
//    $(".tab").click(function(){
    $(document).on("click", ".tab", function(){

        // get the target text area
        var targetTab;
        targetTab = $(this).attr('data-no');

        // hide all text areas
        $(".textarea").hide();

        // show the selected area
        $("#textarea" + targetTab).show();

    });

});