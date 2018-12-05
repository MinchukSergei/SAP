import re

word_regex = re.compile(r'\b(\w+)\b[\s.,:;-?!\'"]*')
just_word_regex = re.compile(r'\b(\w+)\b')
last_word_regex = re.compile(r'\b(\w+)\b[.,:;-?!\'"]*$')
first_word_regex = re.compile(r'^[.,:;-?!\'"]*\b(\w+)\b')


def substring(s, pos=0, length=None):
    if length is None:
        length = len(s)
    return '' if length <= 0 else s[pos] + substring(s, pos + 1, length - 1)


def word_count(sentence, word):
    exact_word_regex = re.compile(r'\b' + word + r'\b')
    match = exact_word_regex.search(sentence)
    return 0 if not match else 1 + word_count(sentence[match.end():], word)


def contains_duplicates(s, word=None):
    word_match = just_word_regex.search(s)
    if not word_match:
        return False
    if word is None:
        exact_word_regex = re.compile(r'\b' + word_match.group(1) + r'\b')
        exact_word_match = exact_word_regex.search(s[word_match.end() + 1:])
        word = None if not exact_word_match else exact_word_match.group(0)

    return True if word_match.group(1) == word else contains_duplicates(s[word_match.end():], word)


def word_replace(s, replace, word):
    start = s.find(replace)
    return s if start < 0 else s[:start] + word + word_replace(s[start + len(replace):], replace, word)


def sentence_reverse(s1):
    word_match = word_regex.search(s1)
    return s1.strip() if not word_match else sentence_reverse(s1[word_match.end():] + ' ') + s1[word_match.start(): word_match.end()]


def word_includes_count(text, word):
    pos = text.find(word)
    return 0 if pos == -1 or not word else 1 + word_includes_count(text[pos + 1:], word)


def sentence_intersects(s1, s2):
    word_match1 = word_regex.search(s1)
    word_match2 = word_regex.search(s2)

    if not word_match1 or not word_match2:
        return False

    return word_match1.group(1) == word_match2.group(1) or sentence_intersects(s1[word_match1.end():], s2) or sentence_intersects(s1, s2[word_match2.end():])


def word_length(s):
    word_match = word_regex.search(s)
    return 0 if not word_match else 1 + word_length(s[word_match.start() + 1:word_match.end()])


def swap_first_last(s, start=0, end=None):
    end = len(s) if end is None else end
    inner_s = s[start:end]

    fwm = first_word_regex.match(inner_s)
    lwm = last_word_regex.search(inner_s)

    if not fwm and not lwm:
        return s

    if fwm and lwm:
        return swap_first_last(inner_s[lwm.end() - 1] + s[:start] + inner_s[fwm.start() + 1:lwm.end() - 1] + s[end:len(s)] + inner_s[fwm.start()], start + 1, end - 1)
    if fwm:
        return swap_first_last(s[: start] + s[start + 1:] + inner_s[fwm.start()], start, end - 1)
    if lwm:
        return swap_first_last(inner_s[lwm.end() - 1] + s[:start] + inner_s[:lwm.end() - 1] + s[end:len(s)], start + 1, end)


def main():
    print('Test substring function:')
    print(substring('hello world'))
    print(substring('hello world', 0, 5))
    print(substring('hello world', 6, 5))
    print('=' * 25)

    print('Test word_count function:')
    print(word_count('helloworld', 'world'))
    print(word_count('hello world world', 'world'))
    print('=' * 25)

    print('Test contains_duplicates function:')
    print(contains_duplicates('hello world hello'))
    print(contains_duplicates('hello world'))
    print('=' * 25)

    print('Test word_count function:')
    print(word_replace('hello word, big word', 'word', 'world'))
    print(word_replace('hello word, big word', 'hi', 'world'))
    print('=' * 25)

    print('Test sentence_reverse function:')
    print(sentence_reverse('hello python world'))
    print(sentence_reverse('world'))
    print('=' * 25)

    print('Test word_includes_count function:')
    print(word_includes_count('hello helloworld world', 'hello'))
    print(word_includes_count('hello helloworld world', 'world'))
    print('=' * 25)

    print('Test sentence_intersects function:')
    print(sentence_intersects('hello big world', 'hello world'))
    print(sentence_intersects('hello big world', 'hi word'))
    print('=' * 25)

    print('Test word_length function:')
    print(word_length('!hello!'))
    print(word_length('.,!'))
    print('=' * 25)

    print('Test swap_first_last function:')
    print(swap_first_last('python world of Hello'))
    print(swap_first_last('big world'))
    print('=' * 25)


if __name__ == '__main__':
    main()
