/**
 * Created by donghyun on 12/24/15.
 */

/**
 * Generate Proportion
 */
var getProportion = function (url) {
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

        });
    };

    data = {}

    getAjaxResult(url, data, fun);
}