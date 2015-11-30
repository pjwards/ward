import analysis.analysis_core as core
from .models import SpamContentList, SpamWordList

__author__ = 'jeonjiseong'


class Spam:
    """
    Spam part
    """
    def __init__(self, group):
        """
        Initialize Spam class
        """
        self.analyzer = core.AnalysisDiction(True, True)
        self.group = group

    def compare_and_count(self, message, spam_db=None):
        """
        Analyze string data with compare and count words
        :param message: message of post or comment
        :return: analyzed data list
        """
        if spam_db is None:
            spam_db = SpamWordList.objects.filter(group=self.group)     # all spamlist data loads in list
        data_set = [sp.word for sp in spam_db]
        twitter_posmore = self.analyzer.analyzer_twitter(message, 'posmore')
        kkma_nouns = self.analyzer.analyzer_kkma(message, 'nouns')

        result_twi = core.compare_and_make_words(twitter_posmore, data_set)
        result_kkma = core.compare_and_make_words(kkma_nouns, data_set)

        analyzed_words = core.count_in_list(result_twi+result_kkma)     # change better solution

        return analyzed_words

    def update_analysis_level(self, message):
        """
        Add words or update count of words in database
        :param message: message of post or comment
        """
        spam_db = SpamWordList.objects.filter(group=self.group)
        analyzed_words = self.compare_and_count(message, spam_db)
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
                new_word = SpamWordList(word=i[0], group=self.group)
                new_word.save()

    def init_db(self):
        """
        Load standard word from spam.txt to database when initialize database
        """
        data_set = [line.strip() for line in open("analysis/texts/spam.txt", 'r')]
        for i in data_set:
            store_data = SpamWordList(word=i, group=self.group)
            store_data.save()

    def delete_words(self, data_list):
        """
        Change a status of word to delete when it is not appropriate and do not use as standard word
        :param data_list: list of words which are wanted to except from standard word
        """
        for i in data_list:
            try:
                delete_data = SpamWordList.objects.get(word=i, group=self.group)
                delete_data.status = 'deleted'
                delete_data.save()
            except Exception as expt:
                print("error occurred:"+expt)

    def update_standard_word(self):
        """
        add spam.txt words in database of words if those are not in it
        """
        data_set = [line.strip() for line in open("analysis/texts/spam.txt", 'r')]
        db_all = SpamWordList.objects.filter(group=self.group)
        standard = [a.word for a in db_all]
        for j in data_set:
            if j not in standard:
                store_data = SpamWordList(word=j, group=self.group)
                store_data.save()

    def improve_analysis_level(self):           # plus url
        """
        Add words that duplicated in deleted state texts in DB
        """
        spam_db = SpamContentList.objects.filter(status='deleted')
        db_text_list = [sp.text for sp in spam_db]
        words_list = []
        for i in db_text_list:
            twitter_posmore = self.analyzer.analyzer_twitter(i, 'posmore')
            kkma_nouns = self.analyzer.analyzer_kkma(i, 'nouns')
            twitter_word_list = []
            for j in twitter_posmore:
                twitter_word_list.append(j[0])
            merged_list = kkma_nouns + twitter_word_list
            words_list += merged_list

        spam_db2 = SpamWordList.objects.filter(group=self.group)
        db_words = [sp.word for sp in spam_db2]
        duped_words = core.analyze_text(words_list, db_words)
        for j in duped_words:
            if j[1] == 10:
                try:
                    word = SpamWordList.objects.get(word=j[0], group=self.group)
                    word.count += 10
                    word.save()
                except Exception as expt:
                    print("error occurred:"+expt)
            else:
                word = SpamWordList(word=j[0], group=self.group)
                word.save()

        #urls = core.get_url_from_string(string_data)
        #url_list = core.url_duplication_check(data_set,urls)


def add_spam_list(message, group):
    """
    add to spam list
    :param message: message of post or comment
    :param group: group data set
    """
    try:
        spam_data = SpamContentList(group=group, text=message)
        spam_data.save()
    except Exception as expt:
        print("error occurred:"+expt)

        
def delete_spam_list(message, group):
    try:
        spam_data = SpamContentList.objects.get(group=group, text=message)
        spam_data.status = 'deleted'
        spam_data.save()
        Spam(group).update_analysis_level(message)
    except Exception as expt:
        print("error occurred:"+expt)

    ##alarm about spam that deleted in other group
    ##remmadation function


def run_app():      # test-only method
    string = '''slack 에서는 팀초대 api 만 제공하고 있고 이를 쓸려면 써드파티 솔루션들을 써야하는 데. 이를 쓸려면 배포하는 수고를 거쳐야되고. 각 팀마다 배포하는 수고를 거치기보다, 나 혼자 수고하면 되지 않나 싶어서. slack 초대 서비스를 간단히 만들어봤습니다. 물론 Django 로 만들었죠. ㅎㅎ http://festi.kr/zlack/ 에 로그인하고, 그 팀에 대한 slack token 만 등록하면 끝 ~ !!! 현재 2개의 팀이 등록되어있습니다. - django korea, django-girls-seoul'''
    group = ''
    #spam = Spam()
    #spam.init_db()
    '''
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
    '''
    a = SpamWordList.objects.filter(status='temp')
    print(a)
    for i in a:
        print(i.word+"/"+str(i.count)+"/"+i.status)


