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
        return 2;
    }
}


/**
 * Detect Inner Width For Page Count
 *
 * @returns {number}
 */
var detectWidthToPageCount = function () {
    var width = window.innerWidth;
    if (width >= 1366) {
        return 10;
    } else if (width >= 800) {
        return 7;
    } else {
        return 5;
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
