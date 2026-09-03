from masoniteorm.models import Model as _MasoniteModel

from armaden.framework.facades._registry import get_application


class Model(_MasoniteModel):
    """Base ORM model for armaden applications.

    Extends masoniteorm's Model, overriding connection resolution to pull
    the ConnectionResolver from our framework container instead of masonite's
    load_config() helper. This is the single integration point between our
    framework and masonite's query builder.
    """

    def get_connection_details(self):
        resolver = get_application().container.get('database.resolver')
        return resolver.get_connection_details()
