$(function () {
    $(".logo").click(function () {
        $(".container").toggleClass("hidden-menu");
    })
})

$(function () {
    // bind change event to select
    $('#dynamic_select').on('change', function () {
        var url = $(this).val(); // get selected value
        if (url) { // require a URL
            window.location = url; // redirect
        }
        return false;
    });
});

var timeSince = function (date) {
    if (typeof date !== 'object') {
        date = new Date(date);
    }

    var seconds = Math.floor((new Date() - date) / 1000);
    var intervalType;

    var interval = Math.floor(seconds / 31536000);
    if (interval >= 1) {
        intervalType = 'year';
    } else {
        interval = Math.floor(seconds / 2592000);
        if (interval >= 1) {
            intervalType = 'month';
        } else {
            interval = Math.floor(seconds / 86400);
            if (interval >= 1) {
                intervalType = 'day';
            } else {
                interval = Math.floor(seconds / 3600);
                if (interval >= 1) {
                    intervalType = "hour";
                } else {
                    interval = Math.floor(seconds / 60);
                    if (interval >= 1) {
                        intervalType = "minute";
                    } else {
                        interval = seconds;
                        intervalType = "second";
                    }
                }
            }
        }
    }

    if (interval > 1 || interval === 0) {
        intervalType += 's';
    }

    return interval + ' ' + intervalType + ' ago';
};

var generate_attachment = function (attachments, picture) {

    var html = '<div class="panel" style="border:1px solid #ababab; border-radius: 10px;"><div class="body"></div></div>';

    if (attachments.length < 0) {
        return '';
    }

    var attachment_html = '';
    var album_title = '';
    var album_url = '';
    var galleria_chk = false;
    for (var i in attachments) {
        var attachment = attachments[i];
        if (attachment["type"] == "share") {
            var share = picture ? '<div class="col col-4" align="middle"><img src="' + picture + '" width="80%"></div><div class="col col-8">' : '<div class="col col-12">';
            var description = attachment["description"] ? '</div><br><div class="h4">' + attachment["description"] + '</div>' : "";
            share += '<div class="h3"><span class="icon icon-share"></span> <a href="' + attachment["url"] + '" target="_blank">' + attachment["title"] + '</a>' + description + '</div>';

            return '<div class="panel" style="border:1px solid #ababab; border-radius: 10px;"><div class="body">' + share + '</div></div>';
        } else if (attachment["type"] == "file_upload") {
            var file = '<div class="h3"><span class="icon icon-save"></span> <a href="' + attachment["url"] + '" target="_blank">' + attachment["title"] + '</a></div>';
            return file;
            //return '<div class="panel" style="border:1px solid #ababab; border-radius: 10px;"><div class="body">' + file + '</div></div>';
        } else if (attachment["type"] == "note") {
            var note = picture ? '<div class="col col-4" align="middle"><img src="' + picture + '" width="80%"></div><div class="col col-8">' : '<div class="col col-12">';
            var description = attachment["description"] ? '</div><br><div class="h4">' + attachment["description"] + '</div>' : "";
            note += '<div class="h3"><span class="icon icon-share"></span> <a href="' + attachment["url"] + '" target="_blank">' + attachment["title"] + '</a>' + description + '</div>';

            return '<div class="panel" style="border:1px solid #ababab; border-radius: 10px;"><div class="body">' + note + '</div></div>';
        } else if (attachment["type"] == "unavailable") {
            var description = attachment["description"] ? '</div><br><div class="h4">' + attachment["description"] + '</div>' : "";
            var unavailable = '<div class="h3"><span class="icon icon-save"></span>' + attachment["title"] + description + '</div>';

            return '<div class="panel" style="border:1px solid #ababab; border-radius: 10px;"><div class="body">' + unavailable + '</div></div>';
        } else if (attachment["type"] == "video_inline") {
            var img = '<a href="' + attachment["url"] + '" target="_blank"><img src="' + picture + '"></a>';
        } else if (attachment["type"] == "album") {
            album_title = attachment["title"];
            album_url = attachment["url"];
        } else if (attachment["type"] == "photo") {

            if (!galleria_chk) {
                galleria_chk = true;
            }

            var img = '<img src="' + attachment["media"]["src"] + '"';

            if (album_title) {
                img += ' data-title="' + album_title + '"';
            }

            if (album_url) {
                img += ' data-description="' + album_url + '"';
            }
            img += '>';
            attachment_html += img;
        }
    }
    if (galleria_chk) {
        var galleria = '<div class="galleria">' + attachment_html + '</div>';
        return galleria;
    }
    return '';
}