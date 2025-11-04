# Python 3.9+ Modernization Plan for asn1crypto

## Overview
This document outlines all changes needed to remove Python 2.x and Python 3.0-3.8 compatibility code and modernize the codebase for Python 3.9+.

## Summary of Changes

### 1. Remove Compatibility Modules

#### `asn1crypto/_ordereddict.py` - DELETE ENTIRE FILE
- Python 3.9+ has `collections.OrderedDict` built-in
- Replace imports: `from ._ordereddict import OrderedDict` → `from collections import OrderedDict`

#### `asn1crypto/_types.py` - SIMPLIFY
**Current (Python 2/3):**
```python
if sys.version_info < (3,):
    str_cls = unicode
    byte_cls = str
    int_types = (int, long)
    def bytes_to_list(byte_string):
        return [ord(b) for b in byte_string]
    chr_cls = chr
else:
    str_cls = str
    byte_cls = bytes
    int_types = int
    bytes_to_list = list
    def chr_cls(num):
        return bytes([num])
```

**New (Python 3.9+):**
```python
str_cls = str
byte_cls = bytes
int_types = int
bytes_to_list = list

def chr_cls(num):
    return bytes([num])
```

### 2. Remove `from __future__` Imports

Remove from ALL 22 Python files:
```python
from __future__ import unicode_literals, division, absolute_import, print_function
```

These are default behavior in Python 3.9+.

### 3. Update Core Modules

#### `asn1crypto/core.py`
- Remove: `if sys.version_info <= (3,):` block (lines 66-75)
- Remove: `from cStringIO import StringIO as BytesIO`
- Remove: `range = xrange` and `_PY2 = True`
- Remove ALL `if _PY2:` conditionals (use Python 3 path only)
- Remove: `ord()` calls on bytes (bytes are already integers in Python 3)
- Simplify: `ord(self.contents[0]) if _PY2 else self.contents[0]` → `self.contents[0]`
- Simplify: `chr(value) if _PY2 else bytes((value,))` → `bytes((value,))`

#### `asn1crypto/parser.py`
- Remove: `_PY2 = sys.version_info <= (3,)`
- Remove: `ord()` conditionals
- Simplify: `ord(encoded_data[pointer]) if _PY2 else encoded_data[pointer]` → `encoded_data[pointer]`

#### `asn1crypto/util.py`
- Remove: Entire Python 2 block (lines 37-116) for `int_to_bytes()` and `int_from_bytes()`
- Remove: Custom `timezone` class (lines 118-206)
- Keep only Python 3 versions which use `int.to_bytes()` and `int.from_bytes()`
- Use `datetime.timezone` directly

#### `asn1crypto/pem.py`
- Remove: `if sys.version_info < (3,):` block
- Remove: `from cStringIO import StringIO as BytesIO`
- Use: `from io import BytesIO` only

#### `asn1crypto/_iri.py`
- Remove: `if sys.version_info < (3,):` check
- Remove: `if sys.version_info < (2, 7)` check
- Simplify URL parsing logic for Python 3 only

### 4. Update Configuration Files

#### `setup.py`
**Change classifiers from:**
```python
'Programming Language :: Python :: 2',
'Programming Language :: Python :: 2.6',
'Programming Language :: Python :: 2.7',
'Programming Language :: Python :: 3',
'Programming Language :: Python :: 3.2',
'Programming Language :: Python :: 3.3',
'Programming Language :: Python :: 3.4',
'Programming Language :: Python :: 3.5',
'Programming Language :: Python :: 3.6',
'Programming Language :: Python :: 3.7',
'Programming Language :: Python :: 3.8',
'Programming Language :: Python :: 3.9',
'Programming Language :: Python :: 3.10',
'Programming Language :: Python :: 3.11',
'Programming Language :: Python :: 3.12',
```

**To:**
```python
'Programming Language :: Python :: 3',
'Programming Language :: Python :: 3.9',
'Programming Language :: Python :: 3.10',
'Programming Language :: Python :: 3.11',
'Programming Language :: Python :: 3.12',
'Programming Language :: Python :: 3 :: Only',
```

**Add:**
```python
python_requires='>=3.9',
```

#### `tox.ini`
**Change:**
```ini
[tox]
envlist = py26,py27,py32,py33,py34,py35,py36,py37,py38,py39,py310,py311,py312,pypy
```

**To:**
```ini
[tox]
envlist = py39,py310,py311,py312,py313,pypy39,pypy310
```

#### `.github/workflows/ci.yml`
- Remove all Python 2.6, 2.7, 3.3, 3.6, 3.7, 3.8 jobs
- Keep only Python 3.9, 3.10, 3.11, 3.12, 3.13
- Update PyPy references to pypy-3.9 or newer

#### `.circleci/config.yml`
- Remove Python 2.7 job
- Update Python 3.9 to 3.11 or newer

### 5. Update Documentation

#### `readme.md`
**Change section "Dependencies":**
```markdown
Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12 or pypy.
```

**To:**
```markdown
Python 3.9, 3.10, 3.11, 3.12, 3.13 or PyPy 3.9+.
```

