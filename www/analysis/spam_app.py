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
""" Provides spam app class """

import ward.www.analysis.analysis_core as core
from django.db.models import Q
from .models import SpamList, SpamWordList


#def __init__(self, group):
#    """
#    Initialize Spam class
#    """
#    self.analyzer = core.AnalysisDiction(True, True)
#    self.group = group

def init_db(group):
    """
    save standard word from spam.txt to database when initialize database
    """
    data_set = [line.strip() for line in open("analysis/texts/spam.txt", 'r')]
    for i in data_set:
        store_data = SpamWordList(word=i, group=group, status='filter')
        store_data.save()


def save_user_word(group, word):
    """
    Save user's words in DB
    """
    store_data = SpamWordList(word=word, group=group, status='user')
    store_data.save()


def analyze_posts(analyzer, group, message):
    """
    Return true if analyzed words and spam words are same
    :param analyzer: analyzer for analysis
    :param group: group id
    :param message: message of post or comment
    :return: true or false
    """
    spam_db = SpamWordList.objects.filter(Q(group=group), Q(status='filter') | Q(status='user'))     # all spamlist data loads in list
    data_set = [sp.word for sp in spam_db]
    twitter_posmore = analyzer.analyzer_twitter(message, 'posmore')
    kkma_nouns = analyzer.analyzer_kkma(message, 'nouns')

    for i in twitter_posmore:                   # change the method
        if i[0] in data_set:
            return True

    for i in kkma_nouns:
        if i in data_set:
            return True

    return False

    #result_twi = core.compare_and_make_words(twitter_posmore, data_set)
    #result_kkma = core.compare_and_make_words(kkma_nouns, data_set)
    #analyzed_words = core.count_in_list(result_twi+result_kkma)     # change better solution
    #return analyzed_words


def add_spam_list(group, message):
    """
    add to spam list
    :param message: message of post or comment
    :param group: group data set
    """
    try:
        spam_db = SpamList.objects.filter(group=group, status='temp')
        for i in spam_db:
            if i.text != message:
                spam_data = SpamList(group=group, text=message)
                spam_data.save()

    except Exception as expt:
        print("error occurred:"+expt)


def delete_from_spam_list(group, message):
    """
    change status of spam list to deleted
    :param message: message of post or comment
    :param group: group data set
    """
    try:
        spam_data = SpamList.objects.get(group=group, text=message)
        spam_data.status = 'deleted'
        spam_data.save()
    except Exception as expt:
        print("error occurred:"+expt)

    ##alarm about spam that deleted in other group
    ##remmadation function


def analyze_deleted_spamlist(analyzer, message):
    """
    analyze deleted spam list
    :param analyzer: analyzer for analysis
    :param message: message of spam list
    :return: spam words list
    """
    tempword = []

    twitter_posmore = analyzer.analyzer_twitter(message, 'posmore')
    kkma_nouns = analyzer.analyzer_kkma(message, 'nouns')

    for i in twitter_posmore:
        tempword.append(i[0])

    tempword = tempword + kkma_nouns
    returnword = list(set(tempword))        # remove duplicates

    return returnword


def add_spam_words(group, words):
    """
    add words in DB
    :param group: group id
    :param words: spam words list
    """
    try:
        words_db = SpamWordList.objects.filter(group=group)
        for i in words_db:
            if i in words:
                word = SpamWordList.objects.filter(group=group, word=i)
                word.count += 1
                word.save()
            else:
                spamword = SpamWordList(word=i, group=group)
                spamword.save()
    except Exception as expt:
        print("error occurred:"+expt)


def update_words_level(group):
    """
    change temp status of word to filter
    :param group: group id
    """
    words_db = SpamWordList.objects.filter(group=group, status='temp', count__gte=10)
    for i in words_db:
        i.status = 'filter'
        i.save()


def run_app(group, message):      # test-only method
    init_db(group)      # when made group

    analyzer = core.AnalysisDiction(True, True)         # always turn analyzer on

    # save_user_word(group)                 # add spam words from users
    spam = analyze_posts(analyzer, group, message)      # analyze posts when get it from FB

    if spam is False:           # if value of spam is false, skip the sequence
        return

    add_spam_list(group, message)          # if value of spam if true, add it to spam list

    words = analyze_deleted_spamlist(analyzer, message)         # if user delete spam post in spam list, analyze it

    add_spam_words(group, words)        # add words from message to spam words list

    update_words_level(group)       # search spam words list and find count of word is greater than critical point

    #string = '''slack 에서는 팀초대 api 만 제공하고 있고 이를 쓸려면 써드파티 솔루션들을 써야하는 데. 이를 쓸려면 배포하는 수고를 거쳐야되고. 각 팀마다 배포하는 수고를 거치기보다, 나 혼자 수고하면 되지 않나 싶어서. slack 초대 서비스를 간단히 만들어봤습니다. 물론 Django 로 만들었죠. ㅎㅎ http://festi.kr/zlack/ 에 로그인하고, 그 팀에 대한 slack token 만 등록하면 끝 ~ !!! 현재 2개의 팀이 등록되어있습니다. - django korea, django-girls-seoul'''

    """
    group = ''
    #spam = Spam()
    #spam.init_db()

    analyzed_words = spam.compare_and_count(string)
    total = 0
    for i in analyzed_words:
        total += i[1]

    a = SpamList.objects.all()
    for i in a:
        print(i.word+"/"+str(i.count)+"/"+i.status)
    print(total)
    print(analyzed_words)
    spam.update_standard_word()
    if total > 10:       #evaluate whether a content is spam or not
        add_spam_list(string, group)

    a = SpamWordList.objects.filter(status='temp')
    print(a)
    for i in a:
        print(i.word+"/"+str(i.count)+"/"+i.status)
    """


