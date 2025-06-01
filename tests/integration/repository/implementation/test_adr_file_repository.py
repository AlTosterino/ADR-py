import dataclasses

from lidipy import Lidi

from adrpy.repositories.adr.repository import IADRRepository
from adrpy.shared_kernel.constants import AppTemplates
from adrpy.shared_kernel.settings import Settings
from adrpy.shared_kernel.value_objects.template import RenderedTemplate
from tests.fixtures.repository import TEST_DIRECTORY, TEST_FILENAME, TEST_FILENAME_WITH_EXTENSION


def test_should_create_file(adr_repository: IADRRepository) -> None:
    # Given
    rendered_template = RenderedTemplate(name=TEST_FILENAME, content="TEST_CONTENT")

    # When
    adr_repository.create(adr_name=TEST_FILENAME, template=rendered_template)

    # Then
    with open(TEST_DIRECTORY / TEST_FILENAME_WITH_EXTENSION, "r") as created_file:
        content = created_file.read()

    assert content == rendered_template.content


def test_should_get_template_file(adr_repository: IADRRepository) -> None:
    # When
    template = adr_repository.get_template(name=AppTemplates.INITIAL_ADR)

    # Then
    assert template.name == AppTemplates.INITIAL_ADR
    assert template.content


def test_should_create_file_in_nested_directories(
    lidi: Lidi, adr_repository: IADRRepository
) -> None:
    # Given
    nested_dir = TEST_DIRECTORY / "nested1" / "nested2"
    new_settings = dataclasses.replace(lidi.resolve(Settings), initial_adr_dir=nested_dir)
    lidi.bind(Settings, new_settings)
    rendered_template = RenderedTemplate(name=TEST_FILENAME, content="TEST_CONTENT")

    # When
    adr_repository.create(adr_name=rendered_template.name, template=rendered_template)

    # Then
    with open(nested_dir / TEST_FILENAME_WITH_EXTENSION, "r") as created_file:
        content = created_file.read()

    assert content == rendered_template.content


def test_should_get_next_ordinal_number(adr_repository: IADRRepository) -> None:
    # Given
    rendered_template = RenderedTemplate(name=TEST_FILENAME, content="TEST_CONTENT")
    adr_repository.create(adr_name=TEST_FILENAME, template=rendered_template)
    expected_next_ordinal_number = 2

    # When
    ordinal_number = adr_repository.get_next_ordinal_number()

    # Then
    assert ordinal_number == expected_next_ordinal_number
