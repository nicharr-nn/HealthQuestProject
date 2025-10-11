from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404

from .models import Recipe
from .serializers import RecipeSerializer
from .permissions import CanViewRecipe


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, CanViewRecipe])
def recipe_list(request):
    """GET = list recipes, POST = create new recipe"""
    if request.method == "GET":
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        user_profile = request.user.userprofile

        # Only coaches or gold users can create recipes
        if user_profile.role != "coach" and user_profile.get_current_level().level != "Gold":
            return Response(
                {"detail": "Only coaches and gold users can create recipes."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = RecipeSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user_profile=user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated, CanViewRecipe])
def recipe_detail(request, pk):
    """GET single recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_recipe_pdf(request, id):
    """
    Endpoint: /api/recipes/<id>/download-pdf/
    Returns the generated PDF file.
    """
    try:
        recipe = Recipe.objects.get(pk=id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe not found")

    # Optional access restriction
    user_profile = request.user.userprofile
    if recipe.access_level == "gold" and (
        user_profile.role not in ["coach"] and user_profile.get_current_level().level != "Gold"
    ):
        return Response({"detail": "Access denied. Gold level required."}, status=403)

    # Generate PDF if missing
    if not recipe.pdf_file:
        recipe.create_pdf()

    # Use Django's FileResponse to stream file
    return FileResponse(
        recipe.pdf_file.open("rb"),
        as_attachment=True,
        filename=f"{recipe.title}.pdf",
        content_type="application/pdf"
    )

