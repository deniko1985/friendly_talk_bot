import random
import unittest
import numpy as np

from fuzzywuzzy import process
from pymorphy2 import MorphAnalyzer

import config
#from answer import response




class MessageHandler():
    
    @staticmethod
    def handle(sentence):
        raise Exception("Метод Handle не реализован")

class UserMessageHandler(MessageHandler):
        
    @staticmethod
    def handle(sentence):
        if GreetingFarewellHandler.is_greeting_or_farewell(sentence):            
            return GreetingFarewellHandler.handle(sentence)            
        else:           
            return DefaultHandler.handle(sentence)            

class GreetingFarewellHandler(MessageHandler):
    with open(config.hello, 'r', encoding='utf-8') as t:
            text_hello = t.read().lower()
    greeting_responses = np.array(text_hello.split('\n'))
    
    with open(config.bye, 'r', encoding='utf-8') as t:
            text_bye = t.read().lower()
    farewell_responses = np.array(text_bye.split('\n'))

#    with open(config.answer, 'r', encoding='utf-8') as t:
#            text_answer = t.read()
#    answer_responses = np.array(text_answer.split('\n'))

    @staticmethod
    def handle(sentence):        
        if GreetingFarewellHandler.is_greeting(sentence):
            rand_h = random.randint(0, len(GreetingFarewellHandler.greeting_responses))
            return GreetingFarewellHandler.greeting_responses[rand_h]
        else:
            rand_b = random.randint(0, len(GreetingFarewellHandler.farewell_responses))
            return GreetingFarewellHandler.farewell_responses[rand_b]

    @staticmethod
    def is_greeting(sentence):
        ma = MorphAnalyzer()
        m = ma.parse(sentence)[0].normal_form
        phrase = process.extractOne(m, GreetingFarewellHandler.greeting_responses)
        return phrase[1] >= 90
    
    @staticmethod
    def is_farewell(sentence):
        ma = MorphAnalyzer()
        m = ma.parse(sentence)[0].normal_form
        phrase_b = process.extractOne(m, GreetingFarewellHandler.farewell_responses)
        return phrase_b[1] >= 90
    
    @staticmethod
    def is_greeting_or_farewell(sentence):
        return GreetingFarewellHandler.is_greeting(sentence) or GreetingFarewellHandler.is_farewell(sentence)

class DefaultHandler(MessageHandler):

    @staticmethod
    def handle(sentence):        
        #return response(sentence)
        return ('Я пока не знаю, как ответить')

if __name__ == '__main__':
    
    class TestCompare (unittest.TestCase):    
        
        def test_positive(self):
            self.assertEqual(GreetingFarewellHandler.is_greeting('Привет!'), (True))  
            self.assertEqual(GreetingFarewellHandler.is_greeting('Приветствую'), (True))
            self.assertEqual(GreetingFarewellHandler.is_greeting('Здравствуй'), (True))  

        def test_negative(self):                    
            self.assertEqual(GreetingFarewellHandler.is_greeting('Пррривееееееет!'), (True))  
            self.assertEqual(GreetingFarewellHandler.is_greeting('привеутьствовую'), (False))
            self.assertEqual(GreetingFarewellHandler.is_greeting('Здрасте!'), (False))  
            self.assertEqual(GreetingFarewellHandler.is_greeting('Здорова!'), (False))
            self.assertEqual(GreetingFarewellHandler.is_greeting('здрасте'), (True))  

    unittest.main()
