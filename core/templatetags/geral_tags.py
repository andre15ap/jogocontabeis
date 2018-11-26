
from django import template


register = template.Library()



@register.filter(name='indice')
def indice(num):
    if num == 1:
        return 'A'
    elif num == 2:
        return 'B'
    elif num == 3:
        return 'C'
    elif num == 4:
        return 'D'
    elif num == 5:
        return 'E'
    elif num == 6:
        return 'F'
    elif num == 7:
        return 'G'
    elif num == 8:
        return 'H'
    elif num == 9:
        return 'I'


# @register.filter(name='tipo_usuario')
# def tipo_usuario(user, tipo):
#     if tipo == 'solicitante':
#         try:
#             usuario = Solicitante.objects.get(id=user.id)
#             return True
#         except:
#             pass
#     elif tipo == 'suporte':
#         try:
#             usuario = SuporteConta.objects.get(id=user.id)
#             return True
#         except:
#             pass
    
#     elif tipo == 'administrador':
#         try:
#             usuario = Administrador.objects.get(id=user.id)
#             return True
#         except:
#             pass
    
#     return False