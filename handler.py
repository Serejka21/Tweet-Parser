from logging import StreamHandler, Formatter, INFO


def create_handler() -> StreamHandler:
    console_handler = StreamHandler()
    console_handler.setLevel(INFO)

    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    return console_handler
