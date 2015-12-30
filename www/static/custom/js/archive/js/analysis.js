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
 * Provides functions for analysis page
 */

/**
 * Generate Statistics
 *
 * @param url
 * @param loading
 * @param method
 * @param from
 * @param to
 */
var getStatistics = function (url, loading, method, from, to) {
    var posts;
    var comments;
    var formatString;

    var fun = function (source) {

        posts = source['posts'];
        comments = source['comments'];

        if (method == 'year') {
            formatString = '%Y';
        } else if (method == 'month') {
            formatString = '%Y %b';
        } else if (method == 'day') {
            formatString = '%y %b %#d';
        } else if (method == 'hour') {
            formatString = '%y %b %#d, %#I %p';
        }

        $(document).ready(function () {
            statisticsPlot = $.jqplot('chart1', [posts, comments], {
                title: method.toUpperCase() + ' Statistics',
                animate: true,
                animateReplot: true,
                highlighter: {
                    show: true,
                    sizeAdjust: 7.5
                },
                legend: {
                    show: true,
                    location: 'ne',     // compass direction, nw, n, ne, e, se, s, sw, w.
                    placement: 'outside',
                    marginLeft: 300
                },
                seriesDefaults: {
                    rendererOptions: {
                        smooth: true
                    },
                    showMarker: true
                },
                series: [
                    {label: 'Posts'},
                    {label: 'Comments', yaxis: 'y2axis'},
                ],
                cursor: {
                    show: true,
                    zoom: true,
                    showTooltip: false
                },
                axesDefaults: {
                    useSeriesColor: true,
                    rendererOptions: {
                        alignTicks: true
                    }
                },
                axes: {
                    xaxis: {
                        tickOptions: {formatString: formatString},
                        renderer: $.jqplot.DateAxisRenderer
                    },
                    yaxis: {
                        label: "Post Count",
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        forceTickAt0: true,
                        pad: 0
                    },
                    y2axis: {
                        label: "Comment Count",
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        forceTickAt0: true,
                        pad: 0
                    }
                }
            });

            controllerStatisticsPlot = $.jqplot('chart2', [posts, comments], {
                animate: true,
                animateReplot: true,
                legend: {
                    show: false,
                },
                seriesDefaults: {
                    showMarker: false
                },
                series: [
                    {label: 'Posts'},
                    {label: 'Comments', yaxis: 'y2axis'},
                ],
                cursor: {
                    show: true,
                    showTooltip: false,
                    zoom: true,
                    constrainZoomTo: 'x'
                },
                axesDefaults: {
                    useSeriesColor: true,
                    rendererOptions: {
                        alignTicks: true
                    }
                },
                axes: {
                    xaxis: {
                        tickOptions: {formatString: formatString},
                        renderer: $.jqplot.DateAxisRenderer
                    },
                    yaxis: {
                        label: "Post Count",
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        forceTickAt0: true,
                        pad: 0
                    },
                    y2axis: {
                        label: "Comment Count",
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        forceTickAt0: true,
                        pad: 0
                    }
                }
            });

            $.jqplot.Cursor.zoomProxy(statisticsPlot, controllerStatisticsPlot);

            $.jqplot._noToImageButton = true;

            loading.hide();
        });
    }

    method = typeof method !== 'undefined' ? method : "month";

    data = {
        method: method,
        from: from,
        to: to
    }

    getAjaxResult(url, data, fun);
}


/**
 * Generate Hour Total Statistics
 *
 * @param url
 * @param loading
 */
