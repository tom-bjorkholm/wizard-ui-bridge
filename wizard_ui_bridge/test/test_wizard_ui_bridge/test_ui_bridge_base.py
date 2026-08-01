#! /usr/bin/env python3
"""Tests for base WizardUiBridge text, integer and path helpers."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from pathlib import Path
from typing import Callable, Optional, Sequence

import pytest

from wizard_ui_bridge import PathAskOptions as PublicPathAskOptions, \
    WizardPathKind as PublicPathKind, WizardUiBridge, TableColumn, TableCell
from wizard_ui_bridge.arg_types import PathAskOptions, \
    WizardPathKind
from wizard_ui_bridge.bridge_helpers import path_answer, INT_ERROR


# A test double implements only the ask methods its tests exercise.
# pylint: disable-next=abstract-method
class _TextBridge(WizardUiBridge):
    """Bridge that feeds scripted text answers to base helper methods."""

    def __init__(self, answers: Sequence[str | int | BaseException]) -> None:
        """Store scripted answers and start with an empty call log."""
        self.answers: list[str | int | BaseException] = list(answers)
        self.calls: list[tuple[str, Optional[str]]] = []

    def _next(self) -> str | int:
        """Return the next scripted answer, raising scripted exceptions."""
        try:
            answer = self.answers.pop(0)
        except IndexError as error:
            raise EOFError('No scripted answer left.') from error
        if isinstance(answer, BaseException):
            raise answer
        return answer

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Return the next scripted answer using ask_text semantics."""
        if sensitive and default is not None:
            raise ValueError('default is not allowed for sensitive input')
        self.calls.append((question, re_ask_reason))
        return _scripted_text(self._next(), nullable, default)

    def show(self, message: str) -> None:
        """Ignore shown messages."""
        _ = message


def _scripted_text(answer: str | int, nullable: bool,
                   default: Optional[str]) -> Optional[str]:
    """Return ask_text semantics for one scripted raw answer."""
    text = answer if isinstance(answer, str) else str(answer)
    if text == '' and default is not None:
        return default
    return None if (nullable and text == '') else text


def test_path_api_exported() -> None:
    """The package root exports the path question API."""
    assert PublicPathAskOptions is PathAskOptions
    assert PublicPathKind is WizardPathKind


_MANDATORY: list[tuple[str, Callable[[WizardUiBridge], object]]] = [
    ('ask_text', lambda bridge: bridge.ask_text('q')),
    ('ask_yes_no', lambda bridge: bridge.ask_yes_no('q', True)),
    ('ask_choice', lambda bridge: bridge.ask_choice('q', choices=('a', 'b'))),
    ('ask_multi', lambda bridge: bridge.ask_multi('q', choices=('a', 'b'))),
    ('ask_table', lambda bridge: bridge.ask_table([TableColumn('c')],
                                                  [[TableCell('v')]], 'q')),
    ('show', lambda bridge: bridge.show('m'))]


@pytest.mark.parametrize('name, call', _MANDATORY)
def test_must_implement(name: str,
                        call: Callable[[WizardUiBridge], object]) -> None:
    """Each method a bridge must implement has no base implementation."""
    with pytest.raises(NotImplementedError, match=name):
        call(WizardUiBridge())


def test_int_default() -> None:
    """An empty integer answer selects the default."""
    bridge = _TextBridge([''])
    assert bridge.ask_int('How many?', default=12) == 12


def test_int_default_range() -> None:
    """An integer default must be inside the allowed range."""
    bridge = _TextBridge([])
    with pytest.raises(AssertionError):
        bridge.ask_int('How many?', min_value=1, max_value=5, default=9)


def test_int_not_number() -> None:
    """An answer that is not an integer re-asks the same question."""
    bridge = _TextBridge(['ten', '10'])
    assert bridge.ask_int('How many?') == 10
    assert bridge.calls == [('How many?', None), ('How many?', INT_ERROR)]


def test_int_nullable() -> None:
    """An empty answer to a nullable integer question reports None."""
    assert _TextBridge(['']).ask_int('How many?', nullable=True) is None


@pytest.mark.parametrize('low, high, rejected, reason', [
    (1, 5, '9', 'Please enter an integer between 1 and 5.'),
    (1, 5, '0', 'Please enter an integer between 1 and 5.'),
    (1, None, '0', 'Please enter an integer at least 1.'),
    (None, 5, '6', 'Please enter an integer at most 5.')])
def test_int_range(low: Optional[int], high: Optional[int], rejected: str,
                   reason: str) -> None:
    """An out-of-range integer re-asks and names the allowed range."""
    bridge = _TextBridge([rejected, '3'])
    assert bridge.ask_int('How many?', min_value=low, max_value=high) == 3
    assert bridge.calls[1] == ('How many?', reason)


@pytest.mark.parametrize('low, high, accepted', [
    (1, 5, '1'), (1, 5, '5'), (1, None, '1'), (None, 5, '5'),
    (None, None, '-7')])
def test_int_in_range(low: Optional[int], high: Optional[int],
                      accepted: str) -> None:
    """The allowed integer range includes both of its bounds."""
    bridge = _TextBridge([accepted])
    result = bridge.ask_int('How many?', min_value=low, max_value=high)
    assert result == int(accepted)


def test_error_file_default() -> None:
    """The base bridge sends validation diagnostics to standard error."""
    assert WizardUiBridge().error_file() is sys.stderr


def _path_case_paths(tmp_path: Path) -> dict[str, Path]:
    """Return existing and missing paths for path validation tests."""
    file_path = tmp_path / 'file.txt'
    file_path.write_text('content', encoding='utf-8')
    dir_path = tmp_path / 'folder'
    dir_path.mkdir()
    return {
        'file': file_path,
        'dir': dir_path,
        'missing_file': tmp_path / 'missing.txt',
        'missing_dir': tmp_path / 'missing_dir'}


@pytest.mark.parametrize(
    'kind, bad_key, good_key, error', [
        (WizardPathKind.EXISTING_FILE, 'missing_file', 'file',
         'does not exist'),
        (WizardPathKind.NON_EXISTING_FILE, 'file', 'missing_file',
         'already exists'),
        (WizardPathKind.FILE, 'dir', 'missing_file', 'not a file'),
        (WizardPathKind.EXISTING_DIR, 'missing_dir', 'dir',
         'does not exist'),
        (WizardPathKind.NON_EXISTING_DIR, 'dir', 'missing_dir',
         'already exists'),
        (WizardPathKind.DIR, 'file', 'missing_dir', 'not a directory')])
def test_path_kind(tmp_path: Path, kind: WizardPathKind, bad_key: str,
                   good_key: str, error: str) -> None:
    """ask_path re-asks until the answer satisfies its path kind."""
    paths = _path_case_paths(tmp_path)
    bridge = _TextBridge([str(paths[bad_key]), str(paths[good_key])])
    options = PathAskOptions(kind=kind)
    assert bridge.ask_path('Path?', options=options) == paths[good_key]
    assert error in (bridge.calls[1][1] or '')


def test_path_nullable() -> None:
    """A nullable empty path answer is reported as None."""
    bridge = _TextBridge([''])
    options = PathAskOptions(nullable=True)
    assert bridge.ask_path('Path?', options=options) is None


def test_path_default(tmp_path: Path) -> None:
    """An empty path answer selects the default path."""
    paths = _path_case_paths(tmp_path)
    options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE,
                             default=paths['file'])
    result = _TextBridge(['']).ask_path('Path?', options=options)
    assert result == paths['file']


def test_path_default_first(tmp_path: Path) -> None:
    """A default beats nullable for an empty path answer, and is checked."""
    paths = _path_case_paths(tmp_path)
    options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE, nullable=True,
                             default=paths['file'])
    assert _TextBridge(['']).ask_path('Path?', options=options) == \
        paths['file']


def test_path_blank_default(tmp_path: Path) -> None:
    """A blank raw answer reports the default, nullable or not."""
    paths = _path_case_paths(tmp_path)
    options = PathAskOptions(nullable=True, default=paths['missing_file'])
    assert path_answer('', options) == (True, paths['missing_file'], None)


def test_path_none_answer() -> None:
    """A bridge reporting no answer at all leaves the path unset."""
    assert path_answer(None, PathAskOptions()) == (True, None, None)


def test_path_empty(tmp_path: Path) -> None:
    """A non-nullable empty path answer is rejected."""
    paths = _path_case_paths(tmp_path)
    bridge = _TextBridge(['', str(paths['file'])])
    assert bridge.ask_path('Path?') == paths['file']
    assert 'enter a path' in (bridge.calls[1][1] or '')


def test_path_unusable(monkeypatch: pytest.MonkeyPatch) -> None:
    """A path whose existence check fails is reported as invalid.

    Some filesystems raise OSError when a path is queried instead of
    reporting that it is absent, so path_answer reports the failure as a
    retry reason rather than letting the error escape.
    """
    def boom(self: Path) -> bool:
        """Fail every existence check with an OSError."""
        _ = self
        raise OSError('unusable')
    monkeypatch.setattr(Path, 'exists', boom)
    options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE)
    done, value, reason = path_answer('some/path', options)
    assert done is False
    assert value is None
    assert reason is not None and 'Invalid path' in reason
