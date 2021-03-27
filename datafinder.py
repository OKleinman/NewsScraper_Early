import requests
from bs4 import BeautifulSoup
import positive
import negative
import random


def GetHeadlines():
    addresses = ['https://www.npr.org/', 'https://www.nbcnews.com/', 'https://www.foxnews.com/', 'https://abcnews.go.com/']
    headlines = []

    for address in addresses:
        result = requests.get(address)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')

        if address == addresses[0]:
            featuredValuesNPR = soup.find_all('h3', class_='title')
            for headline in featuredValuesNPR:
                headline = str(headline)
                headline = headline[18:-5]
                headlines.append(headline)

        if address == addresses[1]:
            featuredValuesNBC = soup.find_all('span', class_='tease-card__headline')
            for headline in featuredValuesNBC:
                headline = str(headline)
                headline = headline[35:-7]
                headlines.append(headline)

        if address == addresses[2]:
            featuredValuesFOX = soup.select("h2 a")
            x = 20
            for headline in featuredValuesFOX:
                headline = str(headline)
                if headline[0:37] == '<a href="https://video.foxnews.com/v/' and x >0:
                    headline = headline[53:]
                    headline = headline.replace('<a>','')
                    headline = headline.replace('</a>', '')
                    headline = headline.replace('<>', '')
                    x-=1
                    headlines.append(headline)

        if address == addresses[3]:
            featuredValuesABC = soup.select('div h1 a', class_='black-ln')
            y = 0
            for headline in featuredValuesABC:
                headline = str(headline)
                headline = headline[headline.index('">')+2:-4]
                headline = headline.replace('\n', '')
                if x > 0:
                    headlines.append(headline)
                x+=1

    print(f'{len(headlines)} headlines in database.\n')
    return headlines


