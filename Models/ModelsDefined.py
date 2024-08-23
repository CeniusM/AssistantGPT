

class Model:
    def __init__(self, name, input_price_per_mil, output_price_per_mil) -> None:
        self.name = name
        self.input_price = input_price_per_mil / 1_000_000.0
        self.output_price = output_price_per_mil / 1_000_000.0