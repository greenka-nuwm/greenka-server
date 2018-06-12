class FloatConverter:
    """Path converter for float."""
    regex = r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return '%06f' % (value, )