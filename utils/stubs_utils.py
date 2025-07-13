import os
import pickle

def save_stub(stub_path, obj):
    dir_name = os.path.dirname(stub_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    with open(stub_path, 'wb') as f:
        pickle.dump(obj, f)


def read_stub(read_from_stub, stub_path):
    """
    Loads a pickled object if allowed and file exists.
    """
    if read_from_stub and stub_path is not None and os.path.exists(stub_path):
        with open(stub_path, 'rb') as f:
            obj = pickle.load(f)
            return obj
    
    return None
