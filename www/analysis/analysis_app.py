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
from django.db.models import Q, Avg
from .models import *
from archive.models import Group, Post, Comment, Attachment
from django.utils import timezone
from dateutil import relativedelta as rdelta
from datetime import datetime
from pytz import timezone as tz


def add_anticipate_list(data_object):
    """
    add analyzed article to db
    :param data_object: data object of target article
    """
    newarticle = AnticipateArchive(group=data_object.group)
    newarticle.id = data_object.id
    newarticle.user = data_object.user
    newarticle.message = data_object.message
    newarticle.time = data_object.created_time
    newarticle.save()


def add_words_db(group, word_set, like_count, comment_count):
    """
    add words to word DB
    :param group: group object
    :param word_set: words to save
    """
    for word in word_set:
        if not ArchiveAnalysisWord.objects.filter(group=group, word=word).exists():
            temp = ArchiveAnalysisWord(group=group, word=word, likenum=like_count, commentnum=comment_count)
            temp.weigh = 1 + int(like_count * 0.8) + int(comment_count * 0.5)
            temp.save()
        else:
            exword = ArchiveAnalysisWord.objects.filter(group=group, word=word)[0]
            exword.count += 1
            likes = exword.likenum + like_count
            comments = exword.commentnum + comment_count
            exword.likenum = likes
            exword.commentnum = comments
            exword.weigh = int(exword.count * 0.5) + int(likes * 0.8) + int(comments * 0.5)
            exword.save()


def get_average_like_and_comment(group, is_post=False, is_comment=False):
    """
    get or make average likes and comments count of posts or comments
    :param group: group object
    :return: array of average likes and comments
    """
    try:
        basicdata = AnalysisDBSchema.objects.filter(group=group)[0]
    except IndexError:
        basicdata = None

    if is_post is True:
        if basicdata is not None:
            now = timezone.now()
            diff = now - basicdata.lastupdatetime

            if basicdata.avgpostcomment is 0 and basicdata.avgpostlike is 0:
                args = Post.objects.filter(group=group).aggregate(avglike=Avg('like_count'),
                                                                  avgcomt=Avg('comment_count'))
                avglike = int(round(args['avglike']))
                avgcomt = int(round(args['avgcomt']))

                basicdata.avgpostlike = avglike
                basicdata.avgpostcomment = avgcomt
                basicdata.lastupdatetime = timezone.now()
                basicdata.save()
            elif diff.days >= 1:
                args = Post.objects.filter(group=group).aggregate(avglike=Avg('like_count'),
                                                                  avgcomt=Avg('comment_count'))
                avglike = int(round(args['avglike']))
                avgcomt = int(round(args['avgcomt']))

                basicdata.avgpostlike = avglike
                basicdata.avgpostcomment = avgcomt
                basicdata.lastupdatetime = timezone.now()
                basicdata.save()
            else:
                avglike = basicdata.avgpostlike
                avgcomt = basicdata.avgpostcomment
        else:
            basicdata = AnalysisDBSchema(group=group)
            args = Post.objects.filter(group=group).aggregate(avglike=Avg('like_count'),
                                                              avgcomt=Avg('comment_count'))
            avglike = int(round(args['avglike']))
            avgcomt = int(round(args['avgcomt']))

            basicdata.avgpostlike = avglike
            basicdata.avgpostcomment = avgcomt
            basicdata.lastupdatetime = timezone.now()
            basicdata.save()

    elif is_comment is True:
        if basicdata is not None:
            now = timezone.now()
            diff = now - basicdata.lastupdatetime

            if basicdata.avgcomtcomment is 0 and basicdata.avgcomtlike is 0:
                args = Comment.objects.filter(group=group)\
                    .aggregate(avglike=Avg('like_count'),
                               avgcomt=Avg('comment_count'))
                avglike = int(round(args['avglike']))
                avgcomt = int(round(args['avgcomt']))

                basicdata.avgpostlike = avglike
                basicdata.avgpostcomment = avgcomt
                basicdata.lastupdatetime = timezone.now()
                basicdata.save()
            elif diff.days >= 1:
                args = Comment.objects.filter(group=group)\
                    .aggregate(avglike=Avg('like_count'),
                               avgcomt=Avg('comment_count'))
                avglike = int(round(args['avglike']))
                avgcomt = int(round(args['avgcomt']))

                basicdata.avgpostlike = avglike
                basicdata.avgpostcomment = avgcomt
                basicdata.lastupdatetime = timezone.now()
                basicdata.save()
            else:
                avglike = basicdata.avgcomtlike
                avgcomt = basicdata.avgcomtcomment
        else:
            basicdata = AnalysisDBSchema(group=group)
            args = Comment.objects.filter(group=group)\
                .aggregate(avglike=Avg('like_count'),
                           avgcomt=Avg('comment_count'))
            avglike = int(round(args['avglike']))
            avgcomt = int(round(args['avgcomt']))

            basicdata.avgpostlike = avglike
            basicdata.avgpostcomment = avgcomt
            basicdata.lastupdatetime = timezone.now()
            basicdata.save()

    else:
        return None

    returnarry = [avglike, avgcomt]
    return returnarry


