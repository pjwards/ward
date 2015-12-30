/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2015 pjwards.com
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 * ==================================================================================
 *
 * Provides functions for management page
 */

/**
 * Post and comment Display for management
 *
 * @param rows
 * @param row
 * @param name
 */
var pcDisplayM = function (rows, row, name) {
    var user_url = '/archive/user/' + row["user"].id + '/';
    var fb_url = "https://www.facebook.com/";
    var message = row["message"] ? String(row["message"]).replace(/</gi, "&lt;") : "(photo)";
    var fb_link = function (message) {
        message = message.length < detectWidthToSubstring() ? message : message.substring(0, detectWidthToSubstring()) + "...";
        return '<div class="h5"><div class="more-link"><a href="' + fb_url + row["id"] + '" target="_blank">' + message + '</a></div></div>';
    }
    rows.push({
        "checkbox": '<input type="checkbox" name="del_' + name + '" value="' + row["id"] + '">',
        "picture": '<img src="' + row["user"].picture + '" style="border-radius: 10px;">',
        "from": '<div class="more-link"><a href="' + user_url + '"><div class="h5">' + row["user"].name + '</div></a><div class="h5"><small><i class="icon-realtime"></i> ' + timeSince(row["created_time"]) + '</small></div></div>',
        "message": fb_link(message),
        "like_count": '<div class="h5">' + row["like_count"] + '</div>',
        "comment_count": '<div class="h5">' + row["comment_count"] + '</div>',
    });
}


/**
 * Get search post and comment for management by using ajax
 *
 * @param url
 * @param table
 * @param limit
 * @param model
 * @param search
 * @param search_check
 * @param page
 * @param paging
 */
var getSearchPCM = function (url, table, limit, model, search, search_check, loading, page, paging) {
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
        c: search_check,
    }

    getAjaxResult(url, data, fun);
}


/**
 * Change search post and comment
 *
 * @param url
 * @param table
 * @param limit
 * @param model
 * @param search
 * @param search_check
 * @param loading
 * @param page
 * @param paging
 */
var changeSearchPCM = function (url, table, limit, model, search, search_check, loading, page, paging) {
    loading.show();
    getSearchPCM(url, table, limit, model, search, search_check, loading, page, paging);
}


/**
 * Get search blacklist for management by using ajax
 *
 * @param url
 * @param group_id
 * @param table
 * @param limit
 * @param search
 * @param page
 * @param paging
 */
var getSearchBM = function (url, group_id, table, limit, search, loading, page, paging) {
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
                "from": '<div class=" more-link"><a href="' + user_url + '"><div class="h4">' + row["name"] + '</div></a></div>',
                "count": '<div class="h4">' + blacklist["count"] + '</div>',
                "post_count": '<div class="h4">' + activity["post_count"] + '</div>',
                "comment_count": '<div class="h4">' + activity["comment_count"] + '</div>',
                "updated_time": '<div class="h4"><i class="icon-realtime"></i> ' + timeSince(blacklist["updated_time"]) + '</div>',
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
 * Change search blacklist
 *
 * @param url
 * @param group_id
 * @param table
 * @param limit
 * @param search
 * @param loading
 * @param page
 * @param paging
 */
var changeSearchBM = function (url, group_id, table, limit, search, loading, page, paging) {
    loading.show();
    getSearchBM(url, group_id, table, limit, search, loading, page, paging);
}


/**
 * Get search user for management by using ajax
 *
 * @param url
 * @param table
 * @param limit
 * @param search
 * @param page
 * @param paging
 */
var getSearchUM = function (url, table, limit, search, loading, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];

            var from = '<div class=" more-link"><a onclick="searchUMSelect(' + row["user"]["id"] + ')"><div class="h4">' + row["user"]["name"] + '<br>' + row["user"]["id"] + '</div></a></div>';
            rows.push({
                "picture": '<img src="' + row["user"]["picture"] + '" style="border-radius: 10px;">',
                "from": from,
            });
        }
        ;

        table.reset();
        table.append(rows);
        if (paging) {
            paging.setOption("pageCount", limit);
            paging.setOption("count", source["count"]);
            paging.reload(source["count"]);
            paging.first();
        }
        loading.hide()
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
 * Change search user
 *
 * @param url
 * @param table
 * @param limit
 * @param search
 * @param loading
 * @param page
 * @param paging
 */
var changeSearchUM = function (url, table, limit, search, loading, page, paging) {
    loading.show();
    getSearchUM(url, table, limit, search, loading, page, paging);
}