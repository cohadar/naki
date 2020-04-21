from наки.__main__ import Контејнер
import dependency_injector.providers as providers


def test_припреми():
    к = Контејнер()
    for дир in к.дирови():
        к.дир.override(providers.Object(дир))
        шпил = к.шпил()
        шпил.припреми()
