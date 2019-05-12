from rest_framework.exceptions import ValidationError


def check_inn(inn):
    """
    Проверка ИНН на валидность
    :param inn: строка с ИНН
    :raises ValidationError: в случае если ИНН неверный
    :return: возвращяет ИНН
    """

    def inn_csum(_inn):
        k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        pairs = zip(k[11 - len(_inn):], [int(x) for x in _inn])
        return str(sum([k * v for k, v in pairs]) % 11 % 10)

    if len(inn) not in (10, 12):
        raise ValidationError('Неверный ИНН, длина должна быть 10 или 12 символов', code='inn')

    if len(inn) == 10:
        integrity = inn[-1] == inn_csum(inn[:-1])
    else:
        integrity = inn[-2:] == inn_csum(inn[:-2]) + inn_csum(inn[:-1])
    if not integrity:
        raise ValidationError('Неверный ИНН, неверный код', code='inn')
    return inn
