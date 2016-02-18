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
from archive.models import Group, Post, Comment


def init_db(group):
    """
    save standard word from spam.txt to database when initialize database
    :param group: group object
    """
    data_set = [line.strip() for line in open("analysis/texts/spam.txt", 'r')]
    words = SpamWordList.objects.filter(group=group)

    for i in data_set:
        if i in words:
            continue

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


def add_spam_list(group, user, object_id, message, time):
    """
    add to spam list
    :param message: message of post or comment
    :param group: group object
    :param object_id: id of post or comment
    :param user: user object
    :param time: time of object
    """
    spamlist = SpamList()
    spamlist.id = object_id
    spamlist.group = group
    spamlist.user = user
    spamlist.message = message
    spamlist.time = time
    spamlist.status = 'temp'
    spamlist.save()


def delete_content(data_object):
    """
    change status of spam list to deleted
    :param data_object: data object for deleting
    """
    spam_data = SpamList.objects.get(group=data_object.group, id=data_object.id)
    spam_data.status = 'deleted'
    spam_data.save()


def analyze_deleted_spamlist(analyzer, message):
    """
    analyze deleted spam
    :param analyzer: analyzer for analysis
    :param message: message of spam list
    :return: spam words list
    """
    tempTwitter = []
    tempKkma = []

    twitter_posmore = analyzer.analyzer_twitter(message, 'posmore')
    kkma_pos = analyzer.analyzer_kkma(message, 'pos')

    # print(kkma_pos)
    # print(twitter_posmore)

    twiStemList = ['Josa', 'Punctuation', 'Suffix', 'Determiner', 'KoreanParticle', 'Foreign', 'Number']
    kkmaStemList = ['NNG']

    for i in twitter_posmore:
        if i[1] in twiStemList:
            continue

        tempTwitter.append(i[0])

    # print(tempTwitter)

    for i in kkma_pos:
        if i[1] in kkmaStemList:
            tempKkma.append(i[0])

    # print(tempKkma)

    tempword = tempTwitter + tempKkma
    returnword = list(set(tempword))        # remove duplicates

    refineword = []

    # print(returnword)

    for i in returnword:
        if len(i) < 2:
            continue
        refineword.append(i)

    # print(refineword)

    return refineword       # need better refine words


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

    group = Group.objects.filter(id=group_id)[0]
    words_db = SpamWordList.objects.filter(group=group)
    for i in words_db:
        if i.word in words:
            i.count -= 1
            i.save()


def add_spam_words(group, words):
    """
    add words in DB
    :param group: group object
    :param words: spam words list
    """
    words_db = SpamWordList.objects.filter(group=group)

    wordlist = []

    for i in words_db:
        wordlist.append(i.word)

    for i in words:
        if i in wordlist:
            #print("if"+i)
            aword = SpamWordList.objects.filter(group=group, word=i)[0]
            aword.count += 1
            aword.save()
        else:
            #print("else"+i)
            SpamWordList(group=group, word=i).save()


def update_words_level(group):
    """
    change temp and deleted status of words which are greater than critical point to filter status
    :param group: group object
    """
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


def analyze_old_posts(group_id):
    analyzer = core.AnalysisDiction(True, True)
    group = Group.objects.filter(id=group_id)[0]
    post_data = Post.objects.filter(group=group)
    for data in post_data:
        if data.message is None:
            continue

        if analyze_post(analyzer, group, data.message) is False:
            continue

        add_spam_list(group, data.user, data.id, data.message, data.created_time)


def analyze_old_comments(group_id):
    analyzer = core.AnalysisDiction(True, True)
    group = Group.objects.filter(id=group_id)[0]
    comment_data = Comment.objects.filter(group=group)
    for data in comment_data:
        if data.message is None:
            continue

        if analyze_post(analyzer, group, data.message) is False:
            continue

        add_spam_list(group, data.user, data.id, data.message, data.created_time)


def analyze_spam_sequence(data_object):
    analyzer = core.AnalysisDiction(True, True)

    if data_object.message is None:
        return

    if analyze_post(analyzer, data_object.group, data_object.message) is False:
        return

    add_spam_list(data_object.group, data_object.user, data_object.id, data_object.message, data_object.created_time)


def delete_sequence(data_object):
    analyzer = core.AnalysisDiction(True, True)

    words = analyze_deleted_spamlist(analyzer, data_object.message)

    add_spam_words(data_object.group, words)
    update_words_level(data_object.group)


def run_app():      # test-only method      lifecoding - 174499879257223, node - 168705546563077, import analysis.spam_app as spam
    # group_id, message
    group = Group.objects.filter(id=168705546563077)[0]
    print("name is "+group.name)

    #posts = Post.objects.filter(group=group)

    # SpamWordList.objects.all().delete()

    # init_db(group)

    words = SpamWordList.objects.filter()

    # analyze_old_posts(group.id)
    spam = SpamList.objects.filter()

    # analyze_spam_sequence(posts[0])
    delete_sequence(spam[0])
