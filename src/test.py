# import json

# default_settings = { # These will be the default settigns, the settings are not customised
#             'Memory Matrix': {
#                 'Difficulty': 'Medium',
#                 'Parameters': [
#                     [5, 10], # First Trail
#                     [13, 18], # Second Trail
#                     [20, 26] # Third Trail
#                 ]
#             },
#             'Schulte Table': {
#                 'Difficulty': 'Easy',
#                 'Grid Dimension': 4
#             },
#             'Aiming': {
#                 'Difficulty': 'Medium',
#                 'Parameters': [
#                     [10, 50] # time limit in seconds followed by the amount of points awarded per target 
#                 ]
#             }
#         }

# with open('src/setting save files/default_settings.txt', 'w') as file:
#     json.dump(default_settings, file)

# with open('src/setting save files/default_settings.txt') as file:
#     settings = json.load(file)
#     for entry in settings.items():
#         print(entry)

# asdf = {
#     'test': 'asdf'
# }
# asdf['new'] = {'difficulty': 'sus'}
# print(asdf)

import os

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return 'sius'
            

print(find('equa_settings.txt', 'src/setting save files'))