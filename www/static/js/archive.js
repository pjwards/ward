/**
 * Created by donghyun on 11/14/15.
 */

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

/**
 * to round to n decimal places
 */
var ceil = function (num, places) {
    var multiplier = Math.pow(10, places);
    return Math.ceil(num / multiplier) * multiplier;
}

/**
 * Get Results by using ajax
 */
var getAjaxResult = function (url, data, fun) {
    $.ajax({
        url: url,
        type: "get",
        data: data,
        dataType: "JSON",
        success: function (source) {
            fun(source);
        },
        error: function (request, status, error) {
            alert(status);
        }
    });
}

/**
 * Get issue by using ajax
 */
var getIssue = function (url, table, limit, from, to, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var picture = '<div class="col col-6"><div class="timeline-badge" align="middle"><img src="' + row["user"]["picture"] + '" style="border-radius: 10px;"></div></div>';
            var from = '<div class="col col-6" style="padding-top: 5px;"><div class="h5">' + row["user"].name + '</div><div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(row["created_time"]) + '</small></div></div>';
            var fb_url = "https://www.facebook.com/";
            var btn = '&nbsp; &nbsp;<a class="btn btn-block btn-social-icon btn-facebook mini" href="' + fb_url + row["id"] + '" target="_blank"><span class="fa fa-facebook"></span></a>';
            var message = row["message"] ? String(row["message"]).replace(/</gi, "&lt;") : "(photo)";
            rows.push({
                "from": picture + from,
                "message": message.length < 80 ? message + btn : message.substring(0, 80) + "..." + btn,
                "like_count": row["like_count"],
                "comment_count": row["comment_count"],
            });
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
        }
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
        from: from,
        to: to,
    }

    getAjaxResult(url, data, fun);
}

/**
 * Get archive by using ajax
 */
var getArchive = function (url, table, limit, from, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var picture = '<div class="col col-6"><div class="timeline-badge" align="middle"><img src="' + row["user"]["picture"] + '" style="border-radius: 10px;"></div></div>';
            var from = '<div class="col col-6" style="padding-top: 5px;"><div class="h5">' + row["user"].name + '</div><div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(row["created_time"]) + '</small></div></div>';
            var fb_url = "https://www.facebook.com/";
            var btn = '&nbsp; &nbsp;<a class="btn btn-block btn-social-icon btn-facebook mini" href="' + fb_url + row["id"] + '" target="_blank"><span class="fa fa-facebook"></span></a>';
            var message = row["message"] ? String(row["message"]).replace(/</gi, "&lt;") : "(photo)";
            rows.push({
                "from": picture + from,
                "message": message.length < 80 ? message + btn : message.substring(0, 80) + "..." + btn,
                "like_count": row["like_count"],
                "comment_count": row["comment_count"],
            });
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
        }
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
        from: from,
    }

    getAjaxResult(url, data, fun);
}

/**
 * Generate Statistics
 */
var getStatistics = function (url, display, method, from, to) {
    var statistics;
    var post_max_cnt;
    var comment_max_cnt;

    var fun = function (source) {
        statistics = source['statistics'];
        post_max_cnt = ceil(source['post_max_cnt'], 2);
        comment_max_cnt = ceil(source["comment_max_cnt"], 2);

        $(display).empty();
        chart(display, {
            padding: {
                left: 60
            },
            height: 400,
            axis: [{
                data: statistics,
                x: {
                    type: "block",
                    domain: "date"
                },
                y: {
                    type: "range",
                    domain: [0, post_max_cnt],
                    step: 4,
                    line: true
                },
                area: {
                    width: "100%",
                    height: "100%"
                }
            }, {
                x: {
                    hide: true
                },
                y: {
                    domain: [0, comment_max_cnt],
                    orient: "right"
                },
                area: {
                    width: "100%",
                    height: "100%"
                },
                extend: 0
            }],
            brush: [{
                type: "column",
                target: "posts",
                axis: 0,
                colors: [0],
                animate: true
            }, {
                type: "line",
                target: "comments",
                axis: 1,
                colors: [2],
                animate: true
            }, {
                type: "scatter",
                target: "comments",
                size: 10,
                axis: 1,
                colors: [2]
            }],
            widget: [{
                type: "title",
                text: "Group Overview",
                align: "start"
            }, {
                type: "title",
                text: "Counts",
                align: "start",
                orient: "center",
                dx: -55,
                dy: -90
            }, {
                type: "tooltip",
                format: function (k, v) {
                    return v;
                },
                brush: [0, 2, 3, 4]
            }],
            style: {
                scatterBorderWidth: 1.5,
                titleFontSize: "11px",
                titleFontWeight: "bold"
            },
            format: function (v) {
                if (typeof(v) == "number") {
                    return ((v > 1000) ? Math.floor(v / 1000) + "k" : v);
                }
                return v;
            }
        });
    }

    method = typeof method !== 'undefined' ? method : "month";

    data = {
        method: method,
        from: from,
        to: to
    }

    getAjaxResult(url, data, fun);
}

/**
 * Generate Hour Total Statistics
 */
var getHourTotalStatistics = function (url, display, from, to) {
    var hour_statistics;

    var fun = function (source) {
        hour_statistics = source['statistics'];
        for (var i in hour_statistics) {
            delete hour_statistics[i].date;
        }

        $(display).empty();
        chart(display, {
            height: 350,
            axis: {
                x: {
                    type: "fullblock",
                    domain: ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"],
                    line: true
                },
                y: {
                    type: "range",
                    domain: function (d) {
                        return Math.max(d.posts, d.comments);
                    },
                    step: 10
                },
                data: hour_statistics
            },
            brush: {
                type: "line",
                display: "max",
                active: "posts",
                activeEvent: "click"
            },
            widget: [
                {type: "title", text: "Time Overview"},
                {type: "legend"}
            ]
        });
    }

    data = {
        method: "hour_total",
        from: from,
        to: to
    }

    getAjaxResult(url, data, fun);
}

/**
 * Get active by using ajax
 */
var getActivity = function (url, limit, method, model, table) {

    var fun = function (source) {
        console.dir(source);

        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var picture = '<div class="col col-6"><div class="timeline-badge" align="middle"><img src="' + row["picture"] + '" style="border-radius: 10px;"></div></div>';
            var from = '<div class="col col-6" style="padding-top: 5px;"><div class="h5">' + row["name"] + '</div></div>';
            rows.push({
                "picture": '<img src="' + row["picture"] + '" style="border-radius: 10px;">',
                "from": row["name"],
                "count": row["count"],
            });
        }
        ;

        table.reset()
        table.append(rows);
    }

    data = {
        limit: limit,
        method: method,
        model: model
    }

    getAjaxResult(url, data, fun);
}
