$(document).ready(function(){

    // on arrow button click, change order of questions appropriately
    $(document).on("click", ".arrow", function(){

        // set direction
        var direction = "up";

        if($(this).hasClass("downArrow")){
            direction = "down"
        }

        // get slug data from template variables
        const course = JSON.parse(document.getElementById("course").textContent);
        const lesson = JSON.parse(document.getElementById("lesson").textContent);

        const question = $($(this).parent().parent().parent().find("p")[0]).attr("data-slug");
        console.log(question)

         $.ajax({
            type: 'GET',
            url: "/question/courses/" + course + "/" + lesson + "/" + question + "/move/" + direction + "/",
            success: function(response){
//                var results = JSON.parse(response);

                console.log(response);

                // get updated question list from response
                var questions = response;

                for(i=0; i<questions.length; i++){

                    // update data attribute to identify
                    $("#question-" + i).attr("data-slug", questions[i].fields.slug);

                    // update link
                    $("#questionLink-" + i).attr("href", "/question/courses/" + course +
                                                "/" + lesson + "/" + questions[i].fields.slug);

                    // update question label
                    $("#questionLink-" + i).text(questions[i].fields.name);
                }
            }
        });

    })

    // on delete button click delete associate question
    $(document).on("click", ".deleteButton", function(){

        // get slug data from template variables
        const course = JSON.parse(document.getElementById("course").textContent);
        const lesson = JSON.parse(document.getElementById("lesson").textContent);

        const question = $($(this).parent().parent().find("p")[0]).attr("data-slug");
        console.log(question)

        var token = $(this).data('token');

         $.ajax({
            type: 'DELETE',
            url: "/question/courses/" + course + "/" + lesson + "/" + question + "/",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", token);
            },
            success: function(response){
//                var results = JSON.parse(response);

                console.log(response);

                var questions = response;

                if(Array.isArray(questions)){
                    // remove last row
                    $($("#question-" + (questions.length)).parent().parent().parent()).remove();

                    for(i=0; i<questions.length; i++){

                        // update data attribute to identify
                        $("#question-" + i).attr("data-slug", questions[i].fields.slug);

                        // update link
                        $("#questionLink-" + i).attr("href", "/question/courses/" + course +
                                                    "/" + lesson + "/" + questions[i].fields.slug);

                        // update question label
                        $("#questionLink-" + i).text(questions[i].fields.name);
                    }
                }
                else{
                    // remove last row
                    $($("#question-0").parent().parent().parent()).remove();
                }
            }
        });
    });
});