from staircase.core.poly.methods import (
    _layer_multiple,
    clip,
    get_integral_and_mean,
    layer,
    resample,
    sample,
    step_changes,
    values_in_range,
)


def add_methods(cls):
    cls._layer_multiple = _layer_multiple
    cls.clip = clip
    cls.get_integral_and_mean = get_integral_and_mean
    cls.layer = layer
    cls.resample = resample
    cls.sample = sample
    cls.step_changes = step_changes
    cls.values_in_range = values_in_range
