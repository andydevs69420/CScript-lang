


from system.cssystem import CSSystem


class CSInternal:

    INTERNAL:dict = ({
        "system": CSSystem.SYSTEM
    })
    
    @staticmethod
    def isInternal(_candidate:str):
        return (_candidate in CSInternal.INTERNAL.keys())

    @staticmethod
    def get(_internal:str):
        assert CSInternal.isInternal(_internal), "invalid candidate"
        return CSInternal.INTERNAL[_internal]

