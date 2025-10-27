#!/usr/bin/env python
"""
Create mock data for testing FoodDiary comment feature
Run: docker exec healthquestproject-backend-1 python create_mock_data.py
"""

import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthquest_backend.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from member.models import Member, CoachMemberRelationship, FoodPost
from coach.models import Coach

def create_mock_data():
    print("🚀 Creating mock data for FoodDiary testing...\n")

    # Get existing coach
    try:
        coach = Coach.objects.get(public_id='C-00000')
        coach_profile = coach.user
        print(f"✅ Using existing coach: {coach_profile.user.username} ({coach.public_id})")
    except Coach.DoesNotExist:
        print("❌ No coach found! Please create a coach first.")
        return

    # Create test member user
    member_username = 'test_member'

    # Check if member already exists
    if User.objects.filter(username=member_username).exists():
        print(f"ℹ️  Member '{member_username}' already exists. Using existing user...")
        member_user = User.objects.get(username=member_username)
        member_profile = UserProfile.objects.get(user=member_user)

        # Update profile to ensure it's a member
        if not member_profile.role or member_profile.role != 'member':
            member_profile.role = 'member'
            member_profile.height = 170
            member_profile.weight = 65
            member_profile.age = 25
            member_profile.gender = 'M'
            member_profile.save()
            print(f"  ✅ Updated UserProfile to member role")
    else:
        # Create User
        member_user = User.objects.create_user(
            username=member_username,
            email='testmember@example.com',
            password='member123'
        )
        print(f"✅ Created user: {member_user.username}")

        # Create UserProfile
        member_profile = UserProfile.objects.create(
            user=member_user,
            role='member',
            height=170,
            weight=65,
            age=25,
            gender='M'
        )
        print(f"✅ Created UserProfile with role: {member_profile.role}")

    # Create or get Member
    member, created = Member.objects.get_or_create(
        user=member_profile,
        defaults={
            'member_id': 'M-00001',
            'experience_level': 'intermediate',
            'status': 'approved'
        }
    )
    if created:
        print(f"✅ Created Member: {member.member_id}")
    else:
        print(f"ℹ️  Member already exists: {member.member_id}")

    # Create Coach-Member Relationship
    relationship, created = CoachMemberRelationship.objects.get_or_create(
        coach=coach,
        member=member,
        defaults={'status': 'accepted'}
    )
    if created:
        print(f"✅ Created relationship: {coach.public_id} → {member.member_id}")
    else:
        print(f"ℹ️  Relationship already exists: {coach.public_id} → {member.member_id}")

    # Clear existing food posts for this member
    existing_posts = FoodPost.objects.filter(user_profile=member_profile)
    deleted_count = existing_posts.count()
    if deleted_count > 0:
        existing_posts.delete()
        print(f"🗑️  Deleted {deleted_count} existing food posts")

    # Create Food Posts
    print("\n📝 Creating food posts...")

    food_posts_data = [
        {
            'title': 'Healthy Breakfast Bowl',
            'content': 'Oatmeal with fresh berries, banana slices, chia seeds, and almond butter. Very filling and nutritious!',
            'days_ago': 0  # Today
        },
        {
            'title': 'Grilled Chicken Salad',
            'content': 'Mixed greens with grilled chicken breast, cherry tomatoes, cucumber, avocado, and olive oil dressing.',
            'days_ago': 0  # Today
        },
        {
            'title': 'Protein Smoothie',
            'content': 'Whey protein, banana, spinach, almond milk, peanut butter, and ice. Post-workout recovery drink.',
            'days_ago': 1  # Yesterday
        },
        {
            'title': 'Salmon with Quinoa',
            'content': 'Baked salmon fillet with quinoa, roasted vegetables (broccoli, carrots, bell peppers), and lemon.',
            'days_ago': 1  # Yesterday
        },
        {
            'title': 'Greek Yogurt Parfait',
            'content': 'Greek yogurt layered with granola, mixed berries, honey, and walnuts. Great morning snack!',
            'days_ago': 2  # 2 days ago
        },
        {
            'title': 'Turkey Wrap',
            'content': 'Whole wheat wrap with turkey breast, lettuce, tomato, cheese, and mustard. Quick lunch option.',
            'days_ago': 2  # 2 days ago
        }
    ]

    created_posts = []
    for post_data in food_posts_data:
        post_date = datetime.now() - timedelta(days=post_data['days_ago'])

        food_post = FoodPost.objects.create(
            user_profile=member_profile,
            coach=coach_profile,
            title=post_data['title'],
            content=post_data['content'],
            # Note: We're not adding images for mock data
        )

        # Manually set created_at to simulate different dates
        food_post.created_at = post_date
        food_post.save()

        created_posts.append(food_post)

        days_text = "today" if post_data['days_ago'] == 0 else f"{post_data['days_ago']} days ago"
        print(f"  ✅ {food_post.title} (posted {days_text})")

    print(f"\n✅ Created {len(created_posts)} food posts")

    # Summary
    print("\n" + "="*60)
    print("🎉 Mock Data Created Successfully!")
    print("="*60)
    print(f"\n📋 Test Credentials:")
    print(f"   Member Username: {member_username}")
    print(f"   Member Password: member123")
    print(f"   Member ID: {member.member_id}")
    print(f"\n📋 Coach Info:")
    print(f"   Coach Username: {coach_profile.user.username}")
    print(f"   Coach ID: {coach.public_id}")
    print(f"\n📋 Food Posts: {len(created_posts)} posts created")
    print(f"\n🌐 Test URLs:")
    print(f"   FoodDiary (Coach View): http://localhost:5173/food-diary/M-00001")
    print(f"   Food Posts (Member View): http://localhost:5173/food-post")
    print("\n💡 Next Steps:")
    print("   1. Login as coach to view FoodDiary")
    print("   2. View member's food posts")
    print("   3. Once backend is built, you can add comments!")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        create_mock_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
