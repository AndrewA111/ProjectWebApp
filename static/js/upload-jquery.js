var tabCount;

$(document).ready(function(){

    // function to submit AJAX request for test results
    $("#upload").click(function(){

        $("#upload").hide();
        $("#spinner").show();

        // get slug data from template variables
        const course = JSON.parse(document.getElementById("course").textContent);
        const lesson = JSON.parse(document.getElementById("lesson").textContent);
        console.log(course);
        console.log(lesson);

        // save CodeMirror instances
        // (update associated textbox for submission)
        for (i = 0; i < codeMirrorInstances.length; i++){
            codeMirrorInstances[i].save();
        }

        // get form data as JSON
        var formData = $("#submission_form").serialize();

        // post to django server
        $.ajax({
            type: 'POST',
            url: "/question/courses/" + course + "/" + lesson + "/" +"create_question/ajax_upload/",
            data: formData,
            success: function(response){

                // for testing
//                alert(response);


                // results available, show output
                $(".testOutput").show();

                // parse results to object
                var results = JSON.parse(response);
                console.log(results);

                // get output sub-object
                var output = results.output;
                // console.log("Output: " + output)

                // if errors are returned, display then
                if(results.errors != ''){

                    // hide results area
                    $(".testOutput").hide();

                    // show errors
                    $("#errorText").text(results.errors);
                    $(".testErrors").show();

                    // reset buttons
                    $("#upload").show();
                    $("#spinner").hide();

                    // error message
                    $("#messagePopupTitle").text("Invalid upload");
                    $("#messagePopupText").text("All files including tests must compile without errors.");
                    $("#messagePopup").show();
                }
                // else display returned results
                else{

                    // clear any old errors
                    $("#errorText").empty();
                    $(".testErrors").hide();

                    // try to parse output and display
                    try{
                        // empty any old test results
                        $("#output").empty();

                        // loop through results and add results boxes to the DOM
                        for(var i = 0; i < output['tests'].length; i++){

                            // get test info
                            var name = output['tests'][i]['name'];
                            var description = output['tests'][i]['description'];
                            var hint = output['tests'][i]['hint'];
                            var passed = output['tests'][i]['passed'];
                            var failure = output['tests'][i]['failureText'];



                            // clone hidden test template
                            var clone = $("#testTemplate").clone().attr({'id': "test" + name});
                            clone.appendTo("#output");

                            // fill new test template fields
                            $($("#test" + name).find("h6")[0]).attr("id", "test" + name + "Name");
                            $("#test" + name + "Name").text(name);

                            $($("#test" + name).find("p")[0]).attr("id", "test" + name + "Description");
                            $("#test" + name + "Description").text(description);

                            $($("#test" + name).find("p")[1]).attr("id", "test" + name + "Result");
                            $("#test" + name + "Result").text(passed);

                            $($("#test" + name).find("p")[2]).attr("id", "test" + name + "Failure");
                            $("#test" + name + "Failure").text(failure);

                            // check if hint given
                            if(hint != null){

                                // populate hint text
                                $($("#test" + name).find("p")[3]).attr("id", "test" + name + "Hint");
                                $("#test" + name + "Hint").text(hint);

                                // show hint toggle button
                                $($("#test" + name).find(".hintButtonContainer")[0]).show();
                            }

                            $($("#test" + name).show());

                            // show output section
                            $(".testOutput").show();

                        }

                        if(results.summaryCode == 1){
//                                alert("Upload valid. Now solve to verify.");

                                // switch UI to allow user to solve question
                                $(".edit").hide();
                                $("#upload").hide();
                                $("#spinner").hide();
                                $('#solve').show();

                                // show first file
                                $(".textarea").hide();
                                $("#textarea1").show();

                                // popup text
                                $("#messagePopupTitle").text("Draft question uploaded.");
                                $("#messagePopupText").text("Solve question to verify.");
                                $("#messagePopup").show();
                        } else{
                            $("#upload").show();
                            $("#spinner").hide();

                            $("#messagePopupTitle").text("Invalid upload");

                            // if some tests are passing
                            if(results.summaryCode == 0 || results.summaryCode == 2){
                                $("#messagePopupText").text("All tests must fail by default.");
                            }
                            // if no tests provided
                            else if(results.summaryCode == 3){
                                $("#messagePopupText").text("No tests provided.");
                            }
                            // if question name already taken
                            else if(results.summaryCode == 4){
                                $("#messagePopupText").text("Question name unavailable.");
                            }
                            $("#messagePopup").show();
                        }
                    } catch(e){
                        // output could not be parsed and displayed
                        console.log("Error loading output JSON");
                        console.log(e);
                    }
                }

            }
        });

    })

    $("#closeMessagePopup").click(function(){
        $("#messagePopup").hide();
    })

    $("#solve").click(function(){

        $("#solve").hide();
        $("#spinner").show();

        // get slug data from template variables
        const course = JSON.parse(document.getElementById("course").textContent);
        const lesson = JSON.parse(document.getElementById("lesson").textContent);
        console.log(course);
        console.log(lesson);

        // save CodeMirror instances
        // (update associated textbox for submission)
        for (i = 0; i < codeMirrorInstances.length; i++){
            codeMirrorInstances[i].save();
        }

        // get form data as JSON
        var formData = $("#submission_form").serialize();

        // post to django server
        $.ajax({
            type: 'POST',
            url: "/question/courses/" + course + "/" + lesson + "/" +"create_question/ajax_solve/",
            data: formData,
            success: function(response){
                 // results available, show output
                $(".testOutput").show();

                // parse results to object
                var results = JSON.parse(response);
                console.log(results);

                // get output sub-object
                var output = results.output;
                // console.log("Output: " + output)

                console.log("test");
                console.log(results.errors);

                // if errors are returned, display then
                if(results.errors != ''){

                    // hide results area
                    $(".testOutput").hide();

                    // reset buttons
                    $('#solve').show();
                    $("#spinner").hide();

                    // show errors
                    $("#errorText").text(results.errors);
                    $(".testErrors").show();
                }
                // else display returned results
                else{

                    // clear any old errors
                    $("#errorText").empty();
                    $(".testErrors").hide();

                    // try to parse output and display
                    try{
                        // empty any old test results
                        $("#output").empty();

                        // loop through results and add results boxes to the DOM
                        for(var i = 0; i < output['tests'].length; i++){

                            // get test info
                            var name = output['tests'][i]['name'];
                            var description = output['tests'][i]['description'];
                            var hint = output['tests'][i]['hint'];
                            var passed = output['tests'][i]['passed'];
                            var failure = output['tests'][i]['failureText'];



                            // clone hidden test template
                            var clone = $("#testTemplate").clone().attr({'id': "test" + name});
                            clone.appendTo("#output");

                            // fill new test template fields
                            $($("#test" + name).find("h6")[0]).attr("id", "test" + name + "Name");
                            $("#test" + name + "Name").text(name);

                            $($("#test" + name).find("p")[0]).attr("id", "test" + name + "Description");
                            $("#test" + name + "Description").text(description);

                            $($("#test" + name).find("p")[1]).attr("id", "test" + name + "Result");
                            $("#test" + name + "Result").text(passed);

                            $($("#test" + name).find("p")[2]).attr("id", "test" + name + "Failure");
                            $("#test" + name + "Failure").text(failure);

                            // check if hint given
                            if(hint != null){

                                // populate hint text
                                $($("#test" + name).find("p")[3]).attr("id", "test" + name + "Hint");
                                $("#test" + name + "Hint").text(hint);

                                // show hint toggle button
                                $($("#test" + name).find(".hintButtonContainer")[0]).show();
                            }

                            $($("#test" + name).show());

                            // show output section
                            $(".testOutput").show();

                        }

                        if(results.summaryCode == 0){
                        // popup text
                            $("#messagePopupTitle").text("Solved.");
                            $("#messagePopupText").text("Question has now been verified.");
                            $("#messagePopup").show();
                            $("#spinner").hide();
//                                alert("Upload solved.");
                        }
                        else{
                            $("#messagePopupTitle").text("Unsuccessful.");
                            $("#messagePopupText").text("Solution must pass all tests to verify question.");
                            $("#messagePopup").show();
                            $("#spinner").hide();
                            $('#solve').show();
                        }
                    } catch(e){
                        // output could not be parsed and displayed
                        console.log("Error loading output JSON")
                    }
                }
            }

        })
    });



    // set tab count based on number of forms
    // (-1 for hidden form)
    tabCount = $("#id_form-TOTAL_FORMS").val() - 1

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

        var desc = $("#qDescInput").val();

        // post to django server to convert to markdown
        $.ajax({
            type: 'POST',
            url: "/question/markdown_convert/",
            data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    description: desc},
//            dataType: "application/json; charset=utf-8",
            success: function(response){
                console.log(response);
                $("#questionDesc").html(response);
                $("#id_question_description").val(desc);
            }
        })
    });

    // --- Tab functionality ---

    // when edit button clicked
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
        var clone = $("#tabTemplateDiv").clone().attr({
                                                'id': tabName,
                                                'data-no': tabCount});

        // remove 'displayNone' to show
        clone.removeClass("displayNone");

        // add to DOM
        clone.appendTo("#tabs");

        $($("#" + tabName).find(".tabBox")[0]).attr("data-no", tabCount);

        // set IDs
        var tabText = $($("#" + tabName).find("p")[0]).attr("id", "tab" + tabCount + "text");

        var tabEdit = $($("#" + tabName).find("a")[0]).attr("id", "tab" + tabCount + "Edit");
        var tabEdit = $($("#" + tabName).find("a")[0]).attr("data-name", tabCount);

        var tabDelete = $($("#" + tabName).find("a")[1]).attr("id", "tab" + tabCount + "Delete");
        var tabDelete = $($("#" + tabName).find("a")[1]).attr("data-name", tabCount);

        // update tab text
        $("#tab" + tabCount + "text").text(tabTitle);

        // hide all text areas
        $(".textarea").hide();

        // add code box
        var codeClone = $("#id_form-0-contents").clone().attr("id", "id_form-" + tabCount + "-contents");
        codeClone.appendTo("#textareaholder")
        $("#id_form-" + tabCount + "-contents").attr("name", "form-" + tabCount + "-contents");
        $("#id_form-" + tabCount + "-contents").wrap("<div id='textarea" + tabCount + "' class='textarea fill100'></div>");

        // convert textarea to codemirror display
        myTextArea = document.getElementById("id_form-" + tabCount + "-contents");
        myCodeMirror = CodeMirror.fromTextArea(myTextArea, {
                        lineNumbers: true,
                        mode: "text/x-java",
                        autoRefresh: true,
                      });
        myCodeMirror.setSize("100%", "100%");
        codeMirrorInstances.push(myCodeMirror);

        // add file name hidden input field
        var nameClone = $("#id_form-0-name").clone().attr("id", "id_form-" + tabCount + "-name");
        nameClone.appendTo("#hiddenInputs");
        $("#id_form-" + tabCount + "-name").val(tabTitle);
        $("#id_form-" + tabCount + "-name").attr("name", "form-" + tabCount + "-name");

        // add delete checkbox hidden input field
        var boxClone = $("#id_form-0-DELETE").clone().attr("id", "id_form-" + tabCount + "-DELETE");
        console.log(boxClone);
        boxClone.appendTo("#hiddenInputs");
        $("#id_form-" + tabCount + "-DELETE").attr("name", "form-" + tabCount + "-DELETE");

        // update formset data
        $("#id_form-TOTAL_FORMS").val(tabCount + 1);

        for (i = 0; i < codeMirrorInstances.length; i++){
            codeMirrorInstances[i].refresh();
        }


    });

    // --- tab switching ---

    // when a tab is clicked
    $(document).on("click", ".tab", function(){

        // get the target text area
        var targetTab;
        targetTab = $(this).attr('data-no');

        // hide all text areas
        $(".textarea").hide();

        // show the selected area
        $("#textarea" + targetTab).show();

        // refresh codemirror instances
        for (i = 0; i < codeMirrorInstances.length; i++){
            codeMirrorInstances[i].refresh();
        }
    });

    // --- tab deleting ---

    // when delete button clicked
    $(document).on("click", ".tabDelete", function(){

        // get tab number
        var tabNo = $(this).attr('data-name');

        // mark hidden field to inform backend not to process the file
        $("#id_form-" + tabNo + "-DELETE").prop("checked", true);

        // hide all text areas
        $("#tab" + tabNo).hide();

        // hide all text areas
        $(".textarea").hide();

        // show the Test file textarea
        $("#textareaTest").show();

        // refresh codemirror instances
        for (i = 0; i < codeMirrorInstances.length; i++){
            codeMirrorInstances[i].refresh();
        }

    });


    // when a 'hint' button is clicked
    $(document).on("click", ".hintButton", function(){

        $($(this).parent().parent().parent().parent().parent().find(".hint")[0]).toggle(500);

    });


});