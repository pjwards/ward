/**
 * Created by donghyun on 11/14/15.
 */

/**
 * Detect Inner Width For Screen Count
 *
 * @returns {number}
 */
var detectWidthToScreenCount =  function () {
    var width = window.innerWidth;
   if(width >= 1366) {
     return 10;
   } else if(width >= 800) {
     return 7;
   } else if(width >= 500) {
     return 5;
   } else if(width >= 350) {
     return 3;
   } else {
     return 1;
   }
}


/**
 * Reload paging
 *
 * @param paging
 */
var reLoadPaging = function(paging) {
    paging.setOption('screenCount', detectWidthToScreenCount());
    paging.reload(paging.options["count"]);
}

/**
 * Detect Inner Width For Substring
 *
 * @returns {number}
 */
var detectWidthToSubstring =  function () {
    var width = window.innerWidth;
   if(width >= 800) {
     return 100;
   } if(width >= 500) {
     return 50;
   }  if(width >= 350) {
     return 30;
   } else {
     return 10;
   }
}


/**
 * Get Results by using ajax
 *
 * @param url
 * @param data
 * @param fun
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
 *
 * @param url
 * @param data
 * @returns {undefined}
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
 *
 * @param url
 * @param data
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
 *
 * @param url
 * @param data
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
 *
 * @param url
 * @param data
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
 *
 * @param url
 * @returns {*}
 */
var getIdFromUrl = function (url) {
    var split_url = url.split('/');
    return split_url[split_url.length - 2];
}


/**
 * Post report
 *
 * @param object_id
 */
var postReport = function (object_id) {
    var url = '/archive/report/' + object_id + '/';
    var data = {};
    postAjax(url, data);
}


/**
 * Report action
 *
 * @param report_id
 * @param action
 */
var reportAction = function (report_id, action) {
    var url = '/archive/report/' + report_id + '/' + action + '/';
    var data = {};
    postAsyncAjax(url, data);
}


/**
 * Post ward
 *
 * @param object_id
 */
var postWard = function (object_id) {
    var url = '/archive/ward/' + object_id + '/';
    var data = {};
    postAjax(url, data);
}


/**
 * Update ward
 *
 * @param ward_id
 * @param fb_url
 */
var updateWard = function (ward_id, fb_url) {
    var url = '/archive/ward/' + ward_id + '/update/';
    var data = {};
    postAjax(url, data);
    window.open(fb_url, '_blank');
}


/**
 * Delete ward
 *
 * @param ward_id
 */
var deleteWard = function (ward_id) {
    var url = '/archive/ward/' + ward_id + '/';
    var data = {};
    deleteAsyncAjax(url, data);
}


/**
 * Post and comment Display
 *
 * @param rows
 * @param row
 */
var pcDisplay = function (rows, row) {
    var user_url = '/archive/user/' + row["user"].id + '/';
    var fb_url = "https://www.facebook.com/";
    var ward_btn = is_authenticated ? '&nbsp; &nbsp;<btn class="btn mini" onclick="postWard(\'' + row["id"] + '\')" style="color:#ffa500;"><i class="icon-pin"></i> Ward</btn>' : '';
    var report_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="if(confirm(\'Is this spam?\')) postReport(\'' + row["id"] + '\');" style="color:#de615e;"><i class="icon-caution2"></i> Report</btn>';
    var message = row["message"] ? String(row["message"]).replace(/</gi, "&lt;") : "(photo)";
    var fb_link = function (message) {
        message = message.length < detectWidthToSubstring() ? message : message.substring(0, detectWidthToSubstring()) + "...";
        return '<div class="h5"><div class="more-link" style="margin-bottom:10px;"><a href="' + fb_url + row["id"] + '" target="_blank">' + message + '</a></div>' + ward_btn + report_btn + '</div>';
    }
    rows.push({
        "picture": '<img src="' + row["user"].picture + '" style="border-radius: 10px;">',
        "from": '<div class="more-link"><a href="' + user_url + '"><div class="h5">' + row["user"].name + '</div></a><div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(row["created_time"]) + '</small></div></div>',
        "message": fb_link(message),
        "like_count": '<div class="h5">' + row["like_count"] + '</div>',
        "comment_count": '<div class="h5">' + row["comment_count"] + '</div>',
    });
}


/**
 * Post and comment Display for ward
 *
 * @param rows
 * @param row
 */
var pcDisplayW = function (rows, row) {
    var object = row["post"] ? row["post"] : row["comment"] ? row["comment"] : undefined;
    var user_url = '/archive/user/' + getIdFromUrl(object["user"].url) + '/';
    var object_id = getIdFromUrl(object.url);
    var fb_url = "https://www.facebook.com/";
    var new_label = row["updated_time"] < object["updated_time"] ? '<span class="label mini success">New</span> &nbsp; &nbsp;' : '';
    var btn = '&nbsp; &nbsp;<btn class="btn btn-block btn-social-icon btn-facebook mini" onclick="updateWard(' + row["id"] + ',\'' + fb_url + object_id + '\')"><span class="fa fa-facebook"></span></btn>';
    var report_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="if(confirm(\'Is this spam?\')) postReport(\'' + object_id + '\');" style="color:#de615e;"><i class="icon-caution2"></i></btn>';
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
            paging.setOption("count", source["count"]);
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
