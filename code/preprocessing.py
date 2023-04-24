def remove_spam(data):
    '''
    Removes duplicated tweets, adds the users to a blacklist and removes all other tweets of theirs.
    '''
    dup_tweets = data[data['text'].duplicated()]
    blacklist = []
    for name in dup_tweets['username']:
        blacklist.append(name)
    blacklist = list(set(blacklist))
    def to_remove(x):
        if x in blacklist:
            return True
        else:
            return False
    data['to_remove'] = data['username'].apply(to_remove)
    mask = data['to_remove']
    data2 = data[~mask]
    return data2

def preprocess(text):
    '''
    Removes usernames and web adresses.
    '''
    new_text = []
    text = str(text)
    text = text.replace("\n", " ")
    for t in text.split(" "):
        t = '' if t.startswith('@') and len(t) > 1 else t
        t = '' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)
