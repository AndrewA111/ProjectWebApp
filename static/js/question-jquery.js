$(document).ready(function(){

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

        $(".tab").css('background-color', '#424242');


        // hide all text areas
        $(".textarea").hide();



        // show the selected area
        $("#" + targetTab).show();
        this.style.setProperty('background-color', '#828282');


    });

});