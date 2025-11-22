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
def generate_or_update_recipe_pdf(sender, instance, created, raw=False, **kwargs):
    """
    Generate or update the PDF for a Recipe when it's created or edited.
    """
    
    # Skip PDF generation during fixture loading
    if raw:
        logger.info("Skipping PDF generation for recipe %s (fixture loading)", instance.pk)
        return

    def _needs_pdf_update():
        # Only regenerate if PDF is missing or the recipe content changed
        if not instance.pdf_file:
            return True
        changed_fields = getattr(instance, "_changed_fields", None)
        if changed_fields:
            return any(
                field in changed_fields for field in ["title", "ingredients", "steps"]
            )
        return True

    # Always trigger on commit, to avoid race condition
    if created or _needs_pdf_update():
        transaction.on_commit(lambda: _generate_pdf(instance))