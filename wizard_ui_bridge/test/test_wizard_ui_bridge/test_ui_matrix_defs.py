#! /usr/bin/env python3
"""Tests for the validation of matrix form dimensions.

A dimension must not be negative, and the minimum, default and maximum
dimensions must be ordered for both rows and columns.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import FrozenInstanceError

import pytest

from wizard_ui_bridge.matrix_defs import MatrixDimension, MatrixDimensions

_DIM = MatrixDimension


@pytest.mark.parametrize('rows, columns', [(-1, 0), (0, -1), (-2, -3)])
def test_negative_dimension(rows: int, columns: int) -> None:
    """A negative number of rows or columns is rejected."""
    with pytest.raises(ValueError, match='negative'):
        MatrixDimension(rows, columns)


@pytest.mark.parametrize('low, default, high', [
    (_DIM(2, 1), _DIM(1, 1), _DIM(3, 3)),
    (_DIM(1, 2), _DIM(1, 1), _DIM(3, 3)),
    (_DIM(1, 1), _DIM(4, 1), _DIM(3, 3)),
    (_DIM(1, 1), _DIM(1, 4), _DIM(3, 3))])
def test_unordered_dimensions(low: MatrixDimension, default: MatrixDimension,
                              high: MatrixDimension) -> None:
    """Rows or columns outside min <= default <= max are rejected."""
    with pytest.raises(ValueError, match='min <= default <= max'):
        MatrixDimensions(low, high, default)


@pytest.mark.parametrize('low, default, high', [
    (_DIM(0, 0), _DIM(0, 0), _DIM(0, 0)), (_DIM(2, 3), _DIM(2, 3), _DIM(2, 3)),
    (_DIM(1, 1), _DIM(2, 3), _DIM(5, 4))])
def test_ordered_dimensions(low: MatrixDimension, default: MatrixDimension,
                            high: MatrixDimension) -> None:
    """Ordered dimensions, including a fixed shape, are accepted."""
    dims = MatrixDimensions(low, high, default)
    assert (dims.min, dims.max, dims.default) == (low, high, default)


@pytest.mark.parametrize('rows, columns', [(0, 0), (1, 1), (4, 6)])
def test_fixed_dimensions(rows: int, columns: int) -> None:
    """Fixed dimensions have the same min, max and default shape."""
    dims = MatrixDimensions.fixed(rows, columns)
    shape = MatrixDimension(rows, columns)
    assert (dims.min, dims.max, dims.default) == (shape, shape, shape)


@pytest.mark.parametrize('rows, columns', [(-1, 0), (0, -1)])
def test_fixed_negative(rows: int, columns: int) -> None:
    """A negative fixed size is rejected like any other dimension."""
    with pytest.raises(ValueError):
        MatrixDimensions.fixed(rows, columns)


def test_dimension_frozen() -> None:
    """A dimension cannot be changed after it was validated."""
    dim = MatrixDimension(1, 2)
    with pytest.raises(FrozenInstanceError):
        setattr(dim, 'rows', -1)
