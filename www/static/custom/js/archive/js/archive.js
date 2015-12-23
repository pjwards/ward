/**
 * Created by donghyun on 11/14/15.
 */
/**
 * to round to n decimal places
 */
var ceil = function (num) {
    var places;

    if (num < 100) {
        places = 1;
    } else {
        places = 2;
    }

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
            data = {
                title: status,
                message: getToday(),
                color: 'danger',
            }
            notify_top_submit(1, data);
        }
    });
}

/**
 * Get Results by using async ajax
 */
var getAsyncAjaxResult = function (url, data) {
    var response = $.ajax({
        url: url,
        type: "get",
        async: false,
        data: data,
        dataType: "JSON",
    }).responseText;

    return response.includes("DoesNotExist") ? undefined : JSON.parse(response);
}

/**
 * Post by using ajax
 */
var postAjax = function (url, data) {
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: url,
        type: "post",
        data: data,
        dataType: "JSON",
        success: function (source) {
            if (source["success"]) {
                data = {
                    title: source["success"],
                    message: getToday(),
                    color: 'success',
                }
                notify_top_submit(1, data);
            }
            else if (source["error"]) {
                data = {
                    title: source["error"],
                    message: getToday(),
                    color: 'danger',
                }
                notify_top_submit(1, data);
            }
        },
        error: function (request, status, error) {
            data = {
                title: status,
                message: getToday(),
                color: 'danger',
            }
            notify_top_submit(1, data)
        }
    });
}

/**
 * Post by using async ajax
 */
var postAsyncAjax = function (url, data) {
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: url,
        type: "post",
        data: data,
        async: false,
        dataType: "JSON",
        success: function (source) {
            if (source["success"]) {
                data = {
                    title: source["success"],
                    message: getToday(),
                    color: 'success',
                }
                notify_top_submit(1, data);
            }
            else if (source["error"]) {
                data = {
                    title: source["error"],
                    message: getToday(),
                    color: 'danger',
                }
                notify_top_submit(1, data);
            }
        },
        error: function (request, status, error) {
            data = {
                title: status,
                message: getToday(),
                color: 'danger',
            }
            notify_top_submit(1, data)
        }
    });
}

/**
 * Delete by using async ajax
 */
var deleteAsyncAjax = function (url, data) {
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: url,
        type: "delete",
        data: data,
        async: false,
        dataType: "JSON",
        success: function (source) {
            if (source["success"]) {
                data = {
                    title: source["success"],
                    message: getToday(),
                    color: 'success',
                }
                notify_top_submit(1, data);
            }
            else if (source["error"]) {
                data = {
                    title: source["error"],
                    message: getToday(),
                    color: 'danger',
                }
                notify_top_submit(1, data);
            }
        },
        error: function (request, status, error) {
            data = {
                title: status,
                message: getToday(),
                color: 'danger',
            }
            notify_top_submit(1, data)
        }
    });
}

/**
 * Get url from id
 */
var getIdFromUrl = function (url) {
    var split_url = url.split('/');
    return split_url[split_url.length - 2];
}

/**
 * Post report
 */
var postReport = function (object_id) {
    var url = '/archive/report/' + object_id + '/';
    var data = {};
    postAjax(url, data);
}

/**
 * Report action
 */
var reportAction = function (report_id, action) {
    var url = '/archive/report/' + report_id + '/' + action + '/';
    var data = {};
    postAsyncAjax(url, data);
}

/**
 * Post ward
 */
var postWard = function (object_id) {
    var url = '/archive/ward/' + object_id + '/';
    var data = {};
    postAjax(url, data);
}

/**
 * Update ward
 */
var updateWard = function (ward_id, fb_url) {
    var url = '/archive/ward/' + ward_id + '/update/';
    var data = {};
    postAjax(url, data);
    window.open(fb_url, '_blank');
}

/**
 * Delete ward
 */
var deleteWard = function (ward_id) {
    var url = '/archive/ward/' + ward_id + '/';
    var data = {};
    deleteAsyncAjax(url, data);
}

/**
 * Post and comment Display
 */
