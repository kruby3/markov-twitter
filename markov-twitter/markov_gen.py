import tweepy
import re
from random import randint



class MarkovGen:

    def __init__(self, twitter_handle, prefix_length, max_chars, api):
        self.twitter_handle = twitter_handle
        self.prefix_length = prefix_length
        self.max_chars = max_chars
        self.api = api
        self.dict = dict()
        self.get_user_tweets()


    def get_user_tweets(self):
        current_prefix = CurrentPrefix(self.prefix_length)
        all_tweets = self.api.user_timeline(screen_name=self.twitter_handle, count=200)
        for status in all_tweets:
            current_string = status.text.split()
            for i in range(len(current_string) - 1):
                current_prefix.add(current_string[i])
                self.add_to_dict(str(current_prefix), current_string[i + 1])

    def add_to_dict(self, prefix_string, next_word):
        if self.dict.has_key(prefix_string):
            suffix_list = self.dict.get(prefix_string)
            suffix_list.append(next_word)
            self.dict[prefix_string] = suffix_list
        else:
            suffix_list = [next_word]
            self.dict[prefix_string] = suffix_list

    def generate_text(self):
        current_prefix = CurrentPrefix(self.prefix_length, self.get_starting_words())
        total_string = str(current_prefix).strip()
        running = True
        while running:
            suffix = self.get_suffix(str(current_prefix))
            current_prefix.add(suffix)
            if (len(total_string) + len(suffix) + 1 < self.max_chars):
                total_string += (" " + suffix)
            else:
                running = False
        return self.clean_up(total_string)

    def clean_up(self, astr):
        astr = re.sub(r"(?:\@|https?\://)\S+", "", astr)
        astr = self.trim(astr)
        astr = astr[:1].upper() + astr[1:]
        return astr

    def trim(self, astr):
        last_period = astr.rfind('.')
        last_exclamation = astr.rfind('!')
        last_punc = max(last_period, last_exclamation)
        return astr[:last_punc + 1]

    def get_starting_words(self):
        size = len(self.dict) - 1
        random_index = randint(0, size)
        keys = self.dict.keys();
        return keys[random_index]

    def get_suffix(self, current_prefix):
        if not self.dict.has_key(current_prefix):
            current_prefix = self.get_starting_words()
        suffixes = self.dict[current_prefix]
        random_index = randint(0, len(suffixes) - 1)
        return suffixes[random_index]




class CurrentPrefix:
    def __init__(self, prefix_length, start_string=None):
        self.prefix_length = prefix_length
        self.word_list = self.create_init_list()

        if start_string is not None:
            word_list = start_string.split()
            for i in range(len(word_list)):
                self.add(word_list[i])

    def add(self, word):
        word = word.strip();
        for c in word:
            if ord(c) > 128:
                word = ""
                break
        for i in range(self.prefix_length - 1):
            self.word_list[i] = self.word_list[i + 1]

        self.word_list[self.prefix_length - 1] = word

    def create_init_list(self):
        temp_list = list()
        for i in range(self.prefix_length):
            temp_list.append('')
        return temp_list

    def __str__(self):
        the_string = self.word_list[0]
        for i in range(1, self.prefix_length):
            if self.word_list[i]:
                the_string += " " + self.word_list[i]
        return the_string
