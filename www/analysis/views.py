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
""" Sets views """
from django.http import HttpResponse
from rest_framework import viewsets
from analysis.tools import network
from analysis.rest.serializer import *


def analysis_network(request):
    """
    Return group network

    :param request: request
    :return: json
    """
    if request.method == 'GET':
        group_id = request.GET.get("group", None)
        if Group.objects.filter(id=group_id).exists():
            network_json = network.network(group_id)
        else:
            network_json = network.network()

        return HttpResponse(network_json, content_type="application/json")


class SpamListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Spam list View Set for django restful framework
    """
    queryset = SpamList.objects.all()
    serializer_class = SpamListSerializer


class SpamWordListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Spam word list View Set for django restful framework
    """
    queryset = SpamWordList.objects.all()
    serializer_class = SpamWordListSerializer


class AnticipateArchiveViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Spam word list View Set for django restful framework
    """
    queryset = AnticipateArchive.objects.all()
    serializer_class = AnticipateArchiveSerializer


class MonthTrendWordViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Month trend word list View Set for django restful framework
    """
    queryset = MonthTrendWord.objects.all()
    serializer_class = MonthTrendWordSerializer


class MonthlyWordsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Monthly words list View Set for django restful framework
    """
    queryset = MonthlyWords.objects.all()
    serializer_class = MonthlyWordsSerializer
