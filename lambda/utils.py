class BaseSpeech:
    def __init__(self, speech_text, should_end_session, session_attributes=None, reprompt=None):
        """
         引数:
             speech_text: Alexaに喋らせたいテキスト
             should_end_session: このやり取りでスキルを終了させる場合はTrue, 続けるならFalse
            session_attributes: 引き継ぎたいデータが入った辞書
            reprompt:
        """
        
        if session_attributes is None:
            session_attributes = {}

        self._response = {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': '<speak>'+speech_text+'</speak>'
                },
                'shouldEndSession': should_end_session,
            },
        }

        if reprompt is None:
            pass
        else:
            """リプロンプトを追加する"""
            self._response['response']['reprompt'] = {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': '<speak>'+reprompt+'</speak>'
                }
            }

        self.speech_text = speech_text
        self.should_end_session = should_end_session
        self.session_attributes = session_attributes

    def build(self):
        return self._response

class OneSpeech(BaseSpeech):
    """1度だけ発話する(ユーザーの返事は待たず、スキル終了)"""

    def __init__(self, speech_text, session_attributes=None):
        super().__init__(speech_text, True, session_attributes)

class QuestionSpeech(BaseSpeech):
    """発話し、ユーザーの返事を待つ"""

def __init__(self, speech_text, session_attributes=None, reprompt=None):
    super().__init__(speech_text, False, session_attributes, reprompt)

class DialogDelegate(BaseSpeech):

    def __init__(self, speech_text='', session_attributes=None, reprompt=None):
        super().__init__(speech_text, False, session_attributes, reprompt)

    def build(self):
        self._response['response'] = {
                "directives": [{
                    "type": "Dialog.Delegate"
                }]
            }
        return self._response
