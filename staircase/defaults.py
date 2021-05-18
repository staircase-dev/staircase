class Defaults:
    def __init__(self):
        self.tz_default = None
        self.use_dates_default = False
        self.dict = {
            "tz": None,
            "use_dates": False,
        }

    def set_default(self, name, val):
        self.dict.update({name: val})

    def get_default(self, name):
        return self.dict[name]


default = Defaults()
