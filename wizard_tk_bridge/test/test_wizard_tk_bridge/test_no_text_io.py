#! /usr/local/bin/python3
"""Tests for the TextIO object that discards everything written to it."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
from typing import Optional
import pytest
from wizard_tk_bridge._no_text_io import NoTextIO

LONG_TEXT = 'x' * 100000


def test_write_discards() -> None:
    """Test written text is dropped instead of stored, however much."""
    stream = NoTextIO()
    assert stream.write(LONG_TEXT) == len(LONG_TEXT)
    assert stream.write(LONG_TEXT) == len(LONG_TEXT)
    assert stream.getvalue() == ''


def test_writelines_discards() -> None:
    """Test written lines are dropped and nothing is stored."""
    stream = NoTextIO()
    assert stream.writelines(['first\n', 'second\n']) is None
    assert stream.getvalue() == ''


def test_print_target() -> None:
    """Test the stream serves as a print target that shows nothing.

    This is how the wizard bridges use it: a diagnostics stream nobody
    reads, printed to as if it were a real file.
    """
    stream = NoTextIO()
    print('hello', 'world', file=stream)
    assert stream.getvalue() == ''


@pytest.mark.parametrize('offset, whence', [
    (0, io.SEEK_SET), (17, io.SEEK_SET), (5, io.SEEK_CUR), (-3, io.SEEK_END)])
def test_seek_stays_at_start(offset: int, whence: int) -> None:
    """Test seeking anywhere reports position zero, as does telling."""
    stream = NoTextIO()
    stream.write('some text')
    assert stream.seek(offset, whence) == 0
    assert stream.tell() == 0


def test_seek_default_whence() -> None:
    """Test seeking with only an offset reports position zero."""
    assert NoTextIO().seek(42) == 0


@pytest.mark.parametrize('size', [None, 0, 5])
def test_truncate(size: Optional[int]) -> None:
    """Test truncating to any size, or to the position, reports zero."""
    stream = NoTextIO()
    stream.write('some text')
    assert stream.truncate(size) == 0
    assert stream.getvalue() == ''


def test_flush_and_close() -> None:
    """Test flushing and closing leave a usable, still-open stream.

    Both do nothing, so unlike a real stream this one accepts more text
    after it was closed.
    """
    stream = NoTextIO()
    assert stream.flush() is None
    assert stream.close() is None
    assert stream.closed is False
    assert stream.write('after close') == len('after close')


def test_context_manager() -> None:
    """Test the stream is its own context manager and stays open after."""
    with NoTextIO() as stream:
        assert isinstance(stream, NoTextIO)
        stream.write('inside')
    assert stream.closed is False
    assert stream.write('outside') == len('outside')
    assert stream.getvalue() == ''


def test_exit_keeps_error() -> None:
    """Test leaving the context on an error does not swallow that error."""
    stream = NoTextIO()
    with pytest.raises(ValueError, match='inside the block'):
        with stream:
            raise ValueError('inside the block')
    assert stream.getvalue() == ''
