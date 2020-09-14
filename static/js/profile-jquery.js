$(document).ready(function(){

    // when edit bio button clicked, show inputs
    $(document).on("click", "#editBioButton", function(){
        $("#bioEditDiv").toggle(500);
    });

    // submit bio
    $(document).on("click", "#submitBio", function(){

        var text = $("#bioTextarea").val();

        // post to django server to convert to markdown
        $.ajax({
            type: 'POST',
            url: "/question/update_profile/",
            data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    description: text},
//            dataType: "application/json; charset=utf-8",
            success: function(response){
                console.log(response);

                $("#updatedBio").html(response);
                $("#updatedBio").show();

                $("#bioText").hide();
                $(".hideOnSubmit").hide();
            }
        })
    });
});