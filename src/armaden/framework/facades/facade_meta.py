from armaden.framework.protocols.facade_protocol import FacadeProtocol


class FacadeMeta(type):
    def __getattr__(cls: type[FacadeProtocol], name: str) -> object:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return getattr(cls.get_facade_root(), name)