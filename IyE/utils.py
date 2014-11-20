__author__ = 'cristian'


class PostData(dict):
    def __init__(self, req):
        super(PostData, self).__init__(req.POST.dict())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self


def is_empty_elements_dict(d=None, *args):
    if d is None or (type(d) != dict and type(d) != PostData):
        return 'You need to pass a dictionary'
    l = ['Hace falta el campo']
    for item in args:
        if d[item] == '':
            l.append("{0},".format(item))
    if len(l) > 1:
        return ' '.join(l)
    return None