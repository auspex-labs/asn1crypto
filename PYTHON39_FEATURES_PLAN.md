# Python 3.9+ Modernization Plan for asn1crypto

## Overview
Modernize asn1crypto to leverage Python 3.9+ features for improved performance, readability, and maintainability.

## Key Modernizations

### 1. Type Hints (PEP 484, 585, 604)
**Benefits:** Better IDE support, type checking, documentation

**Where to apply:**
- Public API methods and functions
- Core classes (`Asn1Value`, `Sequence`, `Choice`, etc.)
- Utility functions in `util.py`, `parser.py`

**Python 3.9+ features:**
```python
# Use built-in generics (no need for typing.List, typing.Dict)
def parse(contents: bytes) -> tuple[int, int, int, bytes, bytes, bytes]:
    ...

# Use | for unions (3.10+) or Optional with from __future__ import annotations
from __future__ import annotations
def load(encoded_data: bytes | None = None) -> Asn1Value:
    ...

# Use collections.abc generics
from collections.abc import Sequence, Mapping
def process(items: Sequence[str]) -> Mapping[str, int]:
    ...
```

### 2. F-Strings (PEP 498)
**Benefits:** Faster, more readable string formatting

**Current usage:** 500+ instances of `%` formatting and `.format()`

**Convert:**
```python
# Old
'%s not greater than %s' % (a, b)
'class_ must be one of 0, 1, 2 or 3, not %s' % class_

# New
f'{a} not greater than {b}'
f'class_ must be one of 0, 1, 2 or 3, not {class_}'
```

### 3. Dict Merge Operator (PEP 584)
**Benefits:** More concise, faster dict merging (Python 3.9+)

```python
# Old
merged = dict(a)
merged.update(b)

# New
merged = a | b

# Old
d = {}
d.update(defaults)
d.update(overrides)

# New
d = defaults | overrides
```

### 4. Walrus Operator (PEP 572)
**Benefits:** More concise code, avoid redundant expressions (Python 3.8+)

```python
# Old
match = pattern.search(text)
if match:
    return match.group(1)

# New
if match := pattern.search(text):
    return match.group(1)

# Old
length = len(data)
if length > 10:
    process(length)

# New
if (length := len(data)) > 10:
    process(length)
```

### 5. Removeprefix/Removesuffix (Python 3.9)
**Benefits:** Clearer intent than slicing

```python
# Old
if s.startswith('prefix_'):
    s = s[7:]  # fragile - magic number

# New
s = s.removeprefix('prefix_')

# Old
if filename.endswith('.py'):
    name = filename[:-3]

# New
name = filename.removesuffix('.py')
```

### 6. Modern Comprehensions and Generators
**Benefits:** More Pythonic, often faster

```python
# Old
output = []
for item in items:
    if item.valid:
        output.append(item.value)

# New
output = [item.value for item in items if item.valid]

# Old
result = {}
for key, value in items:
    result[key] = transform(value)

# New
result = {key: transform(value) for key, value in items}
```

### 7. functools Improvements
**Benefits:** Better caching, decorators

```python
from functools import cache, cached_property

# Python 3.9+ - simpler than lru_cache(maxsize=None)
@cache
def expensive_function(arg):
    ...

# Better than @property + manual caching
class MyClass:
    @cached_property
    def expensive_property(self):
        return calculate()
```

### 8. Standard Library Type Hints (PEP 585)
**Benefits:** No need for `typing` module for basic types (Python 3.9+)

```python
# Old (Python 3.8 and earlier)
from typing import List, Dict, Tuple, Optional, Union

def func(items: List[str]) -> Dict[str, int]:
    ...

# New (Python 3.9+)
def func(items: list[str]) -> dict[str, int]:
    ...

# Can still use typing for complex types
from typing import TypeVar, Generic, Protocol
```

### 9. Improved Error Messages
**Benefits:** Better debugging

```python
# Old
raise ValueError('Invalid value')

# New - include context
raise ValueError(f'Invalid value: {value!r} (expected {expected!r})')
```

### 10. ZoneInfo (Python 3.9)
**Benefits:** Better timezone handling

```python
from zoneinfo import ZoneInfo

# Instead of custom timezone class
dt = datetime(2023, 1, 1, tzinfo=ZoneInfo("UTC"))
```

## Implementation Priority

### Phase 1: High Impact, Low Risk
1. ✅ **F-strings** - Widespread, easy to test
2. ✅ **Removeprefix/removesuffix** - Clear wins
3. ✅ **Dict merge operator** - Clear, simple
4. ✅ **Modern comprehensions** - Where obviously better

### Phase 2: Medium Impact
5. **Type hints on public APIs** - Major documentation/IDE win
6. **Walrus operator** - Selective application where it improves readability
7. **functools.cache/cached_property** - Performance wins

### Phase 3: Careful Application
8. **pathlib** - Only where it simplifies code (may not be many places)
9. **Type hints on internal methods** - Diminishing returns
10. **ZoneInfo** - Review timezone usage first

## Files to Prioritize

### High Value:
- `asn1crypto/core.py` - Most used, biggest file
- `asn1crypto/util.py` - Public utilities
- `asn1crypto/parser.py` - Performance critical
- `asn1crypto/x509.py` - Heavily used

### Medium Value:
- `asn1crypto/keys.py`
- `asn1crypto/algos.py`
- `asn1crypto/cms.py`

### Lower Priority:
- Other specific format files (crl, csr, ocsp, etc.)
- Development/test infrastructure

## Measurements

### Expected Improvements:
- **Performance:** 5-15% faster (f-strings, dict merge, comprehensions)
- **Lines of code:** 3-5% reduction
- **Readability:** Significantly improved
- **Type safety:** IDE autocomplete, static analysis

### Risks:
- **Low** - These are mature Python features
- All changes are backward compatible within Python 3.9+
- Extensive test suite (805 tests) validates correctness

## Example Transformations

### Before (core.py excerpt):
```python
def __repr__(self):
    return '<%s %s %s>' % (type_name(self), id(self), repr(self.dump()))

if tag >= 31:
    header = chr_cls(id_num | 31) + header
else:
    header += chr_cls(id_num | tag)
```

### After:
```python
def __repr__(self) -> str:
    return f'<{type_name(self)} {id(self)} {self.dump()!r}>'

header += chr_cls(id_num | (31 if tag >= 31 else tag))
```

## Testing Strategy

1. Run full test suite after each file
2. Performance benchmarks on critical paths
3. Type checking with mypy (optional but recommended)
4. Manual review of complex changes

## Documentation Updates

- Add "Python 3.9+ Features Used" section to README
- Update CHANGELOG with modernization notes
- Consider adding type stub files (.pyi) for distribution
