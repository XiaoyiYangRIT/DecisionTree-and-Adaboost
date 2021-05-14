import re

NUM_FEATURES = 10
features = list(range(NUM_FEATURES))
positive = "nl"
negative = "en"

def formalize(rawData):
    """
    formalize the input text to a list of boolean value
    make it convienent to use in the algorithm
    :param rawData: The raw text from input file
    """
    data = re.sub(r'[^\w]', ' ', rawData).lower().lstrip(' ').rstrip('\n').split()
    result = []
    result.append(checkaa(data))
    result.append(checkthe(data))
    result.append(checkde(data))
    result.append(checkhet(data))
    result.append(checklength(data))
    result.append(checken(data))
    result.append(checkvan(data))
    result.append(checkwerd(data))
    result.append(checked(data))
    result.append(checkto(data))
    return result

# All features:
# 1. has aa in word|nl
# 2. has the in sentence|en
# 3. has de in sentence|nl
# 4. has het in sentence|nl
# 5. word longer than 12 letters|nl
# 6. has en as word|nl
# 7. has van as word|nl
# 8. has werd as word | nl
# 9. has ed at end
# 10. has to as word
def checkaa(data):
    for ward in data:
        for le in range(0, len(ward)):
            if le < len(ward) - 1:
                if ward[le] == "a" and ward[le + 1] == "a":
                    return True
    return False

def checkthe(data):
    for ward in data:
        if ward == "the":
            return False
    return True

def checkde(data):
    for ward in data:
        if ward == "de":
            return True
    return False

def checkhet(data):
    for ward in data:
        if ward == "het":
            return True
    return False

def checklength(data):
    for ward in data:
        if len(ward) > 12:
            return True
    return False

def checken(data):
    for ward in data:
        if ward == "en":
            return True
    return False

def checkvan(data):
    for ward in data:
        if ward == "van":
            return True
    return False

def checkwerd(data):
    for ward in data:
        if ward == "werd":
            return True
    return False

def checked(data):
    for ward in data:
        if len(ward) > 2:
            if ward[-2] + ward[-1] == "ed":
                return False
    return True

def checkto(data):
    for ward in data:
        if ward == "to":
            return False
    return True