$(document).ready(function(){

    $(document).on("click", ".arrow", function(){
//    $(".upArrow").click(function(){

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



});