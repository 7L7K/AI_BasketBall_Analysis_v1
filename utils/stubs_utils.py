import os
import pickle


def save_stub(obj, path):
    """
    Save a Python object to disk using pickle.
    """
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    with open(path, 'wb') as f:
        pickle.dump(obj, f)
    print(f"[INFO] Object saved to: {path}")


def read_stub(path, read=True):
    """
    Load a Python object from a pickle file.
    """
    if read and path and os.path.exists(path):
        with open(path, 'rb') as f:
            obj = pickle.load(f)
        print(f"[INFO] Object loaded from: {path}")
        return obj

    return None
    
