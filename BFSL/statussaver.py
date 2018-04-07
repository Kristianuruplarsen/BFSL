
import pickle
from collections import defaultdict


STATUSDICT = defaultdict(lambda : None)


def _store_statusdict(statusdict):
    ''' Pickles the status data
    '''
    with open('STATUSDATA.pickle', 'wb') as f:
        pickle.dump(dict(statusdict), f, protocol = pickle.HIGHEST_PROTOCOL)



def _load_statusdict(path):
    ''' Loads a saved dict as statusdict
    '''
    return pickle.load(open(path, 'rb'))
