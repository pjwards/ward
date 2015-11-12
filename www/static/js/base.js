$(function () {
    $(".logo").click(function () {
        $(".container").toggleClass("hidden-menu");
    })
})

$(function () {
    // bind change event to select
    $('#dynamic_select').on('change', function () {
        var url = $(this).val(); // get selected value
        if (url) { // require a URL
            window.location = url; // redirect
        }
        return false;
    });
});

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

//to round to n decimal places
var ceil = function (num, places) {
    var multiplier = Math.pow(10, places);
    return Math.ceil(num / multiplier) * multiplier;
}

var getIssue = function (url, table, len, from, to) {
    var fun = function (rows) {
        table.reset()
        table.append(rows);
    }

    data = {
        len: len,
        from: from,
        to: to
    }

    getAjaxResult(url, data, fun);
}

var getArchive = function (url, table, paging, from) {
    var fun = function (rows) {
        table.reset()
        table.update(rows);
        table.resize();
        paging.reload(table.count());
    }

    data = {
        from: from,
    }

    getAjaxResult(url, data, fun);
}

var getAjaxResult = function (url, data, fun) {
    $.ajax({
        url: url,
        type: "get",
        async: false,
        data: data,
        dataType: "JSON",
        success: function (source) {
            var results = source["results"];
            var rows = []
            for (var i in results) {
                var row = results[i]
                var fb_url = "https://www.facebook.com/";
                var btn = '&nbsp; &nbsp;<a class="btn btn-block btn-social-icon btn-facebook mini" href="' + fb_url + row["id"] + '" target="_blank"><span class="fa fa-facebook"></span></a>';
                var message = row["message"] ? String(row["message"]).replace(/</gi, "&lt;") : "(photo)";
                rows.push({
                    "from": row["user"].name,
                    "created_time": timeSince(row["created_time"]),
                    "message": message.length < 80 ? message + btn : message.substring(0, 80) + "..." + btn,
                    "like_count": row["like_count"],
                    "comment_count": row["comment_count"],
                });
            }
            ;
            fun(rows);
        },
        error: function (request, status, error) {
            alert(status);
        }
    });
}
