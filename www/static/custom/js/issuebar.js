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
 * Provides functions for issue bar
 */

var $Class = function (oClassMember) {
    function ClassOrigin() {
        this.$init.apply(this, arguments);
    }

    ClassOrigin.prototype = oClassMember;
    ClassOrigin.prototype.constructor = ClassOrigin;
    return ClassOrigin
}

var IssueBar = $Class({
    $init: function (id, option) {
        this.id = '#' + id;
        this.option = option;

        if (!String.prototype.format) {
            String.prototype.format = function () {
                var args = arguments;
                return this.replace(/{(\d+)}/g, function (match, number) {
                    return typeof args[number] != 'undefined'
                        ? args[number]
                        : match
                        ;
                });
            };
        }
        this.setup();
    },
    setup: function () {
        $(this.id).append($("<div />"));
        this.issue_header = $(this.id).children().last();
        $(this.id).append($("<div />"));
        this.issue_content = $(this.id).children().last();
        this.issue_content.attr("total_max_score", 0)
        $(this.id).append($("<div />"));
        this.issue_footer = $(this.id).children().last();

        if (this.option) {
            for (var prop in this.option) {
                if (!this.option.hasOwnProperty(prop)) continue;

                if (prop == 'read-more') {
                    this.generateReadMore(this.option[prop].text, this.option[prop].events);
                }
            }
        }
    },
    reset: function () {
        $(this.id).empty();
        this.setup();
    },
    getType: function (percentage) {
        if (percentage <= 20)
            return 'info';
        else if (percentage <= 40)
            return '';
        else if (percentage <= 60)
            return 'success';
        else if (percentage <= 80)
            return 'warning';
        else if (percentage <= 100)
            return 'danger';
    },
    changeEvents: function (object, events) {
        if (events) {
            for (var prop in events) {
                if (!events.hasOwnProperty(prop)) continue;
                object.on(prop, events[prop]);
            }
        }
    },
    generator: function (percentage, events, text1, text2) {
        var type = this.getType(percentage);
        var progress_bar_type = type ? 'progress-bar-' + type : '';
        var progress_bar_text_type = type ? 'issue-bar-text-' + type : '';

        var $process = $("<div>", {class: "progress issue"})
        var $process_bar = $("<div/>")
            .attr("class", "progress-bar issue-bar {0}".format(progress_bar_type))
            .attr("role", "progressbar")
            .attr("aria-valuenow", "60")
            .attr("aria-valuemin", "0")
            .attr("aria-valuemax", "100")
            .attr("style", "width: {0}%;".format(percentage));
        var $process_bar_text = $("<div/>")
            .attr("class", "issue-bar-text {0}".format(progress_bar_text_type))
            .append($("<span/>").text(text1));

        if (text2) {
            $process
                .addClass("issue-swap");
            $process_bar_text
                .attr("rel", text2);
        }

        $process
            .append($process_bar)
            .append($process_bar_text);

        this.changeEvents($process, events);

        this.issue_content.append($process);
    },
    generateReadMore: function (text, events) {
        this.read_more_btn = $("<button />", {
            class: "btn btn-outline btn-primary btn-lg btn-block",
            style: "margin-top: 10px;"
        })
            .text(text)
            .attr("rel", 1);

        this.changeEvents(this.read_more_btn, events);
        this.issue_footer.append(this.read_more_btn);
    }
});
