$(document).ready(function(){

     $(".tab").hover(function(){
        $(this).addClass('bg-secondary');
     }, function(){
        $(this).removeClass('bg-secondary');
     });

    // when a tab is clicked
    $(".tab").click(function(){

        // get the target text area
        var targetTab;
        targetTab = $(this).attr('data-file');

        $(".tab").css('background-color', 'darkslategray');


        // hide all text areas
        $(".textarea").hide();



        // show the selected area
        $("#" + targetTab).show();
        this.style.setProperty('background-color', 'darkgray');


    });

});