from chalice import Chalice
import logging
import json
import random
import re
import os
import sys
import utils

app = Chalice(app_name='alexa-launchmens')
logger = logging.getLogger()
debug = os.environ.get('DEBUG_MODE')
if debug == '1':
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.ERROR)

#mp3
drumrole_mp3 = "soundbank://soundlibrary/musical/amzn_sfx_drum_and_cymbal_01"

@app.lambda_function()
def lambda_handler(event, context):
    request = event['request']
    request_type = request['type']
    session = {}

    if request_type == 'LaunchRequest':
        return questionIntent()
    elif request_type == 'IntentRequest' and 'intent' in request:
        if 'dialogState' in request and request['dialogState'] != 'COMPLETED': 
            logger.info('run DialogDelegate()')
            return onDialogState(request, request['intent'], request['dialogState'])
        else:
            return in_intent(request, session)

def in_intent(request, session):
    intent = request['intent']
    logger.info(str(intent))

    if intent['name'] == 'questionIntent':
        return questionIntent()
    elif intent['name'] == 'AMAZON.HelpIntent':
        return helpIntent()
    elif intent['name'] == 'AMAZON.NavigateHomeIntent':
        return helpIntent()
    elif intent['name'] == 'AMAZON.StopIntent':
        return finishIntent()
    elif intent['name'] == 'AMAZON.CancelIntent':
        return finishIntent()
    elif intent['name'] == 'AMAZON.NoIntent':
        return finishIntent()
    else:
        return questionIntent()


def onDialogState(request, intent, dialogState):
    if dialogState == 'STARTED':
        return utils.DialogDelegate().build()
    if dialogState == 'IN_PROGRESS':
        if 'value' not in intent['slots']['firstSlot']:
            return utils.DialogDelegate().build()
        elif 'value' not in intent['slots']['secondSlot']:
            return utils.DialogDelegate().build()
        elif 'value' not in intent['slots']['thirdSlot']:
            return utils.DialogDelegate().build()
        else:
            return answerIntent(request, intent, intent['slots'])

def finishIntent():
    return utils.OneSpeech(u'お役に立てなくて残念です。またチャレンジしてくださいね。さようなら').build()

def helpIntent():
    return utils.QuestionSpeech(u'ランチメンズです。三つの質問をしますので、三つの回答から一番合うものを選んでください。答えに応じて今日のランチをご提案します。あまり真面目なものではないので参考程度にしてください。はじめますか？', False, '「はい」か「いいえ」で答えてください').build()

def questionIntent():
    return utils.QuestionSpeech(u'ランチメンズです。三つの質問をしますので、三つの回答から一番合うものを選んでください。答えに応じて今日のランチをご提案します。あまり真面目なものではないので参考程度にしてください。準備はよろしいですか？', False, '「はい」か「いいえ」で答えてください').build()

def answerIntent(request, intent, slots):
    logger.info(str(slots))

    try:
        _ans_first = [
            {},
            {"a":"インドカレー", "i":"カレー食っておけば間違いないですよね。ナンにするかライスにするかでまた迷いますね！"},
            {"a":"ラーメンと半チャーハン", "i":"ランチの王道ですよね。半チャーハンがまた憎い。"},
            {"a":"スタミナ定食", "i":"ガッツリ食べてまた昼から頑張りましょう。もちろんライスは大盛りで！"}
        ]
        _ans_second = [
            {},
            {"a":"餃子とライス", "i":"餃子ってなんでこんなにご飯に合うんですかえね。ニンニクの匂いにはご注意を。"},
            {"a":"トンカツ", "i":"豚肉といえばトンカツ、トンカツといえば豚肉ですよね。ライスもお替わりしちゃいましょう。"},
            {"a":"ちゃんこ鍋", "i":"昼からちゃんこを食べてもいいじゃない。どすこい。"}
        ]
        _ans_third = [
            {},
            {"a":"プロテイン", "i":"血となり肉となれタンパク質。炭水化物とかいりません。"},
            {"a":"拾ったおにぎり", "i":"<break time=\"0.5s\" />。。大丈夫でしょうか。。おなか壊さないでくださいね。"},
            {"a":"スニッカーズ", "i":"疲れた脳には糖分が最高ですよね。でも適度に休憩をとってくださいね。。"}
        ]
        _matches = []
        _first = slots['firstSlot']['value']
        _second = slots['secondSlot']['value']
        _third = slots['thirdSlot']['value']
        _matches = [_ans_first[int(_first)], _ans_second[int(_second)], _ans_third[int(_third)]]
        answer = _matches[random.choice(range(1,3))]
        
    except Exception as e:
        answer = {"a":"チキン","i":""}

    logger.info(answer)

    text = '今日のあなたのランチは<break time="0.5s"/>'
    text += '<audio src="%s" />' % drumrole_mp3


    text += u'<prosody rate="105%"><prosody volume="+1dB">' + answer['a'] + 'がオススメです！</prosody></prosody>'
    text += '<break time="0.5s" />' + answer['i'] + '。'
    text += u'<break time="1.0s" />遊んでくれてありがとう。ではまた！'

    return utils.OneSpeech(text).build()
