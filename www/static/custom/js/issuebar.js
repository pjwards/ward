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

var issueBar = new function () {
    this.id;
    this.setup = function (id) {
        this.id = '#' + id;

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
    }
    this.getType = function (percentage) {
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
    }
    this.generator = function (percentage, event, text1, text2) {
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
            .attr("style", "width: {0}%;".format(percentage))
        var $process_bar_text = $("<div/>")
            .attr("class", "issue-bar-text {0}".format(progress_bar_text_type))
            .append($("<span/>").text(text1))

        if (text2) {
            $process_bar_text
                .addClass("issue-swap")
                .attr("rel", text2)
        }

        $process
            .append($process_bar)
            .append($process_bar_text)
            .on('click', event);

        $(this.id).append($process);
    }
}