def analyze_hit_article(analyzer, group, article_set, is_post=False, is_comment=False):
    """
    analyze article
    :param analyzer: analyzer for analysis
    :param group: group object
    :param article_set: list of articles
    :return string of status
    """
    for article in article_set:                # better algorithm
        if is_post is True:
            attach = Attachment.objects.filter(post=article)

            if not attach:
                if article.message is None:
                    return "no_message"

                words = core.analyze_articles(analyzer, article.message)
                add_words_db(group, words, article.like_count, article.comment_count)
            else:
                if attach[0].description is not None:
                    message = attach[0].description
                elif attach[0].title is not None:
                    message = attach[0].title
                else:
                    return "no_message"

                words = core.analyze_articles(analyzer, message)
                add_words_db(group, words, article.like_count, article.comment_count)

        elif is_comment is True:
            attach = Attachment.objects.filter(comment=article)

            if not attach:
                if article.message is None:
                    return "no_message"

                words = core.analyze_articles(analyzer, article.message)
                add_words_db(group, words, article.like_count, article.comment_count)
            else:
                if attach[0].description is not None:
                    message = attach[0].description
                elif attach[0].title is not None:
                    message = attach[0].title
                else:
                    return "no_message"

                words = core.analyze_articles(analyzer, message)
                add_words_db(group, words, article.like_count, article.comment_count)
        else:
            return "no_article"


def analyze_monthly_post():     # analyzer, group
    analyzer = core.AnalysisDiction(True, True)
    group = Group.objects.filter(id=168705546563077)[0]
    # MonthTrendWord.objects.all().delete()

    try:
        groupobjcet = GroupDurations.objects.filter(group=group)[0]
        total_months = (groupobjcet.yeared * 12) + groupobjcet.monthed    # add last month update
        old_time = groupobjcet.oldtimed
    except IndexError:
        old_time = group.get_date_from_oldest_post()
        now_time = timezone.now()
        rd = rdelta.relativedelta(now_time, old_time)
        total_months = (rd.years * 12) + rd.months
        GroupDurations(group=group, yeared=rd.years, monthed=rd.months, lastupdatetime=timezone.now(), oldtimed=old_time).save()

    print(total_months)
    total_months -= 1
    while total_months != 0:
        if old_time.month + 1 > 12:
            old_year = old_time.year + 1
            old_month = 1
        else:
            old_year = old_time.year
            old_month = old_time.month + 1

        temp_time = datetime(year=old_year, month=old_month, day=1)
        target_time = temp_time.replace(tzinfo=tz('UTC'))

        post = Post.objects.filter(group=group, created_time__range=(old_time, target_time))

        if post.count() == 0:
            post = None

        comment = Comment.objects.filter(group=group, created_time__range=(old_time, target_time))

        if comment.count() == 0:
            comment = None

        if post and comment is not None:
            post_dict = {}
            if post is not None:
                for p in post:
                    words = core.analyze_articles(analyzer, p.message)

                    for w in words:
                        if post_dict.get(w) is not None:
                            post_dict[w] += (p.like_count + p.comment_count)
                        else:
                            post_dict[w] = 0

            if comment is not None:
                for c in comment:
                    words = core.analyze_articles(analyzer, c.message)

                    for w in words:
                        if post_dict.get(w) is not None:
                            post_dict[w] += (c.like_count + c.comment_count)
                        else:
                            post_dict[w] = 0

            total_words = 1
            count_value = 1

            for i in post_dict.values():
                if i != 0:
                    total_words += 1
                    count_value += i

            avg = int(count_value/total_words*2)
            print(total_words)
            print(count_value)
            print(avg)
            refinewords = []

            for i in post_dict.items():
                if i[1] > avg:
                    refinewords.append((i[0], i[1]))

            for wd in refinewords:
                if not MonthTrendWord.objects.filter(group=group, datedtime=old_time, word=wd[0]).exists():
                    MonthTrendWord(group=group, datedtime=old_time, word=wd[0], weigh=wd[1]).save()

        old_time = target_time
        total_months -= 1           # target_time is one month before today


