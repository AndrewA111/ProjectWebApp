$(document).ready(function(){

    // on delete button click delete associated course
    $(document).on("click", ".deleteButton", function(){

        // get course slug
        const course = $($(this).parent().parent().find("p")[0]).attr("data-slug");

        // csrf token
        var token = $(this).data('token');

         $.ajax({
            type: 'DELETE',
            url: "/question/courses/" + course + "/",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", token);
            },
            success: function(response){

                console.log(response)

                $($("#myCourse-" + (course)).parent().parent().parent()).remove();
                $($("#course-" + (course)).parent().parent()).remove();
            }
         });
    });
});