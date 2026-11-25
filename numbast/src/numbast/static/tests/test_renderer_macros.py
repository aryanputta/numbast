# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import io

import pytest

from numbast.static.renderer import get_shim


@pytest.mark.parametrize(
    ("macro", "expected"),
    [
        ('FOO="bar"', '#define FOO "bar"'),
        (r"ROOT=C:\new", r"#define ROOT C:\new"),
        ("SOME_MACRO=1", "#define SOME_MACRO 1"),
        ("FLAG", "#define FLAG 1"),
    ],
)
def test_get_shim_preserves_macro_text(macro, expected):
    generated = get_shim('"test.cuh"', predefined_macros=[macro])
    namespace = {"io": io, "CUSource": lambda source: source}

    exec(compile(generated, "<generated bindings>", "exec"), namespace)

    assert namespace["shim_defines"] == expected