var getHourTotalStatistics = function (url, loading) {
    var posts;
    var comments;

    var fun = function (source) {
        posts = source['posts'];
        comments = source['comments'];

        $(document).ready(function () {
            totalHourStatisticsPlot = $.jqplot('chart3', [posts, comments], {
                title: 'Time Overview',
                animate: true,
                animateReplot: true,
                highlighter: {
                    show: true,
                    sizeAdjust: 7.5
                },
                legend: {
                    show: true,
                    location: 'ne',     // compass direction, nw, n, ne, e, se, s, sw, w.
                    placement: 'outside',
                    marginLeft: 300
                },
                seriesDefaults: {
                    rendererOptions: {
                        smooth: true
                    },
                    showMarker: true
                },
                series: [
                    {label: 'Posts'},
                    {label: 'Comments', yaxis: 'y2axis'},
                ],
                cursor: {
                    show: true,
                    zoom: true,
                    showTooltip: false
                },
                axesDefaults: {
                    useSeriesColor: true,
                    rendererOptions: {
                        alignTicks: true
                    }
                },
                axes: {
                    xaxis: {
                        min: 0,
                        max: 23,
                        tickInterval: 1,
                    },
                    yaxis: {
                        label: "Post Count",
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        forceTickAt0: true,
                        pad: 0
                    },
                    y2axis: {
                        label: "Comment Count",
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        forceTickAt0: true,
                        pad: 0
                    }
                },
            });

            controllerTotalHourStatisticsPlot = $.jqplot('chart4', [posts, comments], {
                animate: true,
                animateReplot: true,
                legend: {
                    show: false,
                },
                seriesDefaults: {
                    showMarker: false
                },
                series: [
                    {label: 'Posts'},
                    {label: 'Comments', yaxis: 'y2axis'},
                ],
                cursor: {
                    show: true,
                    showTooltip: false,
                    zoom: true,
                    constrainZoomTo: 'x'
                },
                axesDefaults: {
                    useSeriesColor: true,
                    rendererOptions: {
                        alignTicks: true
                    }
                },
                axes: {
                    xaxis: {
                        min: 0,
                        max: 23,
                        tickInterval: 1,
                    },
                    yaxis: {
                        label: "Post Count",
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        forceTickAt0: true,
                        pad: 0
                    },
                    y2axis: {
                        label: "Comment Count",
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        forceTickAt0: true,
                        pad: 0
                    }
                }
            });

            $.jqplot.Cursor.zoomProxy(totalHourStatisticsPlot, controllerTotalHourStatisticsPlot);

            $.jqplot._noToImageButton = true;

            loading.hide();
        });
    }

    data = {
        method: "hour_total",
    }

    getAjaxResult(url, data, fun);
}


/**
 * Get issue by using ajax
 *
 * @param url
 * @param table
 * @param limit
 * @param from
 * @param to
 * @param loading
 * @param page
 * @param paging
 */
var getIssue = function (url, table, limit, from, to, loading, page, paging) {
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
        from: from,
        to: to,
    }

    getAjaxResult(url, data, fun);
}


/**
 * Change Issue
 *
 * @param url
 * @param table
 * @param limit
 * @param from
 * @param to
 * @param loading
 * @param page
 * @param paging
 */
function changeIssue(url, table, limit, from, to, loading, page, paging) {
    loading.show();
    getIssue(url, table, limit, from, to, loading, page, paging);
}


/**
 * Get archive by using ajax
 *
 * @param url
 * @param table
 * @param limit
 * @param from
 * @param user_id
 * @param loading
 * @param page
 * @param paging
 */
var getArchive = function (url, table, limit, from, user_id, loading, page, paging) {
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
        from: from,
    }

    if (user_id) {
        data["user_id"] = user_id;
    }

    getAjaxResult(url, data, fun);
}


/**
 * Change Archive
 *
 * @param url
 * @param table
 * @param limit
 * @param from
 * @param loading
 * @param page
 * @param paging
 */
function changeArchive(url, table, limit, from, loading, page, paging) {
    var user_id = undefined;
    loading.show();
    getArchive(url, table, limit, from, user_id, loading, page, paging);
}


/**
 * Change Archive by user
 *
 * @param url
 * @param table
 * @param limit
 * @param from
 * @param user_id
 * @param loading
 * @param page
 * @param paging
 */
function changeArchiveByUser(url, table, limit, from, user_id, loading, page, paging) {
    loading.show();
    getArchive(url, table, limit, from, user_id, loading, page, paging);
}