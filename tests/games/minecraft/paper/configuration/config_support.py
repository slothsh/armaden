from __future__ import annotations

from armaden.games.minecraft.paper.configuration.paper_yaml_document import (
    YamlMapping,
    YamlValue,
)


def at(tree: YamlMapping | None, path: tuple[str, ...]) -> YamlValue:
    assert tree is not None, f'missing document for path {path}'

    node: YamlValue = tree

    for key in path:
        assert isinstance(node, dict), f'{key!r} is not a mapping in {path}'
        node = node[key]

    return node
