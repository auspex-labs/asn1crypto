# Focused Python 3.9+ Modernization

## Practical Scope: Top 3 High-Impact Changes

### 1. F-Strings (Performance + Readability)
**Target:** parser.py, util.py, core.py error messages
**Impact:** 10-15% faster string formatting, more readable
**Effort:** Low
**Files:** 3 files, ~50 changes

### 2. Type Hints on Public APIs Only
**Target:** Main public functions: `load()`, `parse()`, `dump()`
**Impact:** Better IDE support, documentation
**Effort:** Low
**Files:** core.py, parser.py, pem.py
**Count:** ~15 function signatures

### 3. functools.cache on Expensive Operations
**Target:** Cached property computations, repeated OID parsing
**Impact:** Performance improvement on repeated operations
**Effort:** Low
**Files:** core.py (cached properties)
**Count:** ~5 locations

## Implementation Plan

### Session 1 (30 min): parser.py modernization
- Convert % formatting to f-strings
- Add type hints to public functions
- Test

### Session 2 (30 min): util.py modernization
- Convert % formatting to f-strings
- Use dict.get() with walrus where appropriate
- Add type hints
- Test

### Session 3 (1 hour): core.py selective improvements
- F-strings in error messages
- Add functools.cache to expensive properties
- Type hints on load(), dump(), parse()
- Test

### Session 4 (30 min): Testing and Documentation
- Full test suite
- Update CHANGELOG
- Commit

## Total Time: 2.5 hours
## Total Impact: Moderate performance gain, significantly better DX
