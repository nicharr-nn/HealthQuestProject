from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from .models import Recipe
import logging

logger = logging.getLogger(__name__)


def _generate_pdf(instance: Recipe):
    try:
        instance.create_pdf()
    except Exception as exc:
        logger.exception("Failed to generate PDF for recipe %s: %s", instance.pk, exc)


@receiver(post_save, sender=Recipe)
def generate_recipe_pdf(sender, instance, created, **kwargs):
    """
    Generate a PDF file for a newly created Recipe after the DB transaction commits.
    """
    if created and not instance.pdf_file:
        # run after transaction commit to ensure instance is persisted
        transaction.on_commit(lambda: _generate_pdf(instance))
