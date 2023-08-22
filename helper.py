def transform_stats_ppg(data, n=5):
    """ return the top n values based on each position
    """
    unique_position = set(x[2] for x in data)
    result = {}
    for pos in unique_position:
        a = list(filter(lambda x: x[2] == pos, data))
        a = sorted(a, key=lambda x: -x[4])[:n]
        result[pos] = { 
            "NAME": [_[1] + " " + _[6] for _ in a], 
            "PPG": [_[4] for _ in a] 
        }
    return result

def transform_stats_salary(data, n=5):
    """ return the difference in ppg scores based on each position
    """
    unique_position = set(x[2] for x in data)
    result = {}
    for pos in unique_position:
        a = list(filter(lambda x: x[2] == pos, data))
        a = sorted(a, key=lambda x: -x[6])[:n]
        result[pos] = { 
            "NAME": [_[1] for _ in a], 
            "SALARY": [_[6] for _ in a] 
        }
    return result

def transform_stats_avgppg(data):
    """ return the difference in ppg scores based on each position
    """
    unique_position = set(x[2] for x in data)
    result = {}
    for pos in unique_position:
        a = list(filter(lambda x: x[2] == pos, data))
        a = sorted(a, key=lambda x: -x[4])
        lst = [_[4] for _ in a]
        result[pos] = sum(lst)/len(lst) 
    return result

