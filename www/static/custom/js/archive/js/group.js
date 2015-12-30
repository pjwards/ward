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
 * Provides functions for group page
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
            var is_stored = row["is_stored"] ? '<i class="icon-check"> Yes</i>' : '<i class="icon-close"> No</i>';
            var name = row["name"].length < detectWidthToSubstring() ? row["name"] : row["name"].substring(0, detectWidthToSubstring()) + "...";
            rows.push({
                "name": '<div class=" more-link"><a href="' + group_url + '"><div class="h4">' + name + '</div></a></div>',
                "updated_time": '<div class="h4"><i class="icon-realtime"></i> ' + timeSince(row["updated_time"]) + '</div>',
                "post_count": '<div class="h4">' + row["post_count"] + '</div>',
                "comment_count": '<div class="h4">' + row["comment_count"] + '</div>',
                "owner": row["owner"] ? row["owner"]["name"] : 'Empty',
                "is_stored": is_stored,
                "action": '<a class="btn large" href="/archive/group/' + row["id"] + '/update/" style="color:#ffa500;">Update</a>',
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
            var is_stored = row["is_stored"] ? '<i class="icon-check"> Yes</i>' : '<i class="icon-close"> No</i>';
            var name = row["name"].length < detectWidthToSubstring() ? row["name"] : row["name"].substring(0, detectWidthToSubstring()) + "...";
            var update_btn = '<a class="btn large" href="/archive/group/' + row["id"] + '/update/" style="color:#ffa500;">Update</a>';
            var store_btn = '<a class="btn large" href="/archive/group/' + row["id"] + '/store/" style="color:#6495ed;">Store</a>';
            var check_btn = '<a class="btn large" href="/archive/group/' + row["id"] + '/check/" style="color:#ff1493;">Check</a>';
            rows.push({
                "name": '<div class=" more-link"><a href="' + group_url + '"><div class="h4">' + name + '</div></a></div>',
                "updated_time": '<div class="h4"><i class="icon-realtime"></i> ' + timeSince(row["updated_time"]) + '</div>',
                "post_count": '<div class="h4">' + row["post_count"] + '</div>',
                "comment_count": '<div class="h4">' + row["comment_count"] + '</div>',
                "owner": row["owner"] ? row["owner"]["name"] : 'Empty',
                "is_stored": is_stored,
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