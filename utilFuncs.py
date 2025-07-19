def convertAmericanStrToDec(strOdds):
    if strOdds:
        odds = int(strOdds.replace('−', '-').replace('+', ''))
        if odds > 0:
            return float(1 + (odds/100)) 
        else:
            return float(1 + (100 / abs(odds)))
    else:
        return None


def convertAmericanIntToDec(odds):
    if odds > 0:
        return float(1 + (odds/100)) 
    else:
        return float(1 + (100 / abs(odds)))
    

def decimalToAmerican(odds):
    if odds >= 2:
        return f"+{int((odds - 1) * 100)}"
    else:
        return f"{int(-100 / (odds - 1))}"
