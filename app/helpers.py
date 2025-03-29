import os
from collections.abc import Callable
from typing import Any, TypeVar

_TRUE_VALUES = ('true', '1', 'yes')
_FALSE_VALUES = ('false', '0', 'no')
_BOOL_VALUES = _TRUE_VALUES + _FALSE_VALUES
_DEFAULT_VALUE = '_DEFAULT'  # для возможности указать None в качестве значения по умолчанию
T = TypeVar('T', bound=Any)


def _cast_to_bool(value: str) -> bool:
    value = value.lower()
    if value not in _BOOL_VALUES:
        raise TypeError(f'Value `{value}` cannot be cast to bool')
    return value in _TRUE_VALUES


def _cast_to(value: str, cast_to: Callable[[Any], T]) -> T:
    if cast_to is bool:
        return cast_to(_cast_to_bool(value))
    try:
        return cast_to(value)
    except Exception as e:
        raise TypeError(f'Cannot cast value `{value}` to specified type {cast_to}: {e}')


def get_env_var(key: str, cast_to: Callable[[Any], T], default: T = _DEFAULT_VALUE) -> T:
    """
    Получение переменной окружения и приведение её к указанному типу
    Args:
        key: название переменной окружения
        cast_to: тип к которому надо привести переменную
        default: значение по умолчанию, если переменная не задана в окружении
    Returns:
        Значение переменной окружения
    """
    value = os.environ.get(key)
    if value in ('', None):  # не задана в окружении
        if default == _DEFAULT_VALUE:
            raise ValueError(f'Environment variable {key} is not specified')
        return default
    return _cast_to(value, cast_to)