#### `changelog.md`
Add new entry:
```markdown
## 2.0.0

BREAKING CHANGES:
 - Dropped support for Python 2.6, 2.7, and Python 3.0-3.8
 - Minimum required version is now Python 3.9
 - Removed all Python 2 compatibility code
 - Removed `_ordereddict` module (use collections.OrderedDict)
 - Simplified `_types` module for Python 3.9+ only
```

#### `asn1crypto/version.py`
Update version to 2.0.0:
```python
__version__ = '2.0.0'
__version_info__ = (2, 0, 0)
```

### 6. Update Development Tools

#### `requires/ci`
- Remove: `setuptools == 36.8.0 ; python_version == '2.6'`
- Remove: `setuptools == 44.1.1 ; python_version == '2.7'`
- Remove: `setuptools == 18.4 ; python_version == '3.2'`
- Remove: `setuptools == 39.2.0 ; python_version == '3.3'`
- Update setuptools to modern version for Python 3.9+

#### `requires/lint`
- Remove all old Python version conditions
- Update flake8 and related tools to latest versions

#### `requires/coverage`
- Remove old version-specific coverage packages
- Use latest coverage version for Python 3.9+

### 7. Development Scripts

#### `dev/*.py` files
- Remove Python 2.6, 2.7 support code
- Remove old Python version installation scripts
- Simplify importlib code (can use standard Python 3.9+ importlib)

## Specific Code Transformations

### Type Checking
**Before:**
```python
if isinstance(value, int_types):  # int_types = (int, long) in Python 2
```

**After:**
```python
if isinstance(value, int):
```

### String/Bytes Handling
**Before:**
```python
if isinstance(value, str_cls):  # str_cls = unicode in Python 2
```

**After:**
```python
if isinstance(value, str):
```

### Byte Indexing
**Before:**
```python
byte_value = ord(data[0]) if _PY2 else data[0]
```

**After:**
```python
byte_value = data[0]
```

### Range
**Before:**
```python
range = xrange  # Python 2
```

**After:**
```python
# Just use range() - no reassignment needed
```

### Integer to Bytes
**Before (Python 2 in util.py):**
```python
hex_str = '%x' % value
output = hex_str.decode('hex')
```

**After (Python 3.9+):**
```python
# Already implemented correctly in the Python 3 branch
output = value.to_bytes(...)
```

### Dictionary Methods
**Before:**
```python
for key in dict.keys():  # May need special handling in Python 2
```

**After:**
```python
for key in dict:  # Modern Python 3 - keys() is default
```

## Testing Strategy

1. Run full test suite after each major module update
2. Verify no functionality is broken
3. Check that all 805 tests still pass
4. Validate on Python 3.9, 3.10, 3.11, 3.12

## Benefits of This Modernization

1. **Simpler codebase** - Remove ~500+ lines of compatibility code
2. **Easier maintenance** - No more dual code paths
3. **Better performance** - Native Python 3 operations
4. **Modern features** - Can use f-strings, type hints, etc.
5. **Security** - Drop EOL Python versions with security issues

## Files to Modify

### Delete:
- `asn1crypto/_ordereddict.py`

### Major Changes:
- `asn1crypto/core.py`
- `asn1crypto/parser.py`
- `asn1crypto/util.py`
- `asn1crypto/pem.py`
- `asn1crypto/_types.py`
- `asn1crypto/_iri.py`
- `setup.py`
- `tox.ini`
- `.github/workflows/ci.yml`
- `.circleci/config.yml`

### Minor Changes (remove `from __future__` imports):
- All 22 `.py` files in `asn1crypto/`
- All `.py` files in `tests/`
- All `.py` files in `dev/`

## Estimated LOC Reduction

- Remove `_ordereddict.py`: ~136 lines
- Simplify `util.py`: ~80 lines
- Simplify `_types.py`: ~15 lines
- Remove `from __future__` imports: ~60 lines (22 files + tests + dev)
- Remove `_PY2` conditionals in core.py: ~50 lines
- Remove version checks across codebase: ~30 lines

**Total: ~370+ lines of code removed**

## Migration Timeline

1. **Phase 1**: Update configuration and documentation (30 min)
2. **Phase 2**: Remove simple compatibility code (1 hour)
3. **Phase 3**: Update core modules (1-2 hours)
4. **Phase 4**: Testing and validation (30 min)
5. **Phase 5**: Update CI/CD (30 min)

**Total estimated time: 3.5-4.5 hours**

## Backward Compatibility

**⚠️ BREAKING CHANGE**: This is a major version bump (1.5.1 → 2.0.0)

Users on Python 2.x or Python 3.0-3.8 must:
- Stay on asn1crypto 1.5.1 (last compatible version)
- Or upgrade to Python 3.9+

## Rollout Strategy

1. Create a new major version branch
2. Update changelog with breaking changes prominently
3. Tag release as 2.0.0
4. Update PyPI description to note Python 3.9+ requirement
5. Keep 1.x branch available for security patches if needed
