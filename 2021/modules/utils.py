

def destructure(obj, *params):
    import operator
    return operator.itemgetter(*params)(obj)

def sparse_matrix():
    from collections import defaultdict
    return defaultdict(lambda:0)

class convert():
    @staticmethod
    def to_int(lst):
        return [int(i) for i in lst]
