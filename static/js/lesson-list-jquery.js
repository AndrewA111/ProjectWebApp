$(document).ready(function(){

    $(document).on("click", ".arrow", function(){

        // set direction
        var direction = "up";

        if($(this).hasClass("downArrow")){
            direction = "down"
        }

        // get slug data from template variables
        const course = JSON.parse(document.getElementById("course").textContent);
        const lesson = $($(this).parent().parent().parent().find("p")[0]).attr("data-slug");

        $.ajax({
            type: 'GET',
            url: "/question/courses/" + course + "/" + lesson + "/move/" + direction + "/",
            success: function(response){

                // get updated lesson list from response
                var lessons = response;

                for(i=0; i<lessons.length; i++){

                    // update data attribute to identify
                    $("#lesson-" + i).attr("data-slug", lessons[i].fields.slug);

                    // update link
                    $("#lessonLink-" + i).attr("href", "/question/courses/" + course +
                                                "/" + lessons[i].fields.slug);

                    // update question label
                    $("#lessonLink-" + i).text(lessons[i].fields.name);
                }

            }

        });

    });


    $(document).on("click", ".deleteButton", function(){

        // get slug data from template variables
        const course = JSON.parse(document.getElementById("course").textContent);
        const lesson = $($(this).parent().parent().find("p")[0]).attr("data-slug");

        // csrf token
        var token = $(this).data('token');

        $.ajax({
            type: 'DELETE',
            url: "/question/courses/" + course + "/" + lesson + "/",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", token);
            },
            success: function(response){

                console.log(response);

                var lessons = response;

                // check that array has been returned
                if(Array.isArray(lessons)){

                    // remove last row
                    $($("#lesson-" + (lessons.length)).parent().parent().parent()).remove();

                    for(i=0; i<lessons.length; i++){

                        // update data attribute to identify
                        $("#lesson-" + i).attr("data-slug", lessons[i].fields.slug);

                        // update link
                        $("#lessonLink-" + i).attr("href", "/question/courses/" + course +
                                                    "/" + lessons[i].fields.slug);

                        // update question label
                        $("#lessonLink-" + i).text(lessons[i].fields.name);
                    }
                }
                // else no array returned, remove last row to leave empty
                else{
                    // remove last row
                    $($("#lesson-0").parent().parent().parent()).remove();
                }


            }
        });
    });



});