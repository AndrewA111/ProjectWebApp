$(document).ready(function(){

    $(document).on("click", "#submitNewCourse", function(){

        // get submitted course name
        var text = $("#newCourseInput").val();

        // post new course name to server
        $.ajax({
            type: 'POST',
            url: "/question/courses/",
            data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    courseName: text},
            success: function(response){

                // if course created, update page
                if(response != "None"){

                    // get the new course object
                    var courseObj = response[0].fields

                    // clone link element and update with new details
                    var clone = $("#templateLink").first().clone().removeClass("displayNone");
                    $(clone.find("a")[0]).attr("href", "/question/courses/"+ courseObj.slug);
                    $(clone.find("a")[0]).text(courseObj.name);


                    // create an extra copy
                    cloneB = clone.clone();

                    // append both clones
                    clone.appendTo("#allCoursesHolder");
                    cloneB.appendTo("#ownerCourseHolder");
                }


            }
        })

    });

});