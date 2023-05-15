import json

print('loading')
with open('dots_and_boxes/3x3_try/state_to_best_actions_and_gain_cache_3x3.json', 'r') as fp:
    cache = json.load(fp)
print('loaded')

print(cache['0'])
print(cache['1'])

