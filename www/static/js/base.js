$(function () {
    $(".hidden-logo").click(function () {
        $(".container").toggleClass("hidden-menu");
    })
})

$(function () {
    $("#search_input").keypress(function (event) {
        var key_code = event.keyCode || window.event.keyCode;
        if (key_code == 13) document.getElementById('search_form').submit();
    })
});

jui.ready([ "ui.dropdown" ], function(dropdown) {
    login_dropdown = dropdown("#login_dropdown", {
        event: {
            hide: function () {
                $("#login_dropdown_btn").attr('onclick', 'login_dropdown.show();');
            },
            show: function() {
                $("#login_dropdown_btn").attr('onclick', 'login_dropdown.hide();');
            },
            change: function(data) {
                location.href = data.value;
            }
        }
    });
});

/**
 * Generate Time Since
 */
var timeSince = function (date) {
    if (typeof date !== 'object') {
        date = new Date(date);
    }

    var seconds = Math.floor((new Date() - date) / 1000);
    var intervalType;

    var interval = Math.floor(seconds / 31536000);
    if (interval >= 1) {
        intervalType = 'year';
    } else {
        interval = Math.floor(seconds / 2592000);
        if (interval >= 1) {
            intervalType = 'month';
        } else {
            interval = Math.floor(seconds / 86400);
            if (interval >= 1) {
                intervalType = 'day';
            } else {
                interval = Math.floor(seconds / 3600);
                if (interval >= 1) {
                    intervalType = "hour";
                } else {
                    interval = Math.floor(seconds / 60);
                    if (interval >= 1) {
                        intervalType = "minute";
                    } else {
                        interval = seconds;
                        intervalType = "second";
                    }
                }
            }
        }
    }

    if (interval > 1 || interval === 0) {
        intervalType += 's';
    }

    return interval + ' ' + intervalType + ' ago';
};

var getToday = function () {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!

    var yyyy = today.getFullYear();
    if (dd < 10) {
        dd = '0' + dd
    }
    if (mm < 10) {
        mm = '0' + mm
    }
    return yyyy + '-' + mm + '-' + dd;
}