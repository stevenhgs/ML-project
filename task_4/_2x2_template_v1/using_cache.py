import json

print('loading')
with open('dots_and_boxes/_3x3_try/state_to_best_actions_and_gain_cache_2x2.json', 'r') as fp:
    cache = json.load(fp)
print('loaded')

print(cache['0'])
print(cache['1'])

