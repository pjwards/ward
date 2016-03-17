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
""" Provides analysis core class """

from konlpy.tag import Twitter
from konlpy.tag import Hannanum
# from konlpy.tag import Mecab
from urllib.parse import urlparse
import re
from collections import Counter


class AnalysisDiction:
    """
    This class is for analysis of korean texts using kkma and twitter dictionaries
    """
    def __init__(self, on_han=False, on_twitter=False, on_mecab=False):    # maybe move to init of analysis_app

        """
        Allocate kkma or twitter diction instance
        :param on_han: han instance
        :param on_twitter: twitter instance
        :param on_mecab: mecab instance
        """
        if on_han is True:
            self.han = Hannanum()
        if on_twitter is True:
            self.twitter = Twitter()
        # if on_mecab is True:
        #     self.mecab = Mecab()

    def analyzer_hannaum(self, string_data, mode):
        """
        This method is for hannanum. It acts differently depends on its mode.
        :param string_data: String data for analysis
        :param mode: Analyze string data depending on its mode
        :return: Return its results. If have no mode in param , return false
        ref: http://konlpy.org/ko/v0.4.4/api/konlpy.tag/#module-konlpy.tag._hannanum
        """
        if mode is 'morphs':
            return self.han.morphs(string_data)
        elif mode is 'nouns':
            return self.han.nouns(string_data)
        elif mode is 'pos':
            return self.han.pos(string_data)
        else:
            return False

    def analyzer_mecab(self, string_data, mode):
        """
        This method is for mecab. It acts differently depends on its mode.
        :param string_data: String data for analysis
        :param mode: Analyze string data depending on its mode
        :return: Return its results. If have no mode in param , return false
        ref: http://konlpy.org/ko/v0.4.4/api/konlpy.tag/#mecab-class
        """
        if mode is 'morphs':
            return self.mecab.morphs(string_data)
        elif mode is 'nouns':
            return self.mecab.nouns(string_data)
        elif mode is 'pos':
            return self.mecab.pos(string_data)
        else:
            return False

    def analyzer_twitter(self, string_data, mode):
        """
        This method is for twitter. It acts differently depends on its mode.
        :param string_data: String data for analysis
        :param mode: Analyze string data depending on its mode
        :return: Return its results. If have no mode in param , return false
        ref: http://konlpy.org/ko/v0.4.4/api/konlpy.tag/#module-konlpy.tag._twitter
        """
        if mode is 'morphs':
            return self.twitter.morphs(string_data)
        elif mode is 'nouns':
            return self.twitter.nouns(string_data)
        elif mode is 'pos':
            return self.twitter.pos(string_data)
        elif mode is 'posmore':
            return self.twitter.pos(string_data, True, True)
        else:
            return False


def analyze_text(string_data, db_data):
    """
    Make list about duplicated words
    :param string_data: text list
    :param db_data: list of words in database
    :return: return list that have tuples of words and count value
    """
    val_words = [item for item, count in Counter(string_data).items() if count > 1]
    res = []
    for i in val_words:
        if i in db_data:
            res.append((i, 10))
        elif i not in db_data:
            res.append((i, 1))
    return res


def compare_and_make_words(words, comparison_words):
    """
    Compare standard words with input words. If two words are same, collects that word
    :param words: analyzed words
    :param comparison_words: standard words
    :return: collecting words list. If input list has no str or tuple type, return false
    """
    meanning_words = []
    if type(words[0]).__name__ == 'str':    # morphs, nouns
        for i in words:
            if i in comparison_words:
                meanning_words.append(i)
        return meanning_words
    elif type(words[0]).__name__ == 'tuple':    # pos, posmore
        for i in words:
            if i[0] in comparison_words:
                meanning_words.append(i[0])
        return meanning_words
    else:
        return False


def get_url_from_string(string_data):
    """
    Get urls from string data
    :param string_data: string data which has urls
    :return: url list
    """
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string_data)
    return_urls = []
    for i in urls:  # Rid of param and query in urls
        mid = urlparse(i)
        string_url = mid[0]+"://"+mid[1]+mid[2]
        return_urls.append(string_url)
    return return_urls


def count_in_list(string_data):
    """
    Count same words in input data
    :param string_data: string data for counting
    :return: return list has tuples that have word and count
    """
    return_list = []
    res = Counter(string_data)
    for i in res.keys():
        return_list.append((i, res.get(i)))
    return return_list


def url_duplication_check(data_set, urls):
    """
    Remove elements from urls list in data_set and urls list
    :param data_set: data_set list
    :param urls: list of urls
    :return: list that no duplicated elements that are in data_set and urls list
    """
    url_list = list(set(urls))
    for i in data_set:
        if i in url_list:
            urls.remove(i)  # this sequence only removes first element of duplicates

    return url_list


def analyze_articles(message):
    """
    analyze articles
    :param message: string data
    :return: refined words list
    """
    analyzer = AnalysisDiction(on_han=False, on_twitter=True, on_mecab=True)

    if message is None:
        return []

    twitter_nouns = analyzer.analyzer_twitter(message, 'nouns')
    # mecab_nouns = analyzer.analyzer_mecab(message, 'nouns')

    # tempword = mecab_nouns + twitter_nouns
    tempword = twitter_nouns

    returnword = list(set(tempword))        # func = remove duplicates

    refineword = []

    for i in returnword:
        if len(i) < 2:
            continue
        refineword.append(i)

    return refineword       # need better refine words


def analyze_articles_up(message):   # analyzer
    """
    analyze articles
    :param message: string data
    :return: refined words list
    """

    analyzer = AnalysisDiction(on_han=True, on_twitter=True, on_mecab=True)

    if message is None:
        return []

    temp_twitter = []
    temp_mecab = []
    temp_han = []

    twitter_posmore = analyzer.analyzer_twitter(message, 'posmore')
    mecab_posmore = analyzer.analyzer_mecab(message, 'pos')
    han_posmore = analyzer.analyzer_hannaum(message, 'pos')

    twi_stemlist = ['Alpha', 'URL']     # 'Adjective', 'Noun'

    for i in twitter_posmore:
        if i[1] in twi_stemlist:
            temp_twitter.append(i)

    for i in mecab_posmore:
        temp_mecab.append(i)

    for i in han_posmore:
        temp_han.append(i)

    print(temp_twitter)
    print(temp_mecab)
    print(temp_han)

    tempword = temp_twitter + temp_mecab + temp_han

    returnword = list(set(tempword))        # func = remove duplicates

    refineword = []

    for i in returnword:
        if len(i[0]) < 2:
            continue
        refineword.append(i)

    return refineword       # need better refine words


def analysis_text_by_words(base_words, analyzed_words, avg_weigh):
    """
    Compare words for analysis
    :param base_words: standard words
    :param analyzed_words: Be compared words
    :param avg_weigh: average of weigh for standard
    :return: Return true if analyzed words are in base words set and over critical number
    """
    wordhash = dict((k, 0) for k in base_words)
    for k in analyzed_words:
        if wordhash.get(k):
            wordhash[k] += 1
        # else:
            # print(k+' is None ')
            # print(k+' is '+str(wordhash[k]))

    total = 0

    for k in wordhash:
        total += wordhash[k]

    # print(total)

    if total > avg_weigh:
        return True
    else:
        return False
