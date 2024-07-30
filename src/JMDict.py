from bs4 import BeautifulSoup
import coloredlogs
import logging
import time
# import romkan
import MeCab

logger = logging.getLogger(__name__)
coloredlogs.install()


class JMEntry:
    def __init__(self, id, kanji=None, readings=None, definitions=None ):
        self.id = id
        self.kanji = kanji
        self.readings = readings
        self.definitions = definitions

class JMDict:
    def __init__(self, filepath):
        self.filepath = filepath
        self.load()
    

    def load(self):
        start = time.perf_counter()
        logging.info("Loading dictionary...")
        with open(self.filepath, "r", encoding="utf-8") as file:
            root = BeautifulSoup(file.read(), "xml")
            # root = ET.parse(file)

        self.entries = {}
        self.kanji_index = {}
        for entry in root.find_all("entry"):
            entry_num = int(entry.find("ent_seq").text)
            readings = [ ele.find("reb").text for ele in entry.find_all("r_ele")]
            sense_element = entry.find("sense")
            definitions = [ele.text for ele in sense_element.find_all("gloss")]
            kanji = entry.find("keb")
            if(kanji is not None):
                kanji = kanji.text
                self.kanji_index[kanji] = entry_num
            self.entries[entry_num] = JMEntry(entry_num, kanji=kanji, readings=readings, definitions=definitions)
            # print(entry)
        #     try:
        #         kanji_ele = entry.find("k_ele")
        #         reading_ele = entry.find("r_ele")
        #         sense_ele = entry.find("sense")
                
        #         hiragana = reading_ele.find("reb").text
        #         gloss_ele = sense_ele.find("gloss")
        #         if(entry.find("k_ele") is not None):
        #             # romaji = romkan.to_roma(hiragana)
        #             kanji = kanji_ele.find("keb").text
        #             if(kanji in self.entries):
        #                 self.entries[kanji].append((hiragana, gloss_ele.text))
        #             else:
        #                 self.entries[kanji] = [(hiragana, gloss_ele.text)]
                
        #         if(hiragana in self.entries):
        #             self.entries[hiragana].append((hiragana, gloss_ele.text))
        #         else:
        #             self.entries[hiragana] = [(hiragana, gloss_ele.text)]
        #     except:
        #         print(entry.text)
                
                # print(kanji_ele.find("keb").text + " - (" + hiragana + " " + romaji + ") - " + gloss_ele.text)

        self.tokenizer = MeCab.Tagger("")

        elapsed = time.perf_counter() - start
        logging.info("Dictionary Loaded. Took %ds.", elapsed)
        logging.info("%d entries loaded.", len(self.entries))


    def tokenize_search(self, text):
        # print(dict.tokenizer.parse(text))
        for token_info in self.tokenizer.parse(text).strip().split("\n"):
            token_info = token_info.split()
            if(token_info[0] == "EOS"):
                continue
            print(token_info)
            
            # self.search(token_info[0])



    def search(self, kanji):
        if(kanji in self.kanji_index):
            return self.entries[self.kanji_index[kanji]]
            # print(self.entries[kanji])
        else:
            return None
            # print(kanji+" unknown")

    




if __name__ == "__main__":
    dict = JMDict("./data/JMdict_e.xml")
    # dict.search("あの日が私の人生で最高の日だった")
    input_sentence = "あの日が私の人生で最高の日だった"
    # input_sentence = '10日放送の「中居正広のミになる図書館」（テレビ朝日系）で、SMAPの中居正広が、篠原信一の過去の勘違いを明かす一幕があった。'
    # ipadic is well-maintained dictionary #
    print(dict.tokenize_search(input_sentence))
    # mecab_wrapper = JapaneseTokenizer.MecabWrapper(dictType='ipadic')
    # print(mecab_wrapper.tokenize(input_sentence).convert_list_object())