var pcDisplay = function (rows, row) {
    var user_url = '/archive/user/' + getIdFromUrl(row["user"].url) + '/';
    var fb_url = "https://www.facebook.com/";
    var btn = '&nbsp; &nbsp;<a class="btn btn-block btn-social-icon btn-facebook mini" href="' + fb_url + row["id"] + '" target="_blank"><span class="fa fa-facebook"></span></a>';
    var ward_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="postWard(\'' + row["id"] + '\')" style="color:#ffa500;"><i class="icon-pin"></i></btn>';
    var report_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="postReport(\'' + row["id"] + '\')" style="color:#de615e;"><i class="icon-caution2"></i></btn>';
    var message = row["message"] ? String(row["message"]).replace(/</gi, "&lt;") : "(photo)";
    rows.push({
        "picture": '<img src="' + row["user"].picture + '" style="border-radius: 10px;">',
        "from": '<div class="more-link"><a href="' + user_url + '"><div class="h5">' + row["user"].name + '</div></a><div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(row["created_time"]) + '</small></div></div>',
        "message": message.length < 100 ? message + btn + ward_btn + report_btn : message.substring(0, 100) + "..." + btn + ward_btn + report_btn,
        "like_count": row["like_count"],
        "comment_count": row["comment_count"],
    });
}

/**
 * Post and comment Display for management
 */
var pcDisplayM = function (rows, row, name) {
    var user_url = '/archive/user/' + getIdFromUrl(row["user"].url) + '/';
    var fb_url = "https://www.facebook.com/";
    var btn = '&nbsp; &nbsp;<a class="btn btn-block btn-social-icon btn-facebook mini" href="' + fb_url + row["id"] + '" target="_blank"><span class="fa fa-facebook"></span></a>';
    var message = row["message"] ? String(row["message"]).replace(/</gi, "&lt;") : "(photo)";
    rows.push({
        "checkbox": '<input type="checkbox" name="del_' + name + '" value="' + row["id"] + '">',
        "picture": '<img src="' + row["user"].picture + '" style="border-radius: 10px;">',
        "from": '<div class="more-link"><a href="' + user_url + '"><div class="h5">' + row["user"].name + '</div></a><div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(row["created_time"]) + '</small></div></div>',
        "message": message.length < 100 ? message + btn : message.substring(0, 100) + "..." + btn,
        "like_count": row["like_count"],
        "comment_count": row["comment_count"],
    });
}

/**
 * Post and comment Display for report
 */
