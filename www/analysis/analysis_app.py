__author__ = 'jeonjiseong'

from analysis.analysis_core import AnalysisDiction
import analysis.analysis_core as core
from .models import SpamContent, SpamList


class Spam:
    """
    Spam part
    """
    def __init__(self):
        """
        Initialize Spam class
        """
        self.analyzer = AnalysisDiction(True, True)
        #self.original_data = string_data
        #self.result_data = []

    def compare_and_count(self, string_data):
        """
        Analyze string data with compare and count words
        :param string_data: string data that have to be analyzed
        :return: analyzed data list
        """
        spam_db = SpamList.objects.all()     # all spamlist data loads in list
        dataset = [sp.word for sp in spam_db]
        twipos_more = self.analyzer.analyzer_twitter(string_data, 'posmore')
        kkma_nouns = self.analyzer.analyzer_kkma(string_data, 'nouns')

        result_twi = core.compare_and_make_words(twipos_more, dataset)
        result_kkma = core.compare_and_make_words(kkma_nouns, dataset)

        analyzed_words = core.count_in_list(result_twi+result_kkma)     # change better solution

        return analyzed_words

    def update_analysis_level(self, analyzed_words):
        """
        Add words or update count of words in database
        :param analyzed_words: analyzed data set
        """
        spam_db = SpamList.objects.all()
        words_s = sorted(analyzed_words)
        temp = []
        for i in words_s:
            for j in spam_db:
                if j.word == i[0]:
                    temp.append(j.word)
                    j.count += i[1]
                    j.save()

        for i in words_s:
            if i[0] not in temp:
                new_word = SpamList(word=i[0])
                new_word.save()

    def init_db(self):
        """
        Load standard word from spam.txt to database when initialize database
        """
        data_set = [line.strip() for line in open("analysis/texts/spam.txt", 'r')]
        for i in data_set:
            store_data = SpamList(word=i)
            store_data.save()

    def delete_words(self, data_list):
        """
        Change a status of word to delete when it is not appropriate and do not use as standard word
        :param data_list: list of words which are wanted to except from standard word
        """
        for i in data_list:
            delete_data = SpamList.objects.get(word=i)
            delete_data.status = 'deleted'
            delete_data.save()

    def update_standard_word(self):
        """
        update spam words in database and this procedure is based on spam.txt
        """
        data_set = [line.strip() for line in open("analysis/texts/spam.txt", 'r')]
        db_all = SpamList.objects.all()
        standard = [a.word for a in db_all]
        for j in data_set:
            if j not in standard:
                store_data = SpamList(word=j)
                store_data.save()

    #def improve_analysis_level

    ##warning sign for same spam content


def run_app():      # test-only method
    string = '''slack 에서는 팀초대 api 만 제공하고 있고 이를 쓸려면 써드파티 솔루션들을 써야하는 데. 이를 쓸려면 배포하는 수고를 거쳐야되고. 각 팀마다 배포하는 수고를 거치기보다, 나 혼자 수고하면 되지 않나 싶어서. slack 초대 서비스를 간단히 만들어봤습니다. 물론 Django 로 만들었죠. ㅎㅎ http://festi.kr/zlack/ 에 로그인하고, 그 팀에 대한 slack token 만 등록하면 끝 ~ !!! 현재 2개의 팀이 등록되어있습니다. - django korea, django-girls-seoul'''
    spam = Spam()
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
    #    urls = core.get_url_from_string(string)
        #if len(urls) != 0:
            # url double problem
    #        url_list = [(u, 1) for u in urls]
    #        analyzed_words += url_list
        spam.update_analysis_level(analyzed_words)

    a = SpamList.objects.all()
    for i in a:
        print(i.word+"/"+str(i.count)+"/"+i.status)

