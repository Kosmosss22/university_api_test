class SoftAssert:
    def __init__(self):
        self.errors = []

    def assert_equal(self, actual, expected, message=""):
        if actual != expected:
            self.errors.append(f"{message}: expected {expected}, got {actual}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.errors:
            raise AssertionError("\n".join(self.errors))