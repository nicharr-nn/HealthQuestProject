## Description
This pull request includes the following changes:
- add due date in creating workout program
- add more api for delete and update workout assignment
- add ProgramCard component
- add more test cases for workout and member app
- remove unused api and models
- seperate functions which have many responsibilities
- fix bugs in creating and editing workout program
- fix bugs in UserProfile updated photo url
- add rating in food-recipe


## Type of Change
- [X] feat (new functionality)
- [X] fix (non-breaking change that fixes an issue)
- [X] refactor (code restructuring without changing functionality)
- [X] style (code style improvements, formatting)
- [X] test (adding or updating tests)


### Build / Frontend
- **Adjust code styles**
  - Modified `CreateWorkoutProgram.vue` to have dropdown for selecting member_id and due date selection.

### Backend / Infrastructure
- **Modify Model and API**
  - Changed logic in member/views.py to update member's program_name when a workout program is assigned.
  - Split complete-workout-day API into two endpoints: one for checking completion status and another for marking completion.
  - Add 2 new API endpoints in workout/urls.py for managing and deleting workout assignments.
  - Add function get_status in models.py to determine assignment status.
  - add logic to handle due_date in workout assignment creation and update.
  - add logic to handle change member_id or change visibility when updating workout assignments.
  - add rating api in recipe app.
- **Serializer Update**
  - Updated `WorkoutAssignmentSerializer` to include `status` field.
- **Delete UserAchivement, Achivement model**
- **Test Cases**
  - Added more unit tests for the workout assignments
  - Fix coach can't see the programs they created because of filter level_access
  - Fix other coach can't see programs created by other coaches
  - Added test cases for food reating api

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
2. Test the frontend changes by navigating to the Create Workout Program page and Workout Page in the application.
3. Test existing functionalities to ensure no regressions (e.g., coach comments on FoodPost, member completes program and gain bonus point).
4. Test edge cases for workout program updates (e.g., change private to public program, update due date).