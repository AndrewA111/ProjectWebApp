$(document).ready(function(){

    $("#ajaxSubmit").click(function(){

        $("#ajaxSubmit").hide();
        $("#spinner").show();

        // get slug data from template variables
        const course = JSON.parse(document.getElementById("course").textContent);
        const lesson = JSON.parse(document.getElementById("lesson").textContent);
        const question_slug = JSON.parse(document.getElementById("question_slug").textContent);
//        console.log(course);
//        console.log(lesson);
//        console.log(question_slug);

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
            url: "/question/courses/" + course + "/" + lesson + "/" + question_slug + "/ajax/",
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

                    // show errors
                    $("#errorText").text(results.errors);
                    $(".testErrors").show();

                    // reset buttons
                    $("#spinner").hide();
                    $('#ajaxSubmit').show();
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

                            console.log(i);

                            // get test info
                            var name = output['tests'][i]['name'];
                            var description = output['tests'][i]['description'];
                            var hint = output['tests'][i]['hint'];
                            var passed = output['tests'][i]['passed'];
                            var failure = output['tests'][i]['failureText'];

                            console.log(name);



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

//                        if(results.summaryCode == 0){
//                        // popup text
//                            $("#messagePopupTitle").text("Solved.");
//                            $("#messagePopupText").text("Question has now been verified.");
//                            $("#messagePopup").show();
//                            $("#spinner").hide();
////                                alert("Upload solved.");
//                        }
//                        else{
//                            $("#messagePopupTitle").text("Unsuccessful.");
//                            $("#messagePopupText").text("Solution must pass all tests to verify question.");
//                            $("#messagePopup").show();
//                            $("#spinner").hide();
//                            $('#solve').show();
//                        }
                    } catch(e){
                        // output could not be parsed and displayed
                        console.log("Error loading output JSON")
                    }
                    $("#spinner").hide();
                    $('#ajaxSubmit').show();
                }
            }

        })
    });

     $(".tab").hover(function(){
        $(this).addClass('highlightGray');
     }, function(){
        $(this).removeClass('highlightGray');
     });

    // when a tab is clicked
    $(".tab").click(function(){

        // get the target text area
        var targetTab;
        targetTab = $(this).attr('data-file');

        // hide all text areas
        $(".textarea").hide();

        // show the selected area
        $("#" + targetTab).show();

        // highlighting
        $(".tab").css('background-color', '#6C757D');
        this.style.setProperty('background-color', '#424242');

        // focus on codemirror to force refresh
        $("#" + targetTab + " .CodeMirror").focus();

    });

    // when a 'hint' button is clicked
    $(document).on("click", ".hintButton", function(){

        $($(this).parent().parent().parent().parent().parent().find(".hint")[0]).toggle(500);

    });

    // -- bookmark functionality --

    $(".bookmark").click(function(){

         // get slug data from template variables
        const course = JSON.parse(document.getElementById("course").textContent);
        const lesson = JSON.parse(document.getElementById("lesson").textContent);
        const question_slug = JSON.parse(document.getElementById("question_slug").textContent);

        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        // post to django server
        $.ajax({
            type: 'POST',
            url: "/question/courses/" + course + "/" + lesson + "/" + question_slug + "/bookmark/",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", token);
            },
            success: function(response){
                $(".bookmark").hide();
                $(".unbookmark").show();
            }

        });
    });

    $(".unbookmark").click(function(){

         // get slug data from template variables
        const course = JSON.parse(document.getElementById("course").textContent);
        const lesson = JSON.parse(document.getElementById("lesson").textContent);
        const question_slug = JSON.parse(document.getElementById("question_slug").textContent);

        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        // post to django server
        $.ajax({
            type: 'DELETE',
            url: "/question/courses/" + course + "/" + lesson + "/" + question_slug + "/bookmark/",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", token);
            },
            success: function(response){
                $(".unbookmark").hide();
                $(".bookmark").show();
            }

        });
    });

});