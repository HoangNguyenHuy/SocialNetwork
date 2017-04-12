class const(object):
    class ConstError(TypeError):
        pass  # base exception class

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name %r is not all uppercase' % name)
        self.__dict__[name] = value

class StatusType(const):
    Public=1
    Private=2
    Friend=3
    Custom=4

    # @classmethod
    # def is_valid_type(cls, status_type):
    #     return status_type in [
    #         cls.Public,
    #         cls.Private,
    #         cls.Friend,
    #         cls.Custom
    #     ]