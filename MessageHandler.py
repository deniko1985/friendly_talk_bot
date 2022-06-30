import random
import unittest
import numpy as np

from fuzzywuzzy import process
from pymorphy2 import MorphAnalyzer




class MessageHandler():
    
    @staticmethod
    def handle(sentence):
        raise Exception("Метод Handle не реализован")

class UserMessageHandler(MessageHandler):
        
    @staticmethod
    def handle(sentence):
        if GreetingFarewellHandler.isGreetingOrFarewell(sentence):            
            return GreetingHandler.handle(sentence)            
        else:           
            return DefaultHandler.handle(sentence)            

class GreetingFarewellHandler(MessageHandler):
    with open('hello.txt', 'r', encoding='utf-8') as t_h:
            text_hello = t_h.read()
    greeting_responses = np.array(text_hello.split('\n'))
    
    with open('bye.txt', 'r', encoding='utf-8') as t_b:
            text_bye = t_b.read()
    farewell_responses = np.array(text_bye.split('\n'))

    @staticmethod
    def handle(sentence):        
        if GreetingFarewellHandler.isGreeting(sentence):
            rand_h = random.randint(0, len(GreetingFarewellHandler.greeting_responses))
            return GreetingFarewellHandler.greeting_responses[rand_h]
        else:
            rand_b = random.randint(0, len(GreetingFarewellHandler.farewell_responses))
            return GreetingFarewellHandler.farewell_responses[rand_b]

    @staticmethod
    def isGreeting(sentence):
        ma = MorphAnalyzer()
        m = ma.parse(sentence)[0].normal_form
        phrase = process.extractOne(m, GreetingFarewellHandler.greeting_responses)
        return phrase[1] >= 90
    
    @staticmethod
    def isFarewell(sentence):
        ma = MorphAnalyzer()
        m = ma.parse(sentence)[0].normal_form
        phrase_b = process.extractOne(m, GreetingFarewellHandler.farewell_responses)
        return phrase_b[1] >= 90
    
    @staticmethod
    def isGreetingOrFarewell(sentence):
        return GreetingFarewellHandler.isGreeting(sentence) or GreetingFarewellHandler.isFarewell(sentence)

class DefaultHandler(MessageHandler):

    @staticmethod
    def handle(sentence):
        return ('Я пока не знаю, как ответить')

if __name__ == '__main__':
    
    class TestCompare (unittest.TestCase):    
        
        def test_positive(self):
            self.assertEqual(GreetingHandler.isGreeting('Привет!'), (True))  
            self.assertEqual(GreetingHandler.isGreeting('Приветствую'), (True))
            self.assertEqual(GreetingHandler.isGreeting('Здравствуй'), (True))  

        def test_negative(self):                    
            self.assertEqual(GreetingHandler.isGreeting('Пррривееееееет!'), (True))  
            self.assertEqual(GreetingHandler.isGreeting('привеутьствовую'), (False))
            self.assertEqual(GreetingHandler.isGreeting('Здрасте!'), (False))  
            self.assertEqual(GreetingHandler.isGreeting('Здорова!'), (False))
            self.assertEqual(GreetingHandler.isGreeting('здрасте'), (True))  

    unittest.main()