var pcDisplayR = function (rows, row) {
    var object = row["post"] ? row["post"] : row["comment"] ? row["comment"] : undefined;
    var user_url = '/archive/user/' + getIdFromUrl(row["user"].url) + '/';
    var group_url = '/archive/group/' + getIdFromUrl(row["group"].url) + '/';
    var fb_url = "https://www.facebook.com/";
    if (object) {
        var object_id = getIdFromUrl(object.url);
        var btn = '&nbsp; &nbsp;<a class="btn btn-block btn-social-icon btn-facebook mini" href="' + fb_url + object_id + '" target="_blank"><span class="fa fa-facebook"></span></a>';
        var message = object["message"] ? String(object["message"]).replace(/</gi, "&lt;") : "(photo)";
    }
    var checked_btn = '<btn class="btn mini" onclick="reportAction(\'' + row["id"] + '\', \'checked\'); reload()" style="color:#ffa500;">checked</btn>';
    var hide_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="reportAction(\'' + row["id"] + '\', \'hide\'); reload()" style="color:#2f4f4f;">hide</btn>';
    var show_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="reportAction(\'' + row["id"] + '\', \'show\'); reload()" style="color:#6495ed;">show</btn>';
    var delete_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="if(confirm(\'Are you sure delete?\')) reportAction(\'' + row["id"] + '\', \'delete\'); reload()" style="color:#ff1493;">deleted</btn>';
    rows.push({
        "picture": '<img src="' + row["user"].picture + '" style="border-radius: 10px;">',
        "from": '<div class="more-link"><a href="' + user_url + '"><div class="h5">' + row["user"].name + '</div></a>' + (object ? '<div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(object["created_time"]) + '</small></div></div>' : ''),
        "message": object ? message.length < 100 ? message + btn : message.substring(0, 100) + "..." + btn : 'deleted',
        "like_count": object ? object["like_count"] : 'deleted',
        "comment_count": object ? object["comment_count"] : 'deleted',
        "group": '<div class="more-link"><a href="' + group_url + '"><div class="h5">' + row["group"]["name"] + '</div></a></div>',
        "status": row["status"],
        "action": row["status"] == 'deleted' ? '' : (row["status"] == 'hide' ? show_btn : (row["status"] == 'checked' ? '' : checked_btn) + hide_btn) + delete_btn,
    });
}

/**
 * Post and comment Display for ward
 */
var pcDisplayW = function (rows, row) {
    var object = row["post"] ? row["post"] : row["comment"] ? row["comment"] : undefined;
    var user_url = '/archive/user/' + getIdFromUrl(object["user"].url) + '/';
    var object_id = getIdFromUrl(object.url);
    var fb_url = "https://www.facebook.com/";
    var new_label = row["updated_time"] < object["updated_time"] ? '<span class="label mini success">New</span> &nbsp; &nbsp;' : '';
    var btn = '&nbsp; &nbsp;<btn class="btn btn-block btn-social-icon btn-facebook mini" onclick="updateWard(' + row["id"] + ',\'' + fb_url + object_id + '\')"><span class="fa fa-facebook"></span></btn>';
    var report_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="postReport(\'' + object_id + '\')" style="color:#de615e;"><i class="icon-caution2"></i></btn>';
    var remove_ward_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="if(confirm(\'Are you sure delete?\')) deleteWard(\'' + row["id"] + '\'); reload()" style="color:#de615e;"><i class="icon-trashcan"></i></btn>'
    var message = object["message"] ? String(object["message"]).replace(/</gi, "&lt;") : "(photo)";
    rows.push({
        "picture": '<img src="' + object["user"].picture + '" style="border-radius: 10px;">',
        "from": '<div class="more-link"><a href="' + user_url + '"><div class="h5">' + object["user"].name + '</div></a><div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(object["created_time"]) + '</small></div></div>',
        "message": new_label + (message.length < 100 ? message + btn + report_btn + remove_ward_btn : message.substring(0, 100) + "..." + btn + report_btn + remove_ward_btn),
        "like_count": object["like_count"],
        "comment_count": object["comment_count"],
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
            pcDisplay(rows, results[i]);
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
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
            pcDisplay(rows, results[i]);
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
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
        var chart = jui.include("chart.builder");

        statistics = source['statistics'];
        post_max_cnt = ceil(source['post_max_cnt']);
        comment_max_cnt = ceil(source["comment_max_cnt"]);

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
        var chart = jui.include("chart.builder");

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
var getActivity = function (url, limit, model, table, loading) {

    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var user_url = '/archive/user/' + getIdFromUrl(row["user"]["url"]) + '/';

            var count = 0;
            if (model == 'post') {
                count = row["post_count"];
            } else {
                count = row["comment_count"];
            }
            rows.push({
                "picture": '<img src="' + row["user"]["picture"] + '" style="border-radius: 10px;">',
                "from": '<div class=" more-link"><a href="' + user_url + '"><div class="h5">' + row["user"]["name"] + '</div></a></div>',
                "count": count,
            });
        }
        ;

        table.reset()
        table.append(rows);
        loading.hide();
    }

    data = {
        limit: limit,
        model: model
    }

    getAjaxResult(url, data, fun);
}

/**
 * Generate Proportion
 */
var getProportion = function (url, post_display, comment_display) {
    function displayProportion(display, data) {
        var chart = jui.include("chart.builder");
        $(display).empty();
        chart(display, {
            padding: 150,
            height: 600,
            axis: {
                data: [data]
            },
            brush: {
                type: "pie",
                showText: true,
                activeEvent: "click",
            },
            widget: [{
                type: "title",
                text: "Proprotion"
            }, {
                type: "tooltip",
                orient: "left",
            }, {
                type: "legend",
            }]
        });
    }

    var fun = function (source) {
        post_proportion = source['posts'];
        comment_proportion = source['comments']

        displayProportion(post_display, post_proportion);
        displayProportion(comment_display, comment_proportion);
    };

    data = {}

    getAjaxResult(url, data, fun);
}

/**
 * Get user archive by using ajax
 */
var getUserArchive = function (url, group_id, table, limit, search, loading, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var user_url = '/archive/user/' + getIdFromUrl(row["user"]["url"]) + '/';

            rows.push({
                "picture": '<img src="' + row["user"]["picture"] + '" style="border-radius: 10px;">',
                "from": '<div class=" more-link"><a href="' + user_url + '"><div class="h5">' + row["user"]["name"] + '</div></a></div>',
                "post_count": row["post_count"],
                "comment_count": row["comment_count"],
            });
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
        loading.hide();
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
    }

    if (search) {
        data['q'] = search;
    }

    getAjaxResult(url, data, fun);
}

/**
 * Get search post and comment by using ajax
 */
var getSearchPC = function (url, table, limit, search, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            pcDisplay(rows, results[i]);
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
        q: search,
    }

    getAjaxResult(url, data, fun);
}