def monthly_analyze_feed():      # analyzer, group
    analyzer = core.AnalysisDiction(True, True)
    group = Group.objects.filter(id=168705546563077)[0]
    now = timezone.now()
    time = now - timezone.timedelta(days=30)
    try:
        groupobjcet = MonthlyWords.objects.filter(group=group)[0]
        rd = rdelta.relativedelta(now, groupobjcet.lastfeeddate)
        if rd.days > 1:
            MonthlyWords.objects.all().delete()

            post = Post.objects.filter(group=group, created_time__range=(time, now))

            if post.count() == 0:
                post = None

            comment = Comment.objects.filter(group=group, created_time__range=(time, now))

            if comment.count() == 0:
                comment = None

            if post and comment is not None:
                return False
            else:
                post_dict = {}
                if post is not None:
                    for p in post:
                        words = core.analyze_articles(analyzer, p.message)

                        for w in words:
                            if post_dict.get(w) is not None:
                                post_dict[w] += (p.like_count + p.comment_count)
                            else:
                                post_dict[w] = 0

                if comment is not None:
                    for c in comment:
                        words = core.analyze_articles(analyzer, c.message)

                        for w in words:
                            if post_dict.get(w) is not None:
                                post_dict[w] += (c.like_count + c.comment_count)
                            else:
                                post_dict[w] = 0

                total_words = 1
                count_value = 1

                for i in post_dict.values():
                    if i != 0:
                        total_words += 1
                        count_value += i

                avg = int(count_value/total_words*2)

                refinewords = []

                for i in post_dict.items():
                    if i[1] > avg:
                        refinewords.append((i[0], i[1]))

                for wd in refinewords:
                    if not MonthlyWords.objects.filter(group=group, lastfeeddate=time, word=wd[0]).exists():
                        MonthlyWords(group=group, lastfeeddate=time, word=wd[0], weigh=wd[1]).save()
        else:
            return False
    except IndexError:
        post = Post.objects.filter(group=group, created_time__range=(time, now))

        if post.count() == 0:
            post = None

        comment = Comment.objects.filter(group=group, created_time__range=(time, now))

        if comment.count() == 0:
            comment = None

        if post and comment is not None:
            return False
        else:
            post_dict = {}
            if post is not None:
                for p in post:
                    words = core.analyze_articles(analyzer, p.message)

                    for w in words:
                        if post_dict.get(w) is not None:
                            post_dict[w] += (p.like_count + p.comment_count)
                        else:
                            post_dict[w] = 0

            if comment is not None:
                for c in comment:
                    words = core.analyze_articles(analyzer, c.message)

                    for w in words:
                        if post_dict.get(w) is not None:
                            post_dict[w] += (c.like_count + c.comment_count)
                        else:
                            post_dict[w] = 0

            total_words = 1
            count_value = 1

            for i in post_dict.values():
                if i != 0:
                    total_words += 1
                    count_value += i

            avg = int(count_value/total_words*2)

            refinewords = []

            for i in post_dict.items():
                if i[1] > avg:
                    refinewords.append((i[0], i[1]))

            for wd in refinewords:
                if not MonthlyWords.objects.filter(group=group, lastfeeddate=time, word=wd[0]).exists():
                    MonthlyWords(group=group, lastfeeddate=time, word=wd[0], weigh=wd[1]).save()

            return True


