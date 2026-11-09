from __future__ import annotations

from armaden.games.minecraft.paper.enums import PaperEnvironmentVariable


def test_environment_variables_match_the_reference() -> None:
    assert {variable.value for variable in PaperEnvironmentVariable} == {
        'PAPER_VELOCITY_SECRET',
        'PAPER_DEFAULT_CENTRAL_REPOSITORY',
        'MINECRAFT_MANAGEMENT_TLS_KEYSTORE_PASSWORD',
    }


def test_every_environment_variable_has_exactly_one_default_semantics() -> None:
    defaults = set(PaperEnvironmentVariable.defaults())
    unset = set(PaperEnvironmentVariable.unset_by_default())

    assert not defaults & unset
    assert defaults | unset == set(PaperEnvironmentVariable)


def test_defaults_match_the_reference() -> None:
    assert PaperEnvironmentVariable.defaults() == {
        PaperEnvironmentVariable.DEFAULT_CENTRAL_REPOSITORY: 'https://maven-central.storage-download.googleapis.com/maven2',
    }


def test_caution_variables_match_the_reference() -> None:
    assert PaperEnvironmentVariable.caution() == frozenset({
        PaperEnvironmentVariable.DEFAULT_CENTRAL_REPOSITORY,
        PaperEnvironmentVariable.MANAGEMENT_TLS_KEYSTORE_PASSWORD,
    })
