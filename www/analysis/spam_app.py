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

import analysis.analysis_core as core
from django.db.models import Q
from .models import SpamList, SpamWordList
from archive.models import Group, FBUser, Post, Comment


def init_db(group_id):
    """
    save standard word from spam.txt to database when initialize database
    :param group_id: group id
    """
    group = Group.objects.filter(id=group_id)[0]
    data_set = [line.strip() for line in open("analysis/texts/spam.txt", 'r')]
    for i in data_set:
        store_data = SpamWordList(word=i, group=group, status='filter')
        store_data.save()


def save_user_word(group_id, word):
    """
    Save user's words in DB
    :param group_id: group id
    :param word: target word
    """
    group = Group.objects.filter(id=group_id)[0]
    store_data = SpamWordList(word=word, group=group, status='user')
    store_data.save()


def delete_user_word(group_id, word):
    """
    Change user word to deleted word
    :param group_id: group id
    :param word: target word
    """
    group = Group.objects.filter(id=group_id)[0]
    word_data = SpamWordList.objects.filter(word=word, group=group)
    word_data.status = 'deleted'
    word_data.save()


def analyze_post(analyzer, group, message):
    """
    Return true if analyzed words and spam words are same
    :param analyzer: analyzer for analysis
    :param group: group object
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


def add_spam_list(group, user, object_id, message, time):
    """
    add to spam list
    :param message: message of post or comment
    :param group: group object
    :param object_id: id of post or comment
    :param user: user object
    :param time: time of object
    """
    try:
        spamlist = SpamList()
        spamlist.id = object_id
        spamlist.group = group
        spamlist.user = user
        spamlist.message = message
        spamlist.last_updated_time = time
        spamlist.status = 'temp'
        spamlist.save()

    except Exception as expt:
        print("error occurred:"+expt)


def delete_content(data_object):
    """
    change status of spam list to deleted
    :param object_id: id of post or comment
    :param group_id: group id
    """
    try:
        spam_data = SpamList.objects.get(group=data_object.group, id=data_object.id)
        spam_data.status = 'deleted'
        spam_data.save()

    except Exception as expt:
        print("error occurred:"+expt)


def analyze_deleted_spamlist(analyzer, message):
    """
    analyze deleted spam
    :param analyzer: analyzer for analysis
    :param message: message of spam list
    :return: spam words list
    """
    tempTwitter = []

    twitter_posmore = analyzer.analyzer_twitter(message, 'posmore')
    kkma_nouns = analyzer.analyzer_kkma(message, 'nouns')

    for i in twitter_posmore:
        tempTwitter.append(i[0])

    tempword = tempTwitter + kkma_nouns
    returnword = list(set(tempword))        # remove duplicates

    return returnword


def analyze_restored_spamlist(analyzer, group_id, message):
    """
    analyze restored spam
    :param analyzer: analyzer for analysis
    :param group_id: group id
    :param message: message of spam list
    """
    tempTwitter = []

    twitter_posmore = analyzer.analyzer_twitter(message, 'posmore')
    kkma_nouns = analyzer.analyzer_kkma(message, 'nouns')

    for i in twitter_posmore:
        tempTwitter.append(i[0])

    tempWord = tempTwitter + kkma_nouns
    words = list(set(tempWord))

    try:
        group = Group.objects.filter(id=group_id)[0]
        words_db = SpamWordList.objects.filter(group=group)
        for i in words_db:
            if i.word in words:
                i.count -= 1

    except Exception as expt:
        print("error occurred:"+expt)


def add_spam_words(group, words):
    """
    add words in DB
    :param group: group object
    :param words: spam words list
    """
    try:
        words_db = SpamWordList.objects.filter(group=group)
        for i in words_db:
            if i.word in words:
                word = SpamWordList.objects.filter(group=group, word=i.word)
                word.count += 1
                word.save()
            else:
                spamword = SpamWordList(word=i.word, group=group)
                spamword.save()

    except Exception as expt:
        print("error occurred:"+expt)


def update_words_level(group):
    """
    change temp and deleted status of words which are greater than critical point to filter status
    :param group: group object
    """
    try:
        words_db = SpamWordList.objects.filter(group=group, status='temp', count__gte=10)
        for i in words_db:
            word = SpamWordList(group=group, word=i.word)
            word.status = 'filter'
            word.save()

        words = SpamWordList.objects.filter(group=group, status='deleted', count__gte=30)
        if words is not None:
            for i in words:
                word = SpamWordList(group=group, word=i.word)
                word.status = 'filter'
                word.save()

    except Exception as expt:
        print("error occurred:"+expt)


def analyze_old_posts(group_id):            # check
    try:
        analyzer = core.AnalysisDiction(True, True)
        group = Group.objects.filter(id=group_id)[0]
        spam_words = SpamWordList.objects.filter(group=group)
        post_data = Post.objects.filter(group=group)

    except Exception as expt:
        print("error occurred:"+expt)


def analyze_old_comments(group_id):         # check
    try:
        analyzer = core.AnalysisDiction(True, True)
        group = Group.objects.filter(id=group_id)[0]

    except Exception as expt:
        print("error occurred:"+expt)


def analyze_spam(data_object):
    analyzer = core.AnalysisDiction(True, True)

    if analyze_post(analyzer, data_object.group, data_object.message) is False:
        return

    add_spam_list(data_object.group, data_object.user, data_object.id, data_object.message, data_object.updated_time)


def delete_sequence(data_object):
    analyzer = core.AnalysisDiction(True, True)

    words = analyze_deleted_spamlist(analyzer, data_object.message)
    add_spam_words(data_object.group, words)
    update_words_level(data_object.group)


def run_app(group, message):      # test-only method
    init_db(group)      # when made group

    analyzer = core.AnalysisDiction(True, True)         # always turn analyzer on

    # save_user_word(group)                 # add spam words from users
    #spam = analyze_posts(analyzer, group, message)      # analyze posts when get it from FB

    #if spam is False:           # if value of spam is false, skip the sequence
    #    return

    add_spam_list(group, message)          # if value of spam if true, add it to spam list

    analyze_restored_spamlist(analyzer, group, message)         # if user restore post from spam list , analyze it

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


