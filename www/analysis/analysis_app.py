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
""" Provides analysis app class """

import analysis.analysis_core as core
from django.db.models import Q
from .models import ArchiveAnalysisWord, AnticipateArchive, AnalysisDBSchema
from archive.models import Group, Post, Comment, Attachment


def analyze_articles(analyzer, message):
    """
    analyze articles
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


def add_anticipate_list(group, data_object):
    """
    add analyzed article to db
    :param group: group object
    :param data_object: data object of target article
    """
    newarticle = AnticipateArchive(group=group)
    newarticle.id = data_object.id
    newarticle.user = data_object.user
    newarticle.message = data_object.message
    newarticle.time = data_object.created_time
    newarticle.save()


def analysis_prev_hit_posts(group):
    """
    analysis previous posts that have high likes and comments
    :param group: group object
    """
    basicdata = AnalysisDBSchema.objects.filter(group=group)[0]         # consider update time
    posts = Post.objects.filter(group=group)

    avgLike = 0
    avgComt = 0

    if basicdata is not None:                       # need update periodically
        if basicdata.avgpostcomment is not 0 and basicdata.avgpostlike is not 0:
            likes = 0
            comments = 0
            counts = posts.count()

            for apost in posts:
                likes += apost.like_count
                comments += apost.comment_count

            avgLike = int(likes / counts)              # or Admin manage this directly
            avgComt = int(comments / counts)

            basicdata.avgpostcomment = avgComt
            basicdata.avgpostlike = avgLike
            basicdata.save()
        else:
            avgComt = basicdata.avgpostcomment
            avgLike = basicdata.avgpostlike
    else:
        basicdata = AnalysisDBSchema(group=group)

        likes = 0
        comments = 0
        counts = posts.count()

        for apost in posts:
            likes += apost.like_count
            comments += apost.comment_count

        avgLike = int(likes / counts)
        avgComt = int(comments / counts)

        basicdata.avgpostcomment = avgComt
        basicdata.avgpostlike = avgLike
        basicdata.save()

    hits = Post.objects.filter(Q(group=group), Q(like_count__gte=avgLike) | Q(comment_count__gte=avgComt))

    analyzer = core.AnalysisDiction(True, True)

    for article in hits:                # Think about attachments
        words = analyze_articles(analyzer, article.message)
        for word in words:
            if not ArchiveAnalysisWord.objects.filter(group=group, word=word).exists():
                ArchiveAnalysisWord(group=group, word=word).save()
            else:
                exword = ArchiveAnalysisWord.objects.filter(group=group, word=word)[0]
                exword.count += 1
                exword.save()


def analysis_prev_hit_comments(group):
    """
    analysis previous comments that have high likes and comments
    :param group: group object
    """
    basicdata = AnalysisDBSchema.objects.filter(group=group)[0]
    commentlist = Comment.objects.filter(group=group)

    avgLike = 0
    avgComt = 0

    if basicdata is not None:                       # need update periodically
        if basicdata.avgcomtcomment is not 0 and basicdata.avgcomtlike is not 0:
            likes = 0
            comments = 0
            counts = commentlist.count()

            for apost in commentlist:
                likes += apost.like_count
                comments += apost.comment_count

            avgLike = int(likes / counts)              # or Admin manage this directly
            avgComt = int(comments / counts)

            basicdata.avgcomtcomment = avgComt
            basicdata.avgcomtlike = avgLike
            basicdata.save()
        else:
            avgComt = basicdata.avgcomtcomment
            avgLike = basicdata.avgcomtlike
    else:
        basicdata = AnalysisDBSchema(group=group)

        likes = 0
        comments = 0
        counts = commentlist.count()

        for apost in commentlist:
            likes += apost.like_count
            comments += apost.comment_count

        avgLike = int(likes / counts)
        avgComt = int(comments / counts)

        basicdata.avgcomtcomment = avgComt
        basicdata.avgcomtlike = avgLike
        basicdata.save()

    hits = Comment.objects.filter(Q(group=group), Q(like_count__gte=avgLike) | Q(comment_count__gte=avgComt))

    analyzer = core.AnalysisDiction(True, True)

    for article in hits:                # Think about attachments
        words = analyze_articles(analyzer, article.message)
        for word in words:
            if not ArchiveAnalysisWord.objects.filter(group=group, word=word).exists():
                ArchiveAnalysisWord(group=group, word=word).save()
            else:
                exword = ArchiveAnalysisWord.objects.filter(group=group, word=word)[0]
                exword.count += 1
                exword.save()


def run_app():
    print('hello')
