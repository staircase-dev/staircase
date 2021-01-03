def check_binop_timezones(first, second):
    assert first.tz == second.tz, "operands must have the same timezone, or none at all"