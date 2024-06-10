from django.contrib.auth.models import User

def group_processor(request):
    if request.user.is_authenticated:
        is_po_group = request.user.groups.filter(name='po').exists()
        is_another_group = request.user.groups.filter(name='another_group').exists()  # Adjust as needed
    else:
        is_po_group = False
        is_another_group = False

    return {
        'is_po_group': is_po_group,
        'is_another_group': is_another_group,
    }
