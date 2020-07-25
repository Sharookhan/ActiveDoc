$(document).ready(function()
{
    $.ajax({
        type: "POST",
        url: "/welcome",
        cache: false,
        context:this,     
        success: function(data){
            $('#print_all').html("<b>Active users :</b> "+data);
          }
    });

    setInterval(function () {
    
       $.ajax({
            type: "POST",
            url: "/welcome",
            cache: false,
            context:this,     
            success: function(data){
                $('#print_all').html("<b>Active users :</b> "+data);
              }
        });

    },10000);
});