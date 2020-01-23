import random

def greeting():
    greeting_list = [
        'Well, hello there citizen, welcome to Niceria!',
        'We\'re very happy to see you here!',
        'Always room for one more! Please wipe your feet as you enter our kingdom.',
        'Open the gates, we\'ve got another one coming in!',
        'Welcome to Niceria! No pressure; enjoy life!',
        'Welcome to our lovely country, Niceria, where everybody says it\'s *nice* seeing ya :)',
        'Niceria welcomes you to a bright future!'
        ]
    return random.choice(greeting_list)
