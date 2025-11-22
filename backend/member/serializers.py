from rest_framework import serializers
from member.models import CoachMemberRelationship, Member, FoodPost, FoodPostComment
from users.models import FitnessGoal
from coach.serializers import CoachSerializer


class MemberSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = [
            "member_id",
            "user",
            "experience_level",
            "program_name",
            "message",
            "submitted_at",
            "status",
            "photo",
        ]

    def get_photo(self, obj):
        user_profile = getattr(obj, "user_profile", None)
        if user_profile and user_profile.photo and hasattr(user_profile.photo, "url"):
            return user_profile.photo.url
        return None


class CoachMemberRelationshipSerializer(serializers.ModelSerializer):
    coach = CoachSerializer(read_only=True)
    memberName = serializers.SerializerMethodField()
    memberId = serializers.CharField(source="member.member_id", read_only=True)
    member_photo = serializers.SerializerMethodField()
    experienceLevel = serializers.CharField(
        source="member.experience_level", read_only=True
    )
    message = serializers.CharField(source="member.message", read_only=True)
    programName = serializers.CharField(source="member.program_name", read_only=True)
    submittedAt = serializers.DateTimeField(
        source="member.submitted_at", read_only=True
    )
    goals = serializers.SerializerMethodField()

    class Meta:
        model = CoachMemberRelationship
        fields = [
            "relationship_id",
            "coach",
            "status",
            "memberName",
            "memberId",
            "member_photo",
            "experienceLevel",
            "message",
            "programName",
            "submittedAt",
            "goals",
        ]

    def get_memberName(self, obj):
        user_profile = obj.member.user
        user = user_profile.user
        full_name = f"{user.first_name} {user.last_name}".strip()
        return full_name if full_name else user.username

    def get_memberId(self, obj):
        return obj.member.member_id

    def get_member_photo(self, obj):
        user_profile = obj.member.user
        if hasattr(user_profile, "photo") and user_profile.photo:
            return user_profile.photo.url
        return None

    def get_goals(self, obj):
        user_profile = obj.member.user
        fitness_goals = FitnessGoal.objects.filter(user_profile=user_profile)
        return [goal.get_goal_type_display() for goal in fitness_goals]


class FoodPostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_first_name = serializers.SerializerMethodField()
    member_id = serializers.SerializerMethodField()
    author_photo = serializers.SerializerMethodField()
    coach_name = serializers.SerializerMethodField()

    class Meta:
        model = FoodPost
        fields = [
            "id",
            "title",
            "content",
            "image",
            "created_at",
            "updated_at",
            "author_name",
            "author_first_name",
            "member_id",
            "coach_name",
            "author_photo",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_author_name(self, obj):
        user = obj.user_profile.user
        full_name = f"{user.first_name} {user.last_name}".strip()
        return full_name if full_name else user.username

    def get_author_first_name(self, obj):
        return obj.user_profile.user.first_name or obj.user_profile.user.username

    def get_author_photo(self, obj):
        user_profile = getattr(obj, "user_profile", None)
        if user_profile and user_profile.photo and hasattr(user_profile.photo, "url"):
            return user_profile.photo.url
        return None

    def get_coach_name(self, obj):
        return obj.coach.user.username if obj.coach else None

    def get_member_id(self, obj):
        profile = obj.user_profile
        return f"M-{profile.user.id:05d}"

    def create(self, validated_data):
        user = self.context["request"].user
        user_profile = user.userprofile

        if user_profile.role != "member":
            raise serializers.ValidationError("Only members can create food posts.")

        # Find the active coach-member relationship
        relationship = (
            CoachMemberRelationship.objects.filter(
                member__user=user_profile, status="accepted"
            )
            .select_related("coach__user")
            .first()
        )

        if not relationship:
            raise serializers.ValidationError(
                "You don't have an active coach assigned."
            )

        validated_data["user_profile"] = user_profile
        validated_data["coach"] = relationship.coach.user

        return super().create(validated_data)


class FoodPostCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_role = serializers.SerializerMethodField()
    is_own = serializers.SerializerMethodField()

    class Meta:
        model = FoodPostComment
        fields = [
            "id",
            "food_post",
            "text",
            "author_name",
            "author_role",
            "is_own",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "food_post", "author_name", "author_role", "is_own"]

    def get_author_name(self, obj):
        return obj.author.user.username

    def get_author_role(self, obj):
        return obj.author.role

    def get_is_own(self, obj):
        request = self.context.get("request")
        return bool(request and obj.author == request.user.userprofile)

    def create(self, validated_data):
        user_profile = self.context["request"].user.userprofile
        validated_data["author"] = user_profile
        return super().create(validated_data)
