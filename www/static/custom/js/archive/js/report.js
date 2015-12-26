/**
 * Created by donghyun on 12/26/15.
 */

/**
 * Post and comment Display for report
 *
 * @param rows
 * @param row
 */
var pcDisplayR = function (rows, row) {
    var object = row["post"] ? row["post"] : row["comment"] ? row["comment"] : undefined;
    var user_url = '/archive/user/' + row["user"].id + '/';
    var group_url = '/archive/group/' + row["group"].id + '/';
    var fb_url = "https://www.facebook.com/";
    if (object) {
        var fb_link = function (message) {
            message = message.length < detectWidthToSubstring() ? message : message.substring(0, detectWidthToSubstring()) + "...";
            return '<div class="h5"><div class="more-link" style="margin-bottom:10px;"><a href="' + fb_url + object.id + '" target="_blank">' + message + '</a></div></div>';
        }
        var message = object["message"] ? fb_link(object["message"]):'';
    }

    var checked_btn = '<btn class="btn mini" onclick="reportAction(\'' + row["id"] + '\', \'checked\'); reload()" style="color:#ffa500;">checked</btn>';
    var hide_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="reportAction(\'' + row["id"] + '\', \'hide\'); reload()" style="color:#2f4f4f;">hide</btn>';
    var show_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="reportAction(\'' + row["id"] + '\', \'show\'); reload()" style="color:#6495ed;">show</btn>';
    var delete_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="if(confirm(\'Are you sure delete?\')) reportAction(\'' + row["id"] + '\', \'delete\'); reload()" style="color:#ff1493;">deleted</btn>';
    rows.push({
        "picture": '<img src="' + row["user"].picture + '" style="border-radius: 10px;">',
        "from": '<div class="more-link"><a href="' + user_url + '"><div class="h5">' + row["user"].name + '</div></a>' + (object ? '<div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(object["created_time"]) + '</small></div></div>' : ''),
        "message": object ? message : '<div class="h5">deleted</div>',
        "like_count": '<div class="h5">' + (object ? object["like_count"] : 'deleted') + '</div>',
        "comment_count": '<div class="h5">' + (object ? object["comment_count"] : 'deleted') + '</div>',
        "group": '<div class="more-link"><a href="' + group_url + '"><div class="h5">' + row["group"]["name"] + '</div></a></div>',
        "status": '<div class="h5">' + row["status"] + '</div>',
        "action": '<div class="h5">' + (row["status"] == 'deleted' ? '' : (row["status"] == 'hide' ? show_btn : (row["status"] == 'checked' ? '' : checked_btn) + hide_btn) + delete_btn)  + '</div>',
    });
}


/**
 * Get reports
 *
 * @param url
 * @param table
 * @param limit
 * @param loading
 * @param page
 * @param paging
 */
var getReports = function (url, table, limit, loading, page, paging) {
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
            paging.setOption("count", source["count"]);
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

    getAjaxResult(url, data, fun);
}


/**
 * Change reports
 *
 * @param url
 * @param table
 * @param limit
 * @param loading
 * @param page
 * @param paging
 */
var changeReports = function (url, table, limit, loading, page, paging) {
    loading.show();
    getReports(url, table, limit, loading, page, paging);
}

