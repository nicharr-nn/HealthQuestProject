## Description
This pull request includes the following changes:
- Add WorkoutAssignment model and API in workout app.
- Change CSS to Tailwind CSS to improve layout.
- Check grammar and limitations.
- Implement Test cases for models and APIs.
- fix goal_achive in UserLevel
- add choiches for difficulty level in workout program (easy, medium, hard).
- fix bugs when creating workout program.

## Type of Change
- [X] feat (new functionality)
- [X] fix (non-breaking change that fixes an issue)
- [X] refactor (code restructuring without changing functionality)
- [X] style (code style improvements, formatting)


### Build / Frontend
- **Adjust code styles**
  - Modified `CreateWorkoutProgram.vue` to improve layout and responsiveness using Tailwind CSS classes.
  - Add Assigned Programs section to display programs assigned to the member in `WorkoutPage.vue`.
  - Remove level access in WorkoutCard and uppercase text.
  - Add restrictions for creating a workout day program: duration must be positive number in frontend.
  - Fix bugs for field name mismatch when creating workout program (duration_minutes -> duration).
  - Adjust fetchProgramDetail logic in `WorkoutProgram.vue` to handle multiple workouts correctly.

- **Grammar and Limitation Fixes**
  - Updated text in `CreateWorkoutProgram.vue` to correct grammar (e.g., "1 days" to "1 day").
- **Edit Existing workout fields**
  - Coach can edit every field in workout program except assigned member.

### Backend / Infrastructure
- **New Model and API**
  - Created `WorkoutAssignment` model to link members with assigned workout programs.
  - Developed API endpoints to manage workout assignments.
  - Changed logic in member/views.py to update member's program_name when a workout program is assigned.
  - Split complete-workout-day API into two endpoints: one for checking completion status and another for marking completion.
- **Difficulty Level Choices**
  - Added choices for difficulty level in `WorkoutProgram` model (easy, medium, hard).
- **Fix UserLevel Goal Achieved Bug**
  - Corrected logic to properly update `goal_achieved` field in `UserLevel` model.
- **Serializer Update**
  - Updated `WorkoutProgramSerializer` to include `assigned_member_id` field.
  - Updated `WorkoutDay` to include `type` field.
  - Change logic in check_completion in workout/models to handle many workouts in one day.
- **Delete workout_assignments, fitness app**
- **Test Cases**
  - Added unit tests for the FoodPost, FoodPostComment, Member, CoachMemberRelationship models.
  - Adjusted some views in FoodPost, Workout.


## Testing Checklist
- [X] Unit tests added for new model and API endpoints
- [X] Manual testing of frontend changes
- [X] Verified grammar and limitation fixes in UI

## Technical Checklist
- [ ] Code follows project style guidelines
- [ ] No console errors in browser developer tools
- [ ] API endpoints return expected status codes
- [ ] Database migrations work correctly

## Database Changes
- [X] New migrations added
- [X] Existing migrations modified

## Steps to check
1. docker-compose exec backend python manage.py migrate
2. docker-compose exec backend python manage.py test workout
3. docker-compose exec backend python manage.py test member
4. Test the frontend changes by navigating to the Create Workout Program page and Workout Page in the application.
5. Test existing functionalities to ensure no regressions (e.g., coach comments on FoodPost, member completes program and gain bonus point).
6. Test edge cases for workout program creation (e.g., duration minutes, editing programs).