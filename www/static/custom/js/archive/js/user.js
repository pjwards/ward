/**
 * Get active by using ajax
 *
 * @param url
 * @param limit
 * @param model
 * @param table
 * @param loading
 */
var getActivity = function (url, limit, model, table, loading) {

    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var user_url = '/archive/user/' + row["user"]["id"] + '/';

            var count = 0;
            if (model == 'post') {
                count = row["post_count"];
            } else {
                count = row["comment_count"];
            }
            rows.push({
                "picture": '<img src="' + row["user"]["picture"] + '" style="border-radius: 10px;">',
                "from": '<div class=" more-link"><a href="' + user_url + '"><div class="h4">' + row["user"]["name"] + '</div></a></div>',
                "count": '<div class="h4">' + count + '</div>',
            });
        }
        ;

        table.reset()
        table.append(rows);
        loading.hide();
    }

    data = {
        limit: limit,
        model: model
    }

    getAjaxResult(url, data, fun);
}


/**
 * Change Activity
 *
 * @param url
 * @param limit
 * @param model
 * @param table
 * @param loading
 */
var changeActivity = function (url, limit, model, table, loading) {
    loading.show();
    getActivity(url, limit, model, table, loading);
}


/**
 * Generate Proportion
 *
 * @param url
 * @param post_loading
 * @param comment_loading
 */
var getProportion = function (url, post_loading, comment_loading) {
    var posts;
    var comments;

    var fun = function (source) {
        posts = source['posts'];
        comments = source['comments'];

        $(document).ready(function () {
            postProportion = $.jqplot('pie1', [posts], {
                highlighter: {
                    show: true,
                    formatString: '%s (%P)',
                    tooltipLocation: 'sw',
                    useAxesFormatters: false
                },
                grid: {
                    drawBorder: false,
                    drawGridlines: false,
                    background: '#ffffff',
                    shadow: false
                },
                axesDefaults: {},
                seriesDefaults: {
                    renderer: $.jqplot.PieRenderer,
                    rendererOptions: {
                        showDataLabels: true
                    }
                },
                legend: {
                    show: true,
                    rendererOptions: {
                        numberRows: 1
                    },
                    location: 's'
                }
            });

            commentProportion = $.jqplot('pie2', [comments], {
                highlighter: {
                    show: true,
                    formatString: '%s (%P)',
                    tooltipLocation: 'sw',
                    useAxesFormatters: false
                },
                grid: {
                    drawBorder: false,
                    drawGridlines: false,
                    background: '#ffffff',
                    shadow: false
                },
                axesDefaults: {},
                seriesDefaults: {
                    renderer: $.jqplot.PieRenderer,
                    rendererOptions: {
                        showDataLabels: true
                    }
                },
                legend: {
                    show: true,
                    rendererOptions: {
                        numberRows: 1
                    },
                    location: 's'
                }
            });

            post_loading.hide();
            comment_loading.hide();
        });
    };

    data = {}

    getAjaxResult(url, data, fun);
}


/**
 * Change Proportion
 *
 * @param url
 * @param post_loading
 * @param comment_loading
 */
function changeProportion(url, post_loading, comment_loading) {
    post_loading.show();
    comment_loading.show();
    getProportion(url, post_loading, comment_loading)
}


/**
 * Get user archive by using ajax
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
var getUserArchive = function (url, group_id, table, limit, search, loading, page, paging) {
    var fun = function (source) {
        var results = source["results"];
        var rows = []
        for (var i in results) {
            var row = results[i];
            var user_url = '/archive/user/' + row["user"]["id"] + '/';

            rows.push({
                "picture": '<img src="' + row["user"]["picture"] + '" style="border-radius: 10px;">',
                "from": '<div class=" more-link"><a href="' + user_url + '"><div class="h4">' + row["user"]["name"] + '</div></a></div>',
                "post_count": '<div class="h4">' + row["post_count"] + '</div>',
                "comment_count": '<div class="h4">' + row["comment_count"] + '</div>',
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
    }

    if (search) {
        data['q'] = search;
    }

    getAjaxResult(url, data, fun);
}


/**
 * Change User Archive
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
function changeUserArchive(url, group_id, table, limit, search, loading, page, paging) {
    loading.show();
    getUserArchive(url, group_id, table, limit, search, loading, page, paging);
}