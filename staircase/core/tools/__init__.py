from staircase.core.tools.datetimes import check_binop_timezones
import staircase as sc


def _sanitize_binary_operands(self, other, copy_other=False):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
        if copy_other:
            other = other.copy()
    return self.copy(), other
