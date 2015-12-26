/**
 * Created by donghyun on 11/14/15.
 */

$(function () {
    $("#sidebar_select_group").change(function () {
        location.href = $("#sidebar_select_group option:selected").val();
    });
});


/**
 * Detect Inner Width For Screen Count
 *
 * @returns {number}
 */
var detectWidthToScreenCount = function () {
    var width = window.innerWidth;
    if (width >= 1366) {
        return 10;
    } else if (width >= 800) {
        return 7;
    } else if (width >= 500) {
        return 5;
    } else if (width >= 350) {
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
var reLoadPaging = function (paging) {
    paging.setOption('screenCount', detectWidthToScreenCount());
    paging.reload(paging.options["count"]);
}

/**
 * Detect Inner Width For Substring
 *
 * @returns {number}
 */
var detectWidthToSubstring = function () {
    var width = window.innerWidth;
    if (width >= 800) {
        return 100;
    }
    if (width >= 500) {
        return 50;
    }
    if (width >= 350) {
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
