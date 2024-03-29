from chatterbot.logic import LogicAdapter
from flask import Flask, render_template, request

class RecipeBOT(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        ().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['recipe', 'dishes', 'cusine']
        if all(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import requests
        from datetime import date, timedelta
        import json

        recipes=['Daalbhat', 'momo', 'chowmein', 'thukpa','Sandwitch', 'samosa', 'omlet', 'Chicken Curry', 'Egg Curry', 'Burger','Cheese Balls']

        today = date.today()
        days=2
        response=requests.get('https://api.covid19api.com/country/canada/status/confirmed?from={}&to={}'.format(today-timedelta(days),today))
        
        if response.status_code == 200:
            confidence = 1
        else:
            confidence = 0

        if any(x in input_statement.text.split() for x in recipes):

            input_dict = json.loads(response.text)
            output_dict = [y for y in input_dict if y['Province'] == list(set(input_statement.text.split()).intersection(recipes))[0]]
            today_cases=output_dict[-1]['Cases']
            prev_cases=output_dict[-2]['Cases']
            response_statement = Statement(text='Change in cases: {}'.format(today_cases-prev_cases))
        else:
            response_statement = Statement(text='Ask again but please include the Province name too')

        response_statement.confidence = confidence
        return response_statement


