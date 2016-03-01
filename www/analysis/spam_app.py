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


def analyze_feed_spam(analyzer, group, message):
    """
    Return true if analyzed words and spam words are same
    :param analyzer: analyzer for analysis
    :param group: group object
    :param message: message of post or comment
    :return: true or false
    """
    spam_db = SpamWordList.objects.filter(Q(group=group), Q(status='filter') | Q(status='user'))
    data_set = [sp.word for sp in spam_db]
    word_set = core.analyze_articles(analyzer, message)

    return core.analysis_text_by_words(data_set, word_set)


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
            aword = SpamWordList.objects.filter(group=group, word=i)[0]
            aword.count += 1
            aword.save()
        else:
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
    word_data = SpamWordList.objects.filter(word=word, group=group)[0]
    word_data.status = 'deleted'
    word_data.save()


def analyze_old_posts(group):
    """
    analyze all stored posts in db
    :param group: group object
    """
    analyzer = core.AnalysisDiction(True, True)
    # group = Group.objects.filter(id=group_id)[0]
    post_data = Post.objects.filter(group=group)
    for data in post_data:
        if data.message is None:
            continue

        if analyze_feed_spam(analyzer, group, data.message) is False:
            continue

        add_spam_list(group, data.user, data.id, data.message, data.created_time)


def analyze_old_comments(group):
    """
    analyze all stored comments in db
    :param group: group object
    """
    analyzer = core.AnalysisDiction(True, True)
    # group = Group.objects.filter(id=group_id)[0]
    comment_data = Comment.objects.filter(group=group)
    for data in comment_data:
        if data.message is None:
            continue

        if analyze_feed_spam(analyzer, group, data.message) is False:
            continue

        add_spam_list(group, data.user, data.id, data.message, data.created_time)


def analyze_spam_sequence(data_object):
    """
    analyze article and add spamlist if it is spam
    :param data_object: article object
    :return string about result
    """
    analyzer = core.AnalysisDiction(True, True)

    if data_object.message is None:
        return "no_message"

    if SpamList.objects.filter(group=data_object.group, id=data_object.id).exists():
        return "exist"

    if analyze_feed_spam(analyzer, data_object.group, data_object.message) is False:
        return "no_spam"

    add_spam_list(data_object.group, data_object.user, data_object.id, data_object.message, data_object.created_time)
    return "ok"


def analyze_restored_spamlist(analyzer, group_id, message):
    """
    analyze restored spam
    :param analyzer: analyzer for analysis
    :param group_id: group id
    :param message: message of spam list
    """
    temp_twitter = []

    twitter_posmore = analyzer.analyzer_twitter(message, 'posmore')
    kkma_nouns = analyzer.analyzer_kkma(message, 'nouns')

    for i in twitter_posmore:
        temp_twitter.append(i[0])

    temp_word = temp_twitter + kkma_nouns
    words = list(set(temp_word))

    group = Group.objects.filter(id=group_id)[0]
    words_db = SpamWordList.objects.filter(group=group)
    for i in words_db:
        if i.word in words:
            i.count -= 1
            i.save()


def delete_spam_sequence(data_object):
    """
    analyze deleted spam article from spam list and add spam words to spamwordlist
    :param data_object: deleted article object
    """
    analyzer = core.AnalysisDiction(True, True)

    words = core.analyze_articles(analyzer, data_object.message)

    add_spam_words(data_object.group, words)
    update_words_level(data_object.group)


def run_app():
    # test-only method      lifecoding - 174499879257223, node - 168705546563077, import analysis.spam_app as spam
    group = Group.objects.filter(id=168705546563077)[0]
    print("name is "+group.name)

    posts = Post.objects.filter(group=group)

    # SpamWordList.objects.all().delete()

    # init_db(group)

    # words = SpamWordList.objects.filter()

    # analyze_old_posts(group)
    # analyze_old_comments(group)

    # spam = SpamList.objects.filter()

    analyze_spam_sequence(posts[0])

    # delete_sequence(spam[0])