/**
 * Get archive for user by using ajax
 */
var getArchiveByUser = function (url, user_id, table, limit, from, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            pcDisplay(rows, results[i]);
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
    }

    if (!page) {
        page = 1;
    }

    if (!user_id) {
        return;
    }

    data = {
        user_id: user_id,
        limit: limit,
        offset: (page - 1) * limit,
        from: from,
    }

    getAjaxResult(url, data, fun);
}

/**
 * Get groups by using ajax
 */
var getGroups = function (url, table, limit, page, search, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var group_url = '/archive/group/' + row["id"] + '/';
            var privacy_btn = row["privacy"] == "CLOSED" ? 'disable' : '';
            rows.push({
                "id": '<div class=" more-link"><a href="' + group_url + '"><div class="h5">' + row["id"] + '</div></a></div>',
                "name": '<div class=" more-link"><a href="' + group_url + '"><div class="h5">' + row["name"] + '</div></a></div>',
                "updated_time": '<div class="h5"><i class="icon-realtime"></i> ' + timeSince(row["updated_time"]) + '</div>',
                "post_count": '<div class="h5">' + row["post_count"] + '</div>',
                "comment_count": '<div class="h5">' + row["comment_count"] + '</div>',
                "privacy": '<div class="h5">' + row["privacy"] + '</div>',
                "is_stored": row["is_stored"] ? '<i class="icon-check"></i>' : '<i class="icon-close"></i>',
                "update": '<a class="btn mini ' + privacy_btn + '" href="/archive/group/' + row["id"] + '/update/" style="color:#ffa500;">Update</a>',
            });
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
        q: search,
    }

    getAjaxResult(url, data, fun);
}


/**
 * Get groups admin by using ajax
 */
var getGroupsAdmin = function (url, table, limit, page, search, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var group_url = '/archive/group/' + row["id"] + '/';
            var privacy_btn = row["privacy"] == "CLOSED" ? 'disable' : '';
            var update_btn = '<a class="btn mini ' + privacy_btn + '" href="/archive/group/' + row["id"] + '/update/" style="color:#ffa500;">Update</a>';
            var store_btn = '&nbsp; &nbsp;<a class="btn mini ' + privacy_btn + '" href="/archive/group/' + row["id"] + '/store/" style="color:#6495ed;">Store</a>';
            var check_btn = '&nbsp; &nbsp;<a class="btn mini ' + privacy_btn + '" href="/archive/group/' + row["id"] + '/check/" style="color:#ff1493;">Check</a>';
            rows.push({
                "id": '<div class=" more-link"><a href="' + group_url + '"><div class="h5">' + row["id"] + '</div></a></div>',
                "name": '<div class=" more-link"><a href="' + group_url + '"><div class="h5">' + row["name"] + '</div></a></div>',
                "updated_time": '<div class="h5"><i class="icon-realtime"></i> ' + timeSince(row["updated_time"]) + '</div>',
                "post_count": '<div class="h5">' + row["post_count"] + '</div>',
                "comment_count": '<div class="h5">' + row["comment_count"] + '</div>',
                "privacy": '<div class="h5">' + row["privacy"] + '</div>',
                "is_stored": row["is_stored"] ? '<i class="icon-check"></i>' : '<i class="icon-close"></i>',
                "action": update_btn + store_btn + check_btn,
            });
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
        q: search,
    }

    getAjaxResult(url, data, fun);
}


/**
 * Generate Notify
 */
