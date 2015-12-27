/**
 * Created by donghyun on 12/28/15.
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