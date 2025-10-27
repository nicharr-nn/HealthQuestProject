from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.utils.text import slugify

from .models import Recipe
from .serializers import RecipeSerializer
from .permissions import CanViewRecipe


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, CanViewRecipe])
def recipe_list(request):
    """GET = list recipes, POST = create new recipe"""
    if request.method == "GET":
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True, context={"request": request})
        return Response(serializer.data)

    if request.method == "POST":
        user_profile = request.user.userprofile

        # Only coaches or gold users can create recipes
        if (
            user_profile.role != "coach"
            and user_profile.get_current_level().level != "Gold"
        ):
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
    serializer = RecipeSerializer(recipe, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_recipe_pdf(request, id):
    """Returns the generated PDF file."""
    try:
        recipe = Recipe.objects.get(pk=id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe not found")

    # Optional access restriction
    user_profile = request.user.userprofile
    if (
        recipe.access_level == "gold"
        and user_profile.role not in ["coach"]
        and user_profile.get_current_level().level != "Gold"
    ):
        return Response({"detail": "Access denied. Gold level required."}, status=403)

    # Generate PDF if missing
    if not recipe.pdf_file:
        recipe.create_pdf()

    return FileResponse(
        recipe.pdf_file.open("rb"),
        as_attachment=True,
        filename=f"{recipe.title}.pdf",
        content_type="application/pdf",
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_recipe_image(request, id):
    """Uploads an image for the recipe."""
    try:
        recipe = Recipe.objects.get(pk=id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe not found")

    user_profile = getattr(request.user, "userprofile", None)
    if user_profile is None:
        return Response(
            {"detail": "Profile not found."}, status=status.HTTP_400_BAD_REQUEST
        )

    if (
        recipe.user_profile != user_profile
        and user_profile.role != "coach"
        and user_profile.get_current_level().level != "Gold"
    ):
        return Response(
            {"detail": "Permission denied. You can only edit your own recipes."},
            status=status.HTTP_403_FORBIDDEN,
        )

    image_file = request.FILES.get("image")
    if not image_file:
        return Response(
            {"detail": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST
        )

    safe_name = f"{slugify(recipe.title) or 'recipe'}-{image_file.name}"
    recipe.image.save(safe_name, image_file, save=True)

    full_url = request.build_absolute_uri(recipe.image.url)
    serializer = RecipeSerializer(recipe)
    return Response(
        {
            "detail": "Photo uploaded successfully!",
            "file_path": recipe.image.name,
            "photo_url": full_url,
            "recipe": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_recipe(request, id):
    """DELETE a recipe"""
    recipe = get_object_or_404(Recipe, pk=id)
    user_profile = request.user.userprofile

    if (
        recipe.user_profile != user_profile
        and user_profile.role != "coach"
        and user_profile.get_current_level().level != "Gold"
    ):
        return Response(
            {"detail": "Permission denied. You can only delete your own recipes."},
            status=status.HTTP_403_FORBIDDEN,
        )

    recipe.delete()
    return Response(
        {"detail": "Recipe deleted successfully."}, status=status.HTTP_200_OK
    )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_recipe(request, id):
    """PUT/PATCH to update a recipe"""
    recipe = get_object_or_404(Recipe, pk=id)
    user_profile = request.user.userprofile

    if (
        recipe.user_profile != user_profile
        and user_profile.role != "coach"
        and user_profile.get_current_level().level != "Gold"
    ):
        return Response(
            {"detail": "Permission denied. You can only update your own recipes."},
            status=status.HTTP_403_FORBIDDEN,
        )

    partial = request.method == "PATCH"
    serializer = RecipeSerializer(recipe, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"success": True, "recipe": serializer.data},
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_recipes(request):
    """Returns only the recipes created by the authenticated user."""
    user_profile = request.user.userprofile
    recipes = Recipe.objects.filter(user_profile=user_profile).order_by("-id")
    serializer = RecipeSerializer(recipes, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)
