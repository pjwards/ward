# The MIT License (MIT)
#
# Copyright (c) 2015 pjwards.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==================================================================================
""" Provides analysis tool about network """

from analysis.models import *
import json


def network(group_id=None):
    """
    Return group network

    :param group_id: group id
    :return: json
    """
    # Is ready to update?
    update_list = UpdateList.objects.filter(method='network')
    if update_list:
        update_list = update_list[0]
        is_update = update_list.is_update()
    else:
        is_update = True

    if is_update or not update_list:
        _network_edge = []
        _network_node = []

        group_user_list = {}
        group_list = {}
        _network_node_dic = {}

        group_data = Group.objects.exclude(privacy='CLOSED').extra(
                select={'fieldsum': 'post_count + comment_count'},
                order_by=('-fieldsum',)
        )
        for group in group_data:
            user_list = group.fbuser_set.values_list('id', flat=True)
            group_user_list[group.id] = user_list
            group_list[group.id] = group

        keys = list(group_user_list.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                edge = len(set(group_user_list[keys[i]]).intersection(set(group_user_list[keys[j]])))
                if edge > 100:
                    _network_edge.append({'from': keys[i], 'to': keys[j], 'value': edge_value(edge)})
                    _network_node_dic[keys[i]] = _network_node_dic.setdefault(keys[i], 0) + 1
                    _network_node_dic[keys[j]] = _network_node_dic.setdefault(keys[j], 0) + 1

        for key in group_list.keys():
            _network_node.append({'id': key, 'value': _network_node_dic.get(key, 1), 'label': group_list[key].name,
                                  'group': network_group(_network_node_dic.get(key, 1))})

        network_json = json.dumps({'edges': _network_edge, 'nodes': _network_node})
        update_list = UpdateList.update(method='network', data=network_json)

    if group_id and Group.objects.filter(id=group_id).exists():
        network_json = update_list.data
        network_dic = json.loads(network_json)
        _network_edge = network_dic['edges']
        _network_node = network_dic['nodes']
        _new_network_edge = []
        _new_network_node = []
        group_list = []

        for edge in _network_edge:
            if edge.get('from') == group_id or edge.get('to') == group_id:
                _new_network_edge.append(edge)
                if edge.get('from') == group_id:
                    group_list.append(edge.get('to'))
                else:
                    group_list.append(edge.get('from'))

        for node in _network_node:
            if node.get('id') in group_list:
                _new_network_node.append(node)
            elif node.get('id') == group_id:
                _new_network_node.append(node)

        network_json = json.dumps({'edges': _new_network_edge, 'nodes': _new_network_node})
    else:
        network_json = update_list.data

    return network_json


def edge_value(edge):
    """
    Return edge value

    :param edge: edge
    :return: value
    """
    if edge < 0:
        return 0
    elif edge < 50:
        return 1
    elif edge < 100:
        return 2
    elif edge < 150:
        return 3
    elif edge < 200:
        return 4
    elif edge < 250:
        return 5
    elif edge < 300:
        return 6
    elif edge < 350:
        return 7
    elif edge < 400:
        return 8
    elif edge < 450:
        return 9
    elif edge < 500:
        return 10
    elif edge < 1000:
        return 12
    elif edge < 1500:
        return 14
    elif edge < 2000:
        return 16
    else:
        return 18


def network_group(value):
    """
    Return network node group

    :param value: value
    :return: node group
    """
    if value < 0:
        return 0
    elif value < 5:
        return 1
    elif value < 10:
        return 2
    elif value < 15:
        return 3
    elif value < 20:
        return 4
    elif value < 25:
        return 5
    elif value < 30:
        return 6
    elif value < 35:
        return 7
    elif value < 40:
        return 8
    elif value < 45:
        return 9
    elif value < 50:
        return 10
    elif value < 55:
        return 11
    elif value < 60:
        return 12
    elif value < 65:
        return 13
    else:
        return 14

