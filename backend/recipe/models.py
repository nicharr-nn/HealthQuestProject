from django.db import models
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.utils.text import slugify
from users.models import UserProfile
from django.db.models import Avg


class Recipe(models.Model):
    LEVEL_CHOICES = [("silver", "Silver"), ("gold", "Gold")]

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    steps = models.TextField()
    access_level = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, default="silver"
    )
    image = models.ImageField(upload_to="recipes/images/", null=True, blank=True)
    pdf_file = models.FileField(upload_to="recipes/pdfs/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.user_profile.user.username})"

    def create_pdf(self):
        """
        Generate a simple PDF containing title, author, ingredients, and steps.
        Saves the PDF to self.pdf_file.
        """

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        # Margins
        width, height = A4
        x_margin, y_margin = 50, height - 100

        # --- Header ---
        p.setFont("Helvetica-Bold", 20)
        p.drawString(x_margin, y_margin, self.title)

        p.setFont("Helvetica", 12)
        author_name = self.user_profile.user.username
        p.drawString(x_margin, y_margin - 25, f"Author: {author_name}")
        p.drawString(
            x_margin, y_margin - 40, f"Access Level: {self.access_level.capitalize()}"
        )

        # --- Ingredients ---
        p.setFont("Helvetica-Bold", 14)
        p.drawString(x_margin, y_margin - 80, "Ingredients:")
        p.setFont("Helvetica", 12)

        y_pos = y_margin - 100
        for line in self.ingredients.splitlines():
            if y_pos < 100:  # handle page overflow
                p.showPage()
                y_pos = height - 100
            p.drawString(x_margin, y_pos, f"- {line.strip()}")
            y_pos -= 15

        # --- Steps ---
        y_pos -= 20
        p.setFont("Helvetica-Bold", 14)
        p.drawString(x_margin, y_pos, "Steps:")
        y_pos -= 20
        p.setFont("Helvetica", 12)

        for line in self.steps.splitlines():
            if y_pos < 100:
                p.showPage()
                y_pos = height - 100
            p.drawString(x_margin, y_pos, line.strip())
            y_pos -= 15

        p.showPage()
        p.save()

        # Save file to model
        buffer.seek(0)
        pdf_content = buffer.read()
        buffer.close()

        safe_title = slugify(self.title) or "recipe"
        filename = f"{safe_title}.pdf"
        self.pdf_file.save(filename, ContentFile(pdf_content), save=True)

        return self.pdf_file.url

    @property
    def average_rating(self):
        return self.ratings.aggregate(Avg("rating"))["rating__avg"] or 0

    def save(self, *args, **kwargs):
        if self.pk:
            old = Recipe.objects.get(pk=self.pk)
            self._changed_fields = [
                f for f in ["title", "ingredients", "steps"]
                if getattr(old, f) != getattr(self, f)
            ]
        else:
            self._changed_fields = ["title", "ingredients", "steps"]
        super().save(*args, **kwargs)


    class Meta:
        ordering = ["-created_at"]


class RecipeRating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )  # expected 1–5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("recipe", "user_profile")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_profile.user.username} → {self.recipe.title}: {self.rating}"
