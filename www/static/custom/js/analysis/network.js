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
 * Provides functions for network
 */


var nodes = null;
var edges = null;
var network = null;

/**
 * Draw network
 *
 * @param url
 * @param group
 */

function drawNetwork(url, group) {
    var fun = function (source) {
        nodes = source["nodes"];
        edges = source["edges"];

        if (network) {
            document.getElementById('network_text').innerHTML = '0%';
            document.getElementById('network_loadingBar').style.display = '';
            document.getElementById('network_loadingBar').style.opacity = 1;
        }

        // Instantiate our network object.
        var container = document.getElementById('network_content');
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {
            nodes: {
                shape: 'dot',
                scaling: {
                    customScalingFunction: function (min, max, total, value) {
                        return value / total;
                    },
                    min: 5,
                    max: 150
                }
            }
        };
        network = new vis.Network(container, data, options);

        network.on("stabilizationProgress", function (params) {
            var maxWidth = 196;
            var minWidth = 10;
            var widthFactor = params.iterations / params.total;
            var width = Math.max(minWidth, maxWidth * widthFactor);
            document.getElementById('network_bar').style.width = width + 'px';
            document.getElementById('network_text').innerHTML = Math.round(widthFactor * 100) + '%';
        });
        network.once("stabilizationIterationsDone", function () {
            document.getElementById('network_text').innerHTML = '100%';
            document.getElementById('network_bar').style.width = '196px';
            document.getElementById('network_loadingBar').style.opacity = 0;
            // really clean the dom element
            setTimeout(function () {
                document.getElementById('network_loadingBar').style.display = 'none';
            }, 500);
        });
        network.on("doubleClick", function (params) {
            params.event = "[original event]";
            if (params.nodes[0]) {
                drawNetwork(url, params.nodes[0]);
            } else {
                drawNetwork(url);
            }
        });
    }

    data = {}
    if (group) {
        data['group'] = group
    }

    getAjaxResult(url, data, fun);
}
