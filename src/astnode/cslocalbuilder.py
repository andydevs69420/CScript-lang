


from astnode.csspitcode import SpitsCode


class LocalBuilder(SpitsCode):

    LOCALS:int = 0

    def __init__(self):
        super().__init__()
    
    def newlocal(self):
        LocalBuilder.LOCALS += 1
        return LocalBuilder.LOCALS - 1

    def reset(self):
        LocalBuilder.LOCALS = 0

