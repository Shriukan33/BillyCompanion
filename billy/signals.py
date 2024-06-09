from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Billy, BillyStat

@receiver(m2m_changed, sender=Billy.items.through)
def update_billystat(sender, instance, action, **kwargs):
    for pk in kwargs.get("pk_set"):
        if action == "post_add":
            for billystat in BillyStat.objects.filter(billy=instance):
                billystat.compute_value("add", pk)
                billystat.save()
        elif action == "pre_remove":
            for billystat in BillyStat.objects.filter(billy=instance):
                billystat.compute_value("remove", pk)
                billystat.save()
