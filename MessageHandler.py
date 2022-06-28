import random
import unittest

from fuzzywuzzy import process
from pymorphy2 import MorphAnalyzer




class MessageHandler():
    
    @staticmethod
    def handle(sentence):
        raise Exception("Метод Handle не реализован")

class UserMessageHandler(MessageHandler):
        
    @staticmethod
    def handle(sentence):
        if GreetingHandler.isGreeting(sentence):            
            return GreetingHandler.handle(sentence)            
        else:           
            return DefaultHandler.handle(sentence)            

class GreetingHandler(MessageHandler):
    text = open('hello.txt', 'r', encoding='utf-8').read()
    greeting_responses = text.split('\n')

    @staticmethod
    def handle(sentence):
        r = random.randint(0, len(GreetingHandler.greeting_responses))
        return GreetingHandler.greeting_responses[r]

    @staticmethod
    def isGreeting(sentence):
        ma = MorphAnalyzer()
        m = ma.parse(sentence)[0].normal_form
        phrase = process.extractOne(m, GreetingHandler.greeting_responses)
        return phrase[1] >= 90


class DefaultHandler(MessageHandler):

    @staticmethod
    def handle(sentence):
        return ('Я пока не знаю, как ответить')

if __name__ == '__main__':

    def two_method(i):
            ma = MorphAnalyzer()
            #list = ['Привет', 'приветствую', 'Здравствуйте']
            m = ma.parse(i)[0].normal_form
            sentence = process.extractOne(m, GreetingHandler.greeting_responses)
            return sentence
    
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

        def test_two_method(self):
            self.assertEqual(two_method('Пррривееееееет!'), ('Ееее!', 90))
            self.assertEqual(two_method('привеутьствовую'), ('Привет!', 75))
            self.assertEqual(two_method('здрасте'), ('Здравствуй!', 100))

    unittest.main()
