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
 * Provides functions for ajax
 */

/**
 * Get Results by using ajax
 *
 * @param url
 * @param data
 * @param fun
 */
var getAjaxResult = function (url, data, fun) {
    $.ajax({
        url: url,
        type: "get",
        data: data,
        dataType: "JSON",
        success: function (source) {
            fun(source);
        },
        error: function (request, status, error) {
            data = {
                title: status,
                message: getToday(),
                color: 'danger',
            }
            notify_top_submit(1, data);
        }
    });
}


/**
 * Get Results by using async ajax
 *
 * @param url
 * @param data
 * @returns {undefined}
 */
var getAsyncAjaxResult = function (url, data) {
    var response = $.ajax({
        url: url,
        type: "get",
        async: false,
        data: data,
        dataType: "JSON",
    }).responseText;

    return response.includes("DoesNotExist") ? undefined : JSON.parse(response);
}


/**
 * Post by using ajax
 *
 * @param url
 * @param data
 */
var postAjax = function (url, data) {
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: url,
        type: "post",
        data: data,
        dataType: "JSON",
        success: function (source) {
            if (source["success"]) {
                data = {
                    title: source["success"],
                    message: getToday(),
                    color: 'success',
                }
                notify_top_submit(1, data);
            }
            else if (source["error"]) {
                data = {
                    title: source["error"],
                    message: getToday(),
                    color: 'danger',
                }
                notify_top_submit(1, data);
            }
        },
        error: function (request, status, error) {
            data = {
                title: status,
                message: getToday(),
                color: 'danger',
            }
            notify_top_submit(1, data)
        }
    });
}


/**
 * Post by using async ajax
 *
 * @param url
 * @param data
 */
var postAsyncAjax = function (url, data) {
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: url,
        type: "post",
        data: data,
        async: false,
        dataType: "JSON",
        success: function (source) {
            if (source["success"]) {
                data = {
                    title: source["success"],
                    message: getToday(),
                    color: 'success',
                }
                notify_top_submit(1, data);
            }
            else if (source["error"]) {
                data = {
                    title: source["error"],
                    message: getToday(),
                    color: 'danger',
                }
                notify_top_submit(1, data);
            }
        },
        error: function (request, status, error) {
            data = {
                title: status,
                message: getToday(),
                color: 'danger',
            }
            notify_top_submit(1, data)
        }
    });
}


/**
 * Delete by using async ajax
 *
 * @param url
 * @param data
 */
var deleteAsyncAjax = function (url, data) {
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: url,
        type: "delete",
        data: data,
        async: false,
        dataType: "JSON",
        success: function (source) {
            if (source["success"]) {
                data = {
                    title: source["success"],
                    message: getToday(),
                    color: 'success',
                }
                notify_top_submit(1, data);
            }
            else if (source["error"]) {
                data = {
                    title: source["error"],
                    message: getToday(),
                    color: 'danger',
                }
                notify_top_submit(1, data);
            }
        },
        error: function (request, status, error) {
            data = {
                title: status,
                message: getToday(),
                color: 'danger',
            }
            notify_top_submit(1, data)
        }
    });
}