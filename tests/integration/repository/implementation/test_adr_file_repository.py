from adrpy.repositories.adr.repository import ADRFileRepository, BaseADRRepository
from adrpy.shared_kernel.constants import AppTemplates
from adrpy.shared_kernel.settings import Settings
from adrpy.shared_kernel.value_objects.template import RenderedTemplate
from lidipy import Lidi

from tests.fixtures.repository import TEST_DIRECTORY, TEST_FILENAME, TEST_FILENAME_WITH_EXTENSION


def test_should_create_file(repo_service: BaseADRRepository) -> None:
    # Given
    rendered_template = RenderedTemplate(name=TEST_FILENAME, content="TEST_CONTENT")

    # When
    repo_service.create(adr_name=TEST_FILENAME, template=rendered_template)

    # Then
    with open(TEST_DIRECTORY / TEST_FILENAME_WITH_EXTENSION, "r") as created_file:
        content = created_file.read()

    assert content == rendered_template.content


def test_should_get_template_file(repo_service: BaseADRRepository) -> None:
    # When
    template = repo_service.get_template(name=AppTemplates.INITIAL_ADR)

    # Then
    assert template.name == AppTemplates.INITIAL_ADR
    assert template.content


def test_should_create_file_in_nested_directories(lidi: Lidi) -> None:
    # Given
    nested_dir = TEST_DIRECTORY / "nested1" / "nested2"
    new_settings = Settings(initial_adr_dir=nested_dir)
    lidi.bind(BaseADRRepository, ADRFileRepository(settings=new_settings))
    rendered_template = RenderedTemplate(name=TEST_FILENAME, content="TEST_CONTENT")

    # When
    lidi.resolve(BaseADRRepository).create(
        adr_name=rendered_template.name, template=rendered_template
    )

    # Then
    with open(nested_dir / TEST_FILENAME_WITH_EXTENSION, "r") as created_file:
        content = created_file.read()

    assert content == rendered_template.content