jui.ready(["ui.notify"], function (notify) {
    var handler = {
        show: function (data) {
            console.log("show : " + JSON.stringify(data));
        },
        hide: function (data) {
            console.log("hide : " + JSON.stringify(data));
        },
        click: function (data) {
            console.log("click : " + JSON.stringify(data));
        }
    };

    notify_1 = notify("body", {
        position: "top-right",
        event: handler,
        timeout: 2000,
        tpl: {
            item: $("#tpl_alarm").html()
        }
    });

    notify_2 = notify("body", {
        position: "top-left",
        event: handler,
        timeout: 2000,
        tpl: {
            item: $("#tpl_alarm").html()
        }
    });

    notify_3 = notify("body", {
        position: "top",
        event: handler,
        timeout: 2000,
        padding: {
            top: 100
        },
        tpl: {
            item: $("#tpl_alarm").html()
        }
    });

    notify_4 = notify("body", {
        position: "bottom",
        event: handler,
        timeout: 2000,
        distance: 30,
        tpl: {
            item: $("#tpl_alarm").html()
        }
    });

    notify_5 = notify("body", {
        position: "bottom-left",
        event: handler,
        timeout: 2000,
        showDuration: 1000,
        hideDuration: 1000,
        tpl: {
            item: $("#tpl_alarm").html()
        }
    });

    notify_6 = notify("body", {
        position: "bottom-right",
        event: handler,
        timeout: 2000,
        showEasing: "linear",
        tpl: {
            item: $("#tpl_alarm").html()
        }
    });

    notify_top_submit = function (type, data) {
        if (type == 1) notify_1.add(data);
        if (type == 2) notify_2.add(data);
        if (type == 3) notify_3.add(data);
        if (type == 4) notify_4.add(data);
        if (type == 5) notify_5.add(data);
        if (type == 6) notify_6.add(data);
    }
});

jui.ready(["ui.combo"], function (combo) {
    groups_combo = combo("#groups_combo", {
        index: $('#current_group').text(),
        width: 200,
        keydown: true,
        event: {
            change: function (data) {
                location.href = data.value;
            }
        }
    });
});

/**
 * Get search post and comment for management by using ajax
 */
var getSearchPCM = function (url, table, limit, model, search, search_check, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            pcDisplayM(rows, results[i], model);
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
        q: search,
        c: search_check,
    }

    getAjaxResult(url, data, fun);
}

/**
 * Get search blacklist for management by using ajax
 */
var getSearchBM = function (url, group_id, table, limit, search, page, paging) {
    var blacklist_url = "/api/groups/" + group_id + "/blacklist_user/";
    var activity_url = "/api/groups/" + group_id + "/user_archive/";

    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var user_url = '/archive/user/' + row["id"] + '/';

            var async_data = {
                user_id: row["id"]
            }
            var blacklist = getAsyncAjaxResult(blacklist_url, async_data);
            var activity = getAsyncAjaxResult(activity_url, async_data)["results"][0];

            rows.push({
                "picture": '<img src="' + row["picture"] + '" style="border-radius: 10px;">',
                "from": '<div class=" more-link"><a href="' + user_url + '"><div class="h5">' + row["name"] + '</div></a></div>',
                "count": blacklist["count"],
                "post_count": activity["post_count"],
                "comment_count": activity["comment_count"],
                "updated_time": timeSince(blacklist["updated_time"]),
            });
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
        q: search,
    }

    getAjaxResult(url, data, fun);
}

/**
 * Get search user for management by using ajax
 */
var getSearchUM2 = function (url, table, limit, search, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var user_url = '/archive/user/' + row["id"] + '/';

            var from = '<div class=" more-link"><a href="' + user_url + '"><div class="h4">' + row["name"] + '</div></a></div>';
            var id = '<div class=" more-link"><a href="' + user_url + '"><div class="h5">' + row["id"] + '</div></a></div>';
            rows.push({
                "picture": '<img src="' + row["picture"] + '" style="border-radius: 10px;">',
                "from": from + id,
                "select": '<button class="btn mini" onclick="searchUMSelect(' + row["id"] + ')"><i class="icon-pin"></i></button>'
            });
        }
        ;

        table.reset();
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
        q: search,
    }

    getAjaxResult(url, data, fun);
}

/**
 * Get reports
 */
var getReports = function (url, table, limit, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            pcDisplayR(rows, results[i]);
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
    }

    getAjaxResult(url, data, fun);
}

/**
 * Get wards
 */
var getWards = function (url, user_id, table, limit, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            pcDisplayW(rows, results[i]);
        }
        ;

        table.reset()
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.reload(source["count"]);
            paging.first();
        }
    }

    if (!user_id) {
        return;
    }

    if (!page) {
        page = 1;
    }

    data = {
        limit: limit,
        offset: (page - 1) * limit,
        user_id: user_id,
    }

    getAjaxResult(url, data, fun);
}
