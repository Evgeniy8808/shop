from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TABLE_HEADER = '''
                    <table class="table">
                        <tbody>
                '''

TABLE_FOOTER = '''
                        </tbody>
                    </table>
                '''

TABLE_CONTENT = '''
                <tr>
                    <td>{name}</td>
                    <td>{value}</td>
                </tr>
                '''

PRODUCT_SPEC = {
    'notebook': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Частота процессора': 'processor_freg',
        'Память': 'ram',
        'Видео память': 'video',
        'Время работы аккумулятора': 'time_without_charge',
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Разрешение экрана': 'resolution',
        'Память': 'ram',
        'cd карта': 'sd',
        'Макс.обьем встроенной памяти': 'sd_vol_max',
        'Обьем батареи': 'accum_volue',
        'Главная камера': 'main_cam_up',
        'Фронтальная камера': 'frontal_cam_up',
    }
}


def get_product_spec(products, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(products, value))
    return table_content


@register.filter
def product_spec(products):
    model_name = products.__class__._meta.model_name
    return mark_safe(TABLE_HEADER + get_product_spec(products, model_name) + TABLE_FOOTER)
