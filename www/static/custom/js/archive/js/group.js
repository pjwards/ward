/**
 * Created by donghyun on 12/26/15.
 */

/**
 * Get groups by using ajax
 *
 * @param url
 * @param table
 * @param limit
 * @param search
 * @param loading
 * @param page
 * @param paging
 */
var getGroups = function (url, table, limit, search, loading, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var group_url = '/archive/group/' + row["id"] + '/';
            var owner = '<div class="h4">Empty</div>'
            if(row["owner"]) {
                var owner_url = '/archive/user/' + row["owner"]["id"] + '/';
                owner = '<div class="more-link"><a href="' + owner_url + '"><div class="h4">' + row["owner"]["name"] + '</div></a></div>';
            }
            var is_stored = row["is_stored"] ? '<i class="icon-check"></i>' : '<i class="icon-close"></i>';
            rows.push({
                "name": '<div class=" more-link"><a href="' + group_url + '"><div class="h4">' + row["name"] + '</div></a></div>',
                "updated_time": '<div class="h4"><i class="icon-realtime"></i> ' + timeSince(row["updated_time"]) + '</div>',
                "post_count": '<div class="h4">' + row["post_count"] + '</div>',
                "comment_count": '<div class="h4">' + row["comment_count"] + '</div>',
                "owner": owner,
                "is_stored": '<div class="h4">' + is_stored + '</div>',
                "action": '<a class="btn mini" href="/archive/group/' + row["id"] + '/update/" style="color:#ffa500;">Update</a>',
            });
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
        q: search,
    }

    getAjaxResult(url, data, fun);
}


/**
 * Change groups list
 *
 * @param url
 * @param table
 * @param limit
 * @param search
 * @param loading
 * @param page
 * @param paging
 */
var changeGroups = function (url, table, limit, search, loading, page, paging) {
    loading.show();
    getGroups(url, table, limit, search, loading, page, paging);
}


/**
 * Get groups admin by using ajax
 *
 * @param url
 * @param table
 * @param limit
 * @param search
 * @param loading
 * @param page
 * @param paging
 */
var getGroupsAdmin = function (url, table, limit, search, loading, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var group_url = '/archive/group/' + row["id"] + '/';
            var owner = '<div class="h4">Empty</div>'
            if(row["owner"]) {
                var owner_url = '/archive/user/' + row["owner"]["id"] + '/';
                owner = '<div class="more-link"><a href="' + owner_url + '"><div class="h4">' + row["owner"]["name"] + '</div></a></div>';
            }
            var is_stored = row["is_stored"] ? '<i class="icon-check"></i>' : '<i class="icon-close"></i>';
            var update_btn = '<a class="btn mini" href="/archive/group/' + row["id"] + '/update/" style="color:#ffa500;">Update</a>';
            var store_btn = '&nbsp; &nbsp;<a class="btn mini" href="/archive/group/' + row["id"] + '/store/" style="color:#6495ed;">Store</a>';
            var check_btn = '&nbsp; &nbsp;<a class="btn mini" href="/archive/group/' + row["id"] + '/check/" style="color:#ff1493;">Check</a>';
            rows.push({
                "name": '<div class=" more-link"><a href="' + group_url + '"><div class="h4">' + row["name"] + '</div></a></div>',
                "updated_time": '<div class="h4"><i class="icon-realtime"></i> ' + timeSince(row["updated_time"]) + '</div>',
                "post_count": '<div class="h4">' + row["post_count"] + '</div>',
                "comment_count": '<div class="h4">' + row["comment_count"] + '</div>',
                "owner": owner,
                "is_stored": '<div class="h4">' + is_stored + '</div>',
                "action": update_btn + store_btn + check_btn,
            });
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
        q: search,
    }

    getAjaxResult(url, data, fun);
}


/**
 * Change groups list for admin
 *
 * @param url
 * @param table
 * @param limit
 * @param search
 * @param loading
 * @param page
 * @param paging
 */
var changeGroupsAdmin = function (url, table, limit, search, loading, page, paging) {
    loading.show();
    getGroupsAdmin(url, table, limit, search, loading, page, paging);
}