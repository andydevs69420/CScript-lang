""" CSObject type prototype
"""


from . import PyLinkInterface


class CSObjectLink(PyLinkInterface):
    
    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = "CSObject"
        self.metadata = ({})