def analyze_feed(analyzer, data_object, group):
    """
    analyze a feed
    :param analyzer: analyzer for analysis
    :param data_object: data object
    :return: words from analyzed feed
    """
    #if data_object.message is not None:
    #    message = data_object.message
    #else:
    #    message = ''

    #if 'attachment' in data_object:
    #    attach = data_object.get('attachment')
    #    if 'description' in attach:
    #        attach_message = attach.get('description')
    #    elif 'title' in attach:
    #        attach_message = attach.get('title')
    #    else:
    #        attach_message = ''
    #else:
    #    attach_message = ''

    message = data_object
    attach_message = ''

    if message is not '':
        message_word_set = core.analyze_articles(analyzer, message)
    else:
        message_word_set = []

    if attach_message is not '':
        attach_word_set = core.analyze_articles(analyzer, attach_message)
    else:
        attach_word_set = []

    temp_set = message_word_set + attach_word_set
    word_set = list(set(temp_set))      # make better algorithm

    word_db = ArchiveAnalysisWord.objects.filter(group=group, weigh__gte=100)
    data_set = [sp.word for sp in word_db]

    arg = ArchiveAnalysisWord.objects.filter(group=group).aggregate(avgweigh=Avg('weigh'))

    return core.analysis_text_by_words(data_set, word_set, arg['avgweigh'])


def analysis_prev_hit_posts(group):
    """
    analysis previous posts that have high likes and comments
    :param group: group object
    """
    avgarry = get_average_like_and_comment(group, is_post=True)           # or Admin manage this directly

    if avgarry is None:
        print("get_average function fail")
        return

    hits = Post.objects.filter(Q(group=group), Q(like_count__gte=avgarry[0]) | Q(comment_count__gte=avgarry[1]))
    # better accuracy

    analyzer = core.AnalysisDiction(True, True)

    analyze_hit_article(analyzer, group, hits, is_post=True)


def analysis_prev_hit_comments(group):
    """
    analysis previous comments that have high likes and comments
    :param group: group object
    """
    avgarry = get_average_like_and_comment(group, is_comment=True)           # or Admin manage this directly

    if avgarry is None:
        print("get_average function fail")
        return

    hits = Comment.objects.filter(Q(group=group), Q(like_count__gte=avgarry[0]) | Q(comment_count__gte=avgarry[1]))

    analyzer = core.AnalysisDiction(True, True)

    analyze_hit_article(analyzer, group, hits, is_comment=True)


def analyze_feed_sequence(data_object):
    """
    analyze article sequence
    :param data_object: data object
    :return: status string
    """
    analyzer = core.AnalysisDiction(True, True)

    if data_object.message is None:
        return "no_message"

    if AnticipateArchive(group=data_object.group, id=data_object.id).exists():
        return "exist"

    arg = ArchiveAnalysisWord.objects.filter(group=data_object.group).aggregate(avgweigh=Avg('weigh'))  # use month word

    result = analyze_feed(analyzer, data_object, arg['avgweigh'])

    if result is False:
        return "no_concern"

    add_anticipate_list(data_object=data_object)
    # after 24hours, delete from list

    return "ok"


def refresh_sequence(group):
    """
    refresh AnalysisDBScheman and comments & likes in words DB
    :param group: group object
    """

    analysis_prev_hit_posts(group)          # consider db init
    analysis_prev_hit_comments(group)       # consider db init


def run_app():
    print('hello')
    group = Group.objects.filter(id=168705546563077)[0]
    analyzer = core.AnalysisDiction(True, True)
    data_object = '1. 노드는 프로그래밍 언어가 아닙니다. 2. 단순히 노드 난이도라고 하면, JavaScript나 V8엔진, RESTful 등 서버 백그라운드를 갖추고 있다는 가정하에 진입장벽이 매우 낮은 편입니다'
    print(analyze_feed(analyzer, data_object, group))
    # AnalysisDBSchema.objects.all().delete()
    # rchiveAnalysisWord.objects.all().delete()
    # analysis_prev_hit_posts(group)

    # analyze old post and comment and spam (make analyzer) - init sequence
    # get new feed
    # check if spam (make analyzer) - feed analyze sequence
    # go to spam app if it is spam
    # go to analysis app if it is not spam
    # analyze feed data and store anticipate db if it will be popular article
    # delete or restore spam sequence (make analyzer)   - spam sequence
    # add anticipate list sequence (make analyzer)  - analysis sequence
    # everyday refresh AnalysisDBSchema
    # everyday refresh words comment & like calculating again
