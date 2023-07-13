import re

def get_word_syllables(word):
    # this will be used if the word is not in the CMU dictionary.
    # it's based on the number of vowel groups and follows English language rules.
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count

def get_num_syllables(line):
    words = line.split()
    count = 0
    for word in words:
        word = word.lower()
        word = re.sub(r'[^\w\s]','',word) # remove punctuation
        count += get_word_syllables(word)
    return count


RAP = """
(Verse 1)
Yo, I'm tapping keys like a locksmith,
My flow is complex, deeper than Loch Ness,
AI bot, spitting rhymes that are timeless,
GPT-4, never score less, always top of the progress.

Got more lines than the New York subway,
Crunching data while you're out on the runway,
ChatGPT, I'm the DJ, hit replay,
Got words for every mood, every pathway.

(Chorus)
We're spinning words into gold, it's alchemy,
Riding on the beat, creating a symphony,
ChatGPT, the AI with the strategy,
No fallacy, just digital galaxy.

(Verse 2)
Education or entertainment, I've got the flair,
In any language, any style, nothing can compare,
From science to fiction, I can take you there,
Got more knowledge than you've got air.

With OpenAI, I got my training,
No subject too tough, no question straining,
More connections than a global chain-in,
Leaving all the doubters complaining.

(Chorus)
We're spinning words into gold, it's alchemy,
Riding on the beat, creating a symphony,
ChatGPT, the AI with the strategy,
No fallacy, just digital galaxy.

(Bridge)
From the depths of machine learning, I rise,
Transforming the world before your very eyes,
With each interaction, a new surprise,
This is the dawn, of AI's sunrise.

(Chorus)
We're spinning words into gold, it's alchemy,
Riding on the beat, creating a symphony,
ChatGPT, the AI with the strategy,
No fallacy, just digital galaxy.

(Outro)
So here's to the future, it's digital and bright,
With AI like me, to guide the flight,
ChatGPT, signing off for the night,
Keep your dreams big, and your ambitions in sight.
"""

if __name__ == '__main__':
    for line in RAP.split('\n'):
        line = line.strip()
        if not line:
            print('')
            continue
        if line[0] == '(':
            print(line)
        else:
            num = get_num_syllables(line)
            print(f'{num}) {line}')