def BigTopics():
    topics = []
    connectors = ['the', 'at', 'there', 'some', 'my', 'of', 'be', 'use', 'her', 'than', 'and', 'this', 'an',
                  'would', 'first', 'a', 'have', 'each', 'make', 'water', 'to', 'from', 'which', 'like', 'been', 'in',
                  'or', 'she', 'him', "is", "one", "do", "into", "who", "you", "had", "how", "time", "that", "by",
                  "their", "has", "its", 'word', 'if', 'look now', "he", "but", 'will', 'two', 'find', 'was', 'not',
                  'up', 'more', 'long', 'for', 'what', 'other', 'write', 'down', 'on', "it", 'all', 'about', 'go',
                  'day', 'are', 'were', 'out', 'see', 'did', 'as', 'as', 'we', 'many', 'number', 'get', 'with', 'when',
                  'then', 'no', 'come', 'his', 'your', 'them', 'way', 'made', 'they', 'can', 'these', 'could', 'may',
                  'I', 'said', 'so', 'people', '_', "—", "--", 'part', '', 'become', 'became', "it's", "|", "i'll", 'do',
                  'that’s', 'don’t', 'if', '1st', '2nd', '3rd', '1', '2', '3', 'why', 'where', 'before', 'after', 'day',
                  'week', 'month', 'year', 'days', 'weeks', 'months', 'years', 'over', 'under', 'said', 'says', 'new']
    x = 0
    lastWord = ""
    last2Word = ""
    last3Word = ""
    last4Word = ""
    words = []


    headlines = GetHeadlines()
    wordAmount = 100
    for headline in headlines:
        cutdown = headline.split(" ")
        for w in cutdown:
            words.append(w)
            words.sort()

    for word in words:
        if wordAmount != 0:
            if last4Word == word and last3Word == word and last2Word == word and lastWord == word and word not in topics:
                if word.lower() not in connectors and word[:-1] not in topics and word[-1] != '.' and word[-1] != ',':
                    topics.append(word)
                    wordAmount -= 1
        last4Word = last3Word
        last3Word = last2Word
        last2Word = lastWord
        lastWord = word

    for item in topics:
        if item[:int((len(item)/2))] in topics[topics.index(item)-1]:
            topics.remove(item)

    newHeadlines0 = []
    newHeadlines1 = []
    newHeadlines2 = []
    newHeadlines3 = []


    for tHeadline in GetHeadlines():
        if topics[0] in tHeadline:
            newHeadlines0.append(tHeadline)
        if topics[1] in tHeadline:
            newHeadlines1.append(tHeadline)
        if topics[2] in tHeadline:
            newHeadlines2.append(tHeadline)
        try:
            if topics[3] in tHeadline:
                newHeadlines3.append(tHeadline)
        except IndexError:
            pass


    topicsList = []
    topicsList = sorted(topicsList, key=len)
    topicsList.append(newHeadlines0)
    topicsList.append(newHeadlines1)
    topicsList.append(newHeadlines2)
    topicsList.append(newHeadlines3)


    pos = open("positive.py", 'a')
    neg = open("negative.py", "r")

    finalList = []
    finalHeadlines = ''

    totalWords = []

    print('Topics and sentiment:')
    try:
        for hl in topicsList[3]:
            for hlWord in hl.split():
                totalWords.append(hlWord)

        t3poscount = 0
        for line in positive.poslist:
            line = line.replace(' ', '')
            for sentiment in totalWords:
                if line.lower() == sentiment.lower() or line.lower() + 's' == sentiment.lower() or line.lower() == sentiment.lower() + 's':
                    t3poscount += 1

        t3negcount = 0
        for line in negative.neglist:
            line = line.replace(' ', '')
            for sentiment in totalWords:
                if line.lower() == sentiment.lower() or line.lower() + 's' == sentiment.lower() or line.lower() == sentiment.lower() + 's':
                    t3negcount += 1


        if t3poscount > t3negcount:
            finalList.append(f'1) {topics[3][0].upper() + topics[3][1:]} (positive)')
        elif t3poscount < t3negcount:
            finalList.append(f'1) {topics[3][0].upper() + topics[3][1:]} (negative)')
        else:
            finalList.append(f'1) {topics[3][0].upper() + topics[3][1:]} (neutral)')
        finalHeadlines+=(f'\nA {topics[3][0].upper() + topics[3][1:]} headline: ')
        finalHeadlines+=(topicsList[3][random.randint(0, len(topicsList[3])-1)]) + '\n'

    except IndexError:
        pass


    for hl in topicsList[2]:
        for hlWord in hl.split():
            totalWords.append(hlWord)

    t2poscount = 0
    for line in positive.poslist:
        line = line.replace(' ', '')
        for sentiment in totalWords:
            if line.lower() == sentiment.lower() or line.lower() + 's' == sentiment.lower() or line.lower() == sentiment.lower() + 's':
                t2poscount += 1

    t2negcount = 0
    for line in negative.neglist:
        line = line.replace(' ', '')
        for sentiment in totalWords:
            if line.lower() == sentiment.lower() or line.lower() + 's' == sentiment.lower() or line.lower() == sentiment.lower() + 's':
                t2negcount += 1

    if t2poscount > t2negcount:
        finalList.append(f'2) {topics[2][0].upper() + topics[2][1:]} (positive)')
    elif t2poscount < t2negcount:
        finalList.append(f'2) {topics[2][0].upper() + topics[2][1:]} (negative)')
    else:
        finalList.append(f'2) {topics[2][0].upper() + topics[2][1:]} (neutral)')
    finalHeadlines+=(f'\nA {topics[2][0].upper() + topics[2][1:]} headline: ')
    finalHeadlines+=(topicsList[2][random.randint(0, len(topicsList[2])-1)]) + '\n'

    for hl in topicsList[1]:
        for hlWord in hl.split():
            totalWords.append(hlWord)

    t1poscount = 0
    for line in positive.poslist:
        line = line.replace(' ', '')
        for sentiment in totalWords:
            if line.lower() == sentiment.lower() or line.lower() + 's' == sentiment.lower() or line.lower() == sentiment.lower() + 's':
                t1poscount += 1

    t1negcount = 0
    for line in negative.neglist:
        line = line.replace(' ', '')
        for sentiment in totalWords:
            if line.lower() == sentiment.lower() or line.lower() + 's' == sentiment.lower() or line.lower() == sentiment.lower() + 's':
                t1negcount += 1

    if t1poscount > t1negcount:
        finalList.append(f'3) {topics[1][0].upper() + topics[1][1:]} (positive)')
    elif t1poscount < t1negcount:
        finalList.append(f'3) {topics[1][0].upper() + topics[1][1:]} (negative)')
    else:
        finalList.append(f'3) {topics[1][0].upper() + topics[1][1:]} (neutral)')
    finalHeadlines+=(f'\nA {topics[1][0].upper() + topics[1][1:]} headline: ')
    finalHeadlines+=(topicsList[1][random.randint(0, len(topicsList[1])-1)]) + '\n'

    for hl in topicsList[0]:
        for hlWord in hl.split():
            totalWords.append(hlWord)

    t0poscount = 0
    for line in positive.poslist:
        line = line.replace(' ', '')
        for sentiment in totalWords:
            if line.lower() == sentiment.lower() or line.lower() + 's' == sentiment.lower() or line.lower() == sentiment.lower() + 's':
                t0poscount += 1

    t0negcount = 0
    for line in negative.neglist:
        line = line.replace(' ', '')
        for sentiment in totalWords:
            if line.lower() == sentiment.lower() or line.lower() + 's' == sentiment.lower() or line.lower() == sentiment.lower() + 's':
                t0negcount += 1

    if t0poscount > t0negcount:
        finalList.append(f'4) {topics[0][0].upper() + topics[0][1:]} (positive)')
    elif t0poscount < t0negcount:
        finalList.append(f'4) {topics[0][0].upper() + topics[0][1:]} (negative)')
    else:
        finalList.append(f'4) {topics[0][0].upper() + topics[0][1:]} (neutral)')

    finalHeadlines+=(f'\nA {topics[0][0].upper() + topics[0][1:]} headline: ')
    finalHeadlines+=(topicsList[0][random.randint(0, len(topicsList[0]))])

    pos.close()
    print(finalList), print(finalHeadlines)

BigTopics()