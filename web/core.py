import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import dropbox
import shortuuid
from social_django.models import UserSocialAuth

from web.models import MonthlyLimitService
from web.models import PersistenceService
from web.models import SupervisorIdService
from web.models import ViewerConnectionService
from web.models import ViewerService


# Persistence Models
class Supervisor(models.Model):
    active = models.BooleanField(default=True)
    premium_expiration = models.DateField(blank=True, null=True)
    inbound_identity_token = models.OneToOneField(User, on_delete=models.CASCADE)
    supervisor_id = models.CharField(max_length=40, unique=True)
    viewer_authentication_key = models.CharField(max_length=80)


class Activity(models.Model):
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    activity_month = models.DateField()
    activity_count = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs):  # @UnusedVariable Because this method is an
        # override

    if created:
        supervisor_id = shortuuid.ShortUUID().random(length=7)

        Supervisor.objects.create(active=True, inbound_identity_token=instance, supervisor_id=supervisor_id)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs):  # @UnusedVariable Because this method is an override
    instance.supervisor.save()


@receiver(post_save, sender=UserSocialAuth)
def save_user(sender, instance:UserSocialAuth, **kwargs):  # @UnusedVariable Because this method is an override
    if 'access_token' in instance.extra_data:
        supervisor = instance.user.supervisor
        supervisor.viewer_authentication_key = instance.extra_data['access_token']
    
        supervisor.save()


class CoreServiceFactory:
    core_monthly_limit_service = datetime.date
    core_persistence_service = Activity
    core_persistence_service2 = Supervisor
    core_supervisor_id_service = shortuuid.ShortUUID()
    core_viewer_service = dropbox.Dropbox
    core_viewer_connection_service = dropbox.DropboxOAuth2Flow
    
    def createMonthlyLimitService(self) -> MonthlyLimitService:
        return MonthlyLimitService(self.core_monthly_limit_service)
    
    def createPersistenceService(self) -> PersistenceService:
        return PersistenceService(self.core_persistence_service, self.core_persistence_service2)

    def createSupervisorIdService(self) -> SupervisorIdService:
        return SupervisorIdService(self.core_supervisor_id_service)

    def createViewerService(self) -> ViewerService:
        return ViewerService(self.core_viewer_service)

    def createViewerConnectionService(self) -> ViewerConnectionService:
        return ViewerConnectionService(self.core_viewer_connection_service)
