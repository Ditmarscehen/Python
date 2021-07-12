from collections import defaultdict
from collections import Counter
import random
import re


def flat_map(f_map, elements):
    return [item for sublist in map(f_map, elements) for item in sublist]


def print_format(__str, *__args):
    print(__str.format(*map(str, __args)))


def ends_sentnece_ending(str_):
    return re.match("[.!?]", str_[-1])


def get_random_weighted(items_):
    return random.choices(list(items_.keys()), weights=items_.values())[0]


def get_random_with_conditions(condition, random_f, parameters):
    for ii in range(2000):
        if condition(string := random_f(parameters)):
            return string
    return ""


file_name = input()
f = open(file_name, "r", encoding="utf-8")
list_of_lines = f.readlines()
f.close()
tokens = list(flat_map(lambda st: st.split(), list_of_lines))
tokens_len = len(tokens)
threegrams = list(zip(tokens, tokens[1:], tokens[2:]))
threegrams_grouped = defaultdict(list)
for h1, h2, t in threegrams:
    threegrams_grouped[(h1, h2)].append(t)

threegrams_grouped = {k: dict(Counter(v)) for k, v in threegrams_grouped.items()}

i = 0
while i < 10:
    sentence = list(get_random_with_conditions(
        lambda p: p[0][0].isupper() and not ends_sentnece_ending(p[0]) and not ends_sentnece_ending(p[1]),
        random.choice, list(threegrams_grouped.keys())))
    for j in range(2):
        s = get_random_with_conditions(lambda q: not ends_sentnece_ending(q), get_random_weighted,
                                       threegrams_grouped[(sentence[-2], sentence[-1])])
        if s == "":
            break
        else:
            sentence.append(s)
    if len(sentence) != 4:
        continue
    while True:
        s = get_random_weighted(threegrams_grouped[(sentence[-2], sentence[-1])])
        sentence.append(s)
        if ends_sentnece_ending(s):
            break
    print(*sentence)
    i += 1
