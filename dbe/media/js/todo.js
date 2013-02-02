$(document).ready( function() {

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // hover
    $(".progress_btns li").hover(function() {
        var progress = $(this).text();
        $(this).parents(".progress_cont").children(".progress_on").css("width", barWidth(progress));
    });

    // mouseout
    $(".progress_btns li").mouseout(function() {
        var pk = $(this).parents(".progress_btns").attr("id");
        $(this).parents(".progress_cont").children(".progress_on").css("width",
            barWidth(progress_array[pk]));
    });

    // click
    $(".progress_btns li").click(function() {
        $progress = $(this).text();
        $(this).parents(".progress_cont").children(".progress_on").css("width", barWidth($progress));
        $pk = $(this).parents(".progress_btns").attr("id");
        progress_array[$pk] = $progress;
        $.ajax({
            type: "POST",
            url: "/todo/update_item/" + $pk + "/progress/" + $progress + '/',
        })
    });


    // init progress bars
    for (var pk in progress_array) {
        $("#progress_on_"+pk).css("width", barWidth(progress_array[pk]));
    }


    // OnHold / Done toggle
    $(".toggle").click(function() {

        $action = $(this).html().indexOf("icon-on") != -1 ? "off" : "on";
        $id = $(this).attr("id");
        $pk = $id.substring(2) + '/';
        $atype = $(this).hasClass("done") ? "done/" : "onhold/";

        $.ajax({
            type: "POST",
            url: "/todo/update_item/" + $pk + $atype + $action + '/',
            success: function(action) {
                $('#' + $id).html("<img class='btn' src='/media/img/admin/icon-"
                    +$action+".gif' />");
            }
        })
    });


    function barWidth(progress) {
        progress = parseFloat(progress);
        var width = '';
        switch (progress) {
            case 0   : width = "0px"; break;
            case 10  : width = "14px"; break;
            case 20  : width = "28px"; break;
            case 30  : width = "42px"; break;
            case 40  : width = "56px"; break;
            case 50  : width = "70px"; break;
            case 60  : width = "84px"; break;
            case 70  : width = "98px"; break;
            case 80  : width = "112px"; break;
            case 90  : width = "126px"; break;
            case 100 : width = "140px"; break;
            default  : width =  "0px";
        }
        return width;
    }

});
