from typing import Union, List

from fastapi import FastAPI
import MeCab
# from pydantic import BaseModel
import sys

import JMDict

from contextlib import asynccontextmanager


jp_dict = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load
    global jp_dict
    jp_dict = JMDict.JMDict("../scraper/data/JMdict_e.xml")
    yield
    # Deload
    jp_dict = None



app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/song/{id}/{name}")
def read_item(id: str, q: Union[str, None] = None):


    return {}





def convert_part_of_speech_en(q: str):
    mecab_to_en = {
        "副詞": "adverb",
        "名詞": "noun",
        "助詞": "particle",
        "動詞": "verb",
        "助動詞": "auxillary-verb",
        "代名詞": "pronoun"

    }
    if(q in mecab_to_en):
        return mecab_to_en[q]
    return q



@app.get("/tokenize/jp")
def tokenize_jp(q: str):
    print(sys.version_info)
    tokenizer = MeCab.Tagger("")

    mecab_to_en = {
        "副詞": "adverb",
        "名詞": "noun",
        "助詞": "particle",
        "動詞": "verb",
        "助動詞": "auxillary-verb",
        "代名詞": "pronoun"

    }

    def process_token(token:str):
        if(token == "EOS"):
            return {
                "token": "",
                "type": "eos"
            }
        
        token, info = token.split("\t")
        info = info.split(",")
        # if(len(token) == 1):
        #     if(token[0] == "空白"):
        #         return ["　","空白"]
        #     elif(token[0] == "EOS"):
        #         return ["", "EOS"]
        # return token
        # if(token[0] == "EOS") :
        #     return {
        #         "token": "",
        #         "type": "eos"
        #     }
        # else:
        #     t = token[4].split("-")
        pos = convert_part_of_speech_en(info[0])
        out = {
            "token": token,
            "type": pos
        }
        print(token, info)
        if(pos == "verb"):
            out["base"] = info[7]
        return out
    print(tokenizer.parse(q))
    results = [
        process_token(token)
        # token.split()
        for token in
        tokenizer.parse(q).strip().split("\n")
    ]

    return {
        "result": results
    }




@app.get("/term/jp/{term}")
def read_item(term:str):
    # return { "result": None }

    return { "result": jp_dict.search(term)}

