from random import random


class SomeModel:
    def predict(self, message: str) -> float:
        return random()


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    if not (isinstance(message, str) and isinstance(model, SomeModel)):
        raise TypeError("message expected as instance of str and "
                        "model expected as instance of SomeModel")

    if not (isinstance(bad_thresholds, float) and isinstance(good_thresholds, float)):
        raise TypeError("bad_thresholds and good_thresholds expected as instance of float")

    if bad_thresholds > good_thresholds:
        raise ValueError("good_thresholds should be greater than bad_thresholds")

    prediction = model.predict(message)
    if prediction < bad_thresholds:
        return "неуд"
    elif prediction > good_thresholds:
        return "отл"
    else:
        return "норм"


if __name__ == '__main__':
    assert predict_message_mood("Чапаев и пустота", model) == "отл"
    assert predict_message_mood("Вулкан", model) == "неуд"
