/**
 * Created by donghyun on 12/26/15.
 */

/**
 * Post and comment Display for ward
 *
 * @param rows
 * @param row
 */
var pcDisplayW = function (rows, row) {
    var object = row["post"] ? row["post"] : row["comment"] ? row["comment"] : undefined;
    var user_url = '/archive/user/' + object["user"].id + '/';
    var fb_url = "https://www.facebook.com/";
    var new_label = row["updated_time"] < object["updated_time"] ? '<span class="label mini success">New</span> &nbsp; &nbsp;' : '';
    var report_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="if(confirm(\'Is this spam?\')) postReport(\'' + object.id + '\');" style="color:#de615e;"><i class="icon-caution2"></i></btn>';
    var remove_ward_btn = '&nbsp; &nbsp;<btn class="btn mini" onclick="if(confirm(\'Are you sure delete?\')) deleteWard(\'' + row["id"] + '\'); reload()" style="color:#de615e;"><i class="icon-trashcan"></i></btn>'
    var message = object["message"] ? String(object["message"]).replace(/</gi, "&lt;") : "(photo)";
    var fb_link = function (message) {
        message = message.length < detectWidthToSubstring() ? message : message.substring(0, detectWidthToSubstring()) + "...";
        return '<div class="h5"><div class="more-link" style="margin-bottom:10px;">' + new_label + '<a onclick="updateWard(' + row["id"] + ',\'' + fb_url + object.id + '\')">' + message + '</a></div>' + report_btn + remove_ward_btn + '</div>';
    }
    rows.push({
        "picture": '<img src="' + object["user"].picture + '" style="border-radius: 10px;">',
        "from": '<div class="more-link"><a href="' + user_url + '"><div class="h5">' + object["user"].name + '</div></a><div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(object["created_time"]) + '</small></div></div>',
        "message": fb_link(message),
        "like_count": '<div class="h5">' + object["like_count"] + '</div>',
        "comment_count": '<div class="h5">' + object["comment_count"] + '</div>',
    });
}


/**
 * Get wards
 *
 * @param url
 * @param user_id
 * @param table
 * @param limit
 * @param loading
 * @param page
 * @param paging
 */
var getWards = function (url, user_id, table, limit, loading, page, paging) {
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
        loading.hide();
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


/**
 * Change ward
 *
 * @param url
 * @param user_id
 * @param table
 * @param limit
 * @param loading
 * @param page
 * @param paging
 */
var changeWards = function (url, user_id, table, limit, loading, page, paging) {
    loading.show();
    getWards(url, user_id, table, limit, loading, page, paging);
}
