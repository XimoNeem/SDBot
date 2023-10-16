import enum

class ProductType(enum.Enum):
    '''
    Тип продукта (По типу All можно получить все продукты из бд))
    '''
    all = 'items_All'
    cases = 'items_Cases'
    headphones = 'items_Headphones'

    def get_type_by_value(value:str):
        '''
        Конверитровать строку в тип продуктов
        '''
        for val in ProductType:
            if val.value == value:
                return val
        print('[ERROR] Нет такого типа')