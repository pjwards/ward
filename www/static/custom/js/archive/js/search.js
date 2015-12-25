/**
 * Created by donghyun on 12/25/15.
 */

/**
 * Get search post and comment by using ajax
 *
 * @param url
 * @param table
 * @param limit
 * @param search
 * @param loading
 * @param page
 * @param paging
 */
var getSearchPC = function (url, table, limit, search, loading, page, paging) {
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
 * Change search post and comment
 *
 * @param url
 * @param table
 * @param limit
 * @param search
 * @param page
 * @param paging
 */
var changeSearchPC = function (url, table, limit, search, loading, page, paging) {
    loading.show();
    getSearchPC(url, table, limit, search, loading, page, paging);
}