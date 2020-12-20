from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as gettext


class UserExtraConf(models.Model):
    traceability = models.BooleanField(
        default=False, verbose_name=gettext("Tracabilidad")
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,
        verbose_name=User._meta.verbose_name, related_name='user_extra_conf'
    )

    class Meta:
        verbose_name = gettext("User extra config")
        verbose_name_plural = gettext("User extra config")

        db_table = 'c19t_user_extra_conf'


@receiver(signals.post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'user_extra_conf'):
        UserExtraConf.objects.create(user=instance)

    if hasattr(instance, 'user_extra_conf'):
        instance.user_extra_conf.save()
