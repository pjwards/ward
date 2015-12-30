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
 * Provides functions for search page
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