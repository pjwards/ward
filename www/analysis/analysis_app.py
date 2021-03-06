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
from archive.models import Post, Comment, Attachment
from django.utils import timezone
from dateutil import relativedelta as rdelta


def add_anticipate_list(data_object, typed):
    """
    add analyzed article to db
    :param data_object: data object of target article
    :param typed: post or comment
    """
    newarticle = AnticipateArchive(group=data_object.group)
    newarticle.id = data_object.id
    newarticle.user = data_object.user
    newarticle.message = data_object.message
    newarticle.time = data_object.created_time
    newarticle.status = typed
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


def analyze_hit_article(group, article_set, is_post=False, is_comment=False):
    """
    analyze article
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

                words = core.analyze_articles(article.message)
                add_words_db(group, words, article.like_count, article.comment_count)
            else:
                if attach[0].description is not None:
                    message = attach[0].description
                elif attach[0].title is not None:
                    message = attach[0].title
                else:
                    return "no_message"

                words = core.analyze_articles(message)
                add_words_db(group, words, article.like_count, article.comment_count)

        elif is_comment is True:
            attach = Attachment.objects.filter(comment=article)

            if not attach:
                if article.message is None:
                    return "no_message"

                words = core.analyze_articles(article.message)
                add_words_db(group, words, article.like_count, article.comment_count)
            else:
                if attach[0].description is not None:
                    message = attach[0].description
                elif attach[0].title is not None:
                    message = attach[0].title
                else:
                    return "no_message"

                words = core.analyze_articles(message)
                add_words_db(group, words, article.like_count, article.comment_count)
        else:
            return "no_article"


def analyze_monthly_post(group, from_date, to_date):
    """
    Make trend words
    :param group: group object
    :param from_date: collect data from this date
    :param to_date: collect data to this date
    :return: if works well return true
    """
    if MonthTrendWord.objects.filter(group=group).exists():
        try:
            group_objcet = MonthTrendWord.objects.filter(group=group, datedtime__range=(from_date, to_date))[0]
        except IndexError:
            post = Post.objects.filter(group=group, created_time__range=(from_date, to_date))

            if post.count() == 0:
                return False

            post_dict = {}
            if post is not None:
                for p in post:
                    words = core.analyze_articles(p.message)

                    for w in words:
                        if post_dict.get(w) is not None:
                            post_dict[w] += (p.like_count + p.comment_count)
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
                MonthTrendWord(group=group, datedtime=from_date, word=wd[0], weigh=wd[1], lastfeeddate=to_date).save()

            return True

        rd = rdelta.relativedelta(to_date, group_objcet.datedtime)

        if rd.days < 30:
            rdt = rdelta.relativedelta(to_date, group_objcet.lastfeeddate)
            if rdt.days > 1:
                MonthTrendWord.objects.filter(group=group, datedtime__range=(from_date, to_date)).delete()
                post = Post.objects.filter(group=group, created_time__range=(from_date, to_date))

                if post.count() == 0:
                    return False

                post_dict = {}
                if post is not None:
                    for p in post:
                        words = core.analyze_articles(p.message)

                        for w in words:
                            if post_dict.get(w) is not None:
                                post_dict[w] += (p.like_count + p.comment_count)
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
                    MonthTrendWord(group=group, datedtime=from_date, word=wd[0], weigh=wd[1], lastfeeddate=to_date).save()

                return True
            else:
                return False
        else:
            return False

    else:
        post = Post.objects.filter(group=group, created_time__range=(from_date, to_date))

        if post.count() == 0:
            return False

        post_dict = {}
        if post is not None:
            for p in post:
                words = core.analyze_articles(p.message)

                for w in words:
                    if post_dict.get(w) is not None:
                        post_dict[w] += (p.like_count + p.comment_count)
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
            MonthTrendWord(group=group, datedtime=from_date, word=wd[0], weigh=wd[1], lastfeeddate=to_date).save()

        return True


def monthly_analyze_feed(group):
    """
    analyze monthly feed
    :param group: group object
    :return: if works well return true
    """
    now = timezone.now()
    time = now - timezone.timedelta(days=70)
    # print(time)
    if MonthlyWords.objects.filter(group=group).exists():
        # print('part1')
        groupobjcet = MonthlyWords.objects.filter(group=group)[0]
        rd = rdelta.relativedelta(now, groupobjcet.lastfeeddate)
        # print(rd.days)
        if groupobjcet is None or rd.days > 7:
            MonthlyWords.objects.filter(group=group).delete()

            post = Post.objects.filter(group=group, created_time__range=(time, now))

            if post.count() == 0:
                return False

            post_dict = {}

            if post is not None:
                for p in post:
                    words = core.analyze_articles(p.message)

                    for w in words:
                        if post_dict.get(w) is not None:
                            post_dict[w] += (p.like_count + p.comment_count)
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
                MonthlyWords(group=group, lastfeeddate=now, word=wd[0], weigh=wd[1]).save()

            return True
        else:
            return False
    else:
        post = Post.objects.filter(group=group, created_time__range=(time, now))

        if post.count() == 0:
            return False

        post_dict = {}
        print(post.count())
        for p in post:
            words = core.analyze_articles(p.message)

            for w in words:
                if post_dict.get(w) is not None:
                    post_dict[w] += (p.like_count + p.comment_count)
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
            MonthlyWords(group=group, lastfeeddate=now, word=wd[0], weigh=wd[1]).save()

        return True


def weekly_analyze_feed(group):
    """
    analyze monthly feed
    :param group: group object
    :return: if works well return true
    """
    now = timezone.now()
    time = now - timezone.timedelta(days=40)
    # print(time)
    if MonthlyWords.objects.filter(group=group).exists():
        # print('part1')
        groupobjcet = MonthlyWords.objects.filter(group=group)[0]
        rd = rdelta.relativedelta(now, groupobjcet.lastfeeddate)

        # print(rd.days)
        if groupobjcet is None or rd.days > 1:
            MonthlyWords.objects.filter(group=group).delete()

            post = Post.objects.filter(group=group, created_time__range=(time, now))

            if post.count() == 0:
                post = None

            comment = Comment.objects.filter(group=group, created_time__range=(time, now))

            if comment.count() == 0:
                comment = None

            if post and comment is None:
                return False
            else:
                post_dict = {}
                if post is not None:
                    for p in post:
                        words = core.analyze_articles(p.message)

                        for w in words:
                            if post_dict.get(w) is not None:
                                post_dict[w] += (p.like_count + p.comment_count)
                            else:
                                post_dict[w] = 0

                if comment is not None:
                    for c in comment:
                        words = core.analyze_articles(c.message)

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
                    MonthlyWords(group=group, lastfeeddate=now, word=wd[0], weigh=wd[1]).save()

                return True
        else:
            return False
    else:
        post = Post.objects.filter(group=group, created_time__range=(time, now))

        if post.count() == 0:
            post = None

        comment = Comment.objects.filter(group=group, created_time__range=(time, now))

        if comment.count() == 0:
            comment = None

        print(post.count())
        print(comment.count())

        if post and comment is None:
            return False
        else:
            post_dict = {}
            if post is not None:
                for p in post:
                    words = core.analyze_articles(p.message)

                    for w in words:
                        if post_dict.get(w) is not None:
                            post_dict[w] += (p.like_count + p.comment_count)
                        else:
                            post_dict[w] = 0

            if comment is not None:
                for c in comment:
                    words = core.analyze_articles(c.message)

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
                MonthlyWords(group=group, lastfeeddate=now, word=wd[0], weigh=wd[1]).save()

            return True


def analyze_feed(data_object):
    """
    analyze a feed
    :param data_object: data object
    :return: words from analyzed feed
    """
    if data_object.message is not None:
        message = data_object.message
    else:
        message = ''

    if 'attachment' in data_object:
        attach = data_object.get('attachment')
        if 'description' in attach:
            attach_message = attach.get('description')
        elif 'title' in attach:
            attach_message = attach.get('title')
        else:
            attach_message = ''
    else:
        attach_message = ''

    # message = data_object
    # attach_message = ''

    if message is not '':
        message_word_set = core.analyze_articles(message)
    else:
        message_word_set = []

    if attach_message is not '':
        attach_word_set = core.analyze_articles(attach_message)
    else:
        attach_word_set = []

    temp_set = message_word_set + attach_word_set
    word_set = list(set(temp_set))      # make better algorithm

    word_db = MonthlyWords.objects.filter(group=data_object.group)
    data_set = [sp.word for sp in word_db]

    return core.analysis_text_by_words(data_set, word_set, 5)


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

    analyze_hit_article(group, hits, is_post=True)


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

    analyze_hit_article(group, hits, is_comment=True)


def analyze_feed_sequence(data_object, typed):
    """
    analyze article sequence
    :param data_object: data object
    :param typed: post or comment
    :return: status string
    """
    if data_object.message is None:
        return "no_message"

    if AnticipateArchive(group=data_object.group, id=data_object.id).exists():
        return "exist"

    # arg = ArchiveAnalysisWord.objects.filter(group=data_object.group).aggregate(avgweigh=Avg('weigh'))

    result = analyze_feed(data_object)

    if result is False:
        return "no_concern"

    add_anticipate_list(data_object=data_object, typed=typed)
    # after 24hours, delete from list

    return "ok"


def post_time_out(group):
    """
    Delete feed data from AnticipateArchive list
    :param group: group object
    """
    now = timezone.now()
    dayago = now - timezone.timedelta(1)
    postlist = AnticipateArchive.objects.filter(group=group, time__lte=dayago)
    for i in postlist:
        i.delete()


def refresh_sequence(group):
    """
    refresh AnalysisDBScheman and comments & likes in words DB
    :param group: group object
    """
    # analysis_prev_hit_posts(group)          # consider db init
    # analysis_prev_hit_comments(group)       # consider db init
    monthly_analyze_feed(group)
    post_time_out(group)


def future_analysis_post(group, data_object, typed):
    """
    analysis feed and enroll future hot issue
    :param group: group object
    :param data_object: data object
    :param typed: post or comment
    :return: if works well return True
    """
    if AnticipateArchive.objects.filter(group=group):
        analyze_feed_sequence(data_object, typed)
    else:
        if typed is 'post':
            now = timezone.now()
            dayago = now - timezone.timedelta(1)
            posts = Post.objects.filter(group=group, created_time__range=(dayago, now))

            if posts is None:
                return False

            for p in posts:
                if p.message is None:
                    continue

                result = analyze_feed(p)

                if result is False:
                    continue

                add_anticipate_list(data_object=p, typed=typed)
        else:
            now = timezone.now()
            dayago = now - timezone.timedelta(1)
            comments = Comment.objects.filter(group=group, created_time__range=(dayago, now))

            if comments is None:
                return False

            for c in comments:
                if c.message is None:
                    continue

                result = analyze_feed(c)

                if result is False:
                    continue

                add_anticipate_list(data_object=c, typed=typed)

        return True


def run_app():
    print('hello')
    message = '초보자들 헷갈리라고 넣는 겁니다 (웃음). 지금의 단계에서는 굳이 이해하려고 하실 필요가 없습니다. 꼭 알고 싶으시다면 "변수는 정보와 실체의 합으로서 존재하는데, test는 변수에 담긴 정보를 의미하고 &test는 변수의 실체를 의미한다" 정도로 생각해 두시면 되겠습니다. 더 쉽게 말하면, int b = 72; 이렇게 값이 72인 변수 b가 있을 때, 우리는 이것을 b라는 상자에 72라는 정보가 담겨 있는 것으로 이해할 수 있습니다. b라고 지정하면 72라는 값을 꺼내 주는 것이고, &b라고 지정하면 72가 담긴 상자를 통째로 건네주는 것입니다. 내용물을 꺼내서 주면 받는 쪽에서는 상자에 접근할 수 없으므로 상자의 내용물을 바꿀 수는 없습니다. 상자를 통째로 주면 받는 쪽에서 상자에 다른 물건을 담아놓을 수 있겠죠.'
    core.analyze_articles(message)
    message = '우려했던 K-알파고가 곧 나올듯 합니다.... :('
    core.analyze_articles(message)
    message = '역시 ..LG'
    core.analyze_articles(message)
    # core.analyze_articles_up(message)
    # print(analyze_feed(analyzer, data_object, group))
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
