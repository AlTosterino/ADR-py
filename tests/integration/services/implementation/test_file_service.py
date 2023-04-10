from pathlib import Path
from typing import Iterator

import pytest
from adrpy.services.file.base import BaseFileService
from adrpy.services.file.service import FileService
from adrpy.shared_kernel.value_objects.template import File
from injector import Injector

TEST_DIRECTORY = Path(__file__).parent / "testdir"
TEST_FILENAME = "testfile"


@pytest.fixture()
def file_service(injector: Injector) -> Iterator[BaseFileService]:
    original_binding = injector.binder.get_binding(BaseFileService)
    injector.binder.bind(BaseFileService, to=FileService)
    yield injector.get(BaseFileService)
    injector.binder.bind(BaseFileService, to=original_binding)


@pytest.fixture(scope="module", autouse=True)
def remove_test_file() -> Iterator[None]:
    yield
    import shutil

    shutil.rmtree(TEST_DIRECTORY, ignore_errors=True)


def test_should_create_file(file_service: BaseFileService) -> None:
    # Given
    file_template = File(path=TEST_DIRECTORY, content="TEST_CONTENT")

    # When
    file_service.create_file(
        path=file_template.path, filename=TEST_FILENAME, content=file_template.content
    )

    # Then
    with open(file_template.path / TEST_FILENAME, "r") as created_file:
        content = created_file.read()

    assert content == file_template.content


def test_should_get_created_file(file_service: BaseFileService) -> None:
    # Given
    file_template = File(path=TEST_DIRECTORY, content="TEST_CONTENT")

    # When
    file_service.create_file(
        path=file_template.path, filename=TEST_FILENAME, content=file_template.content
    )

    # Then
    created_file_path = file_template.path / TEST_FILENAME
    created_file = file_service.get_file(path=file_template.path / TEST_FILENAME)
    assert created_file.path == created_file_path
    assert created_file.content == file_template.content


def test_should_create_file_in_nested_directories(file_service: BaseFileService) -> None:
    # Given
    nested_dir = TEST_DIRECTORY / "nested1" / "nested2"
    file_template = File(path=nested_dir, content="TEST_CONTENT")

    # When
    file_service.create_file(
        path=file_template.path, filename=TEST_FILENAME, content=file_template.content
    )

    # Then
    with open(file_template.path / TEST_FILENAME, "r") as created_file:
        content = created_file.read()

    assert content == file_template.content


def test_should_get_created_file_from_nested_directories(file_service: BaseFileService) -> None:
    # Given
    nested_dir = TEST_DIRECTORY / "nested1" / "nested2"
    file_template = File(path=nested_dir, content="TEST_CONTENT")

    # When
    file_service.create_file(
        path=file_template.path, filename=TEST_FILENAME, content=file_template.content
    )

    # Then
    created_file_path = file_template.path / TEST_FILENAME
    created_file = file_service.get_file(path=file_template.path / TEST_FILENAME)
    assert created_file.path == created_file_path
    assert created_file.content == file_template.content
