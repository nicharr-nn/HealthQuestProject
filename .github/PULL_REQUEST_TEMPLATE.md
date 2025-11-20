## Description
This pull request includes the following changes:
- add test for coach viewing their created programs only
- add test for member and coach comments on foodPost
- fix the issue where member's program_name is not updated when a assignment is deleted or changed
- fix format data to show in ProgramCard.vue
- fix bonus point not added when member completes a workout program


## Type of Change
- [X] feat (new functionality)
- [X] fix (non-breaking change that fixes an issue)
- [X] refactor (code restructuring without changing functionality)
- [X] style (code style improvements, formatting)
- [X] test (adding or updating tests)


### Build / Frontend
- **Adjust code styles**
  - Modified `ProgramCard.vue` to have consistent formatting for status, category, and difficulty level by replacing underscores with spaces and capitalizing words.
- **Update Status Filtering Logic**
  - Added the filtering logic in `member/views.py` to include status filtering
### Backend / Infrastructure
- **Modify Model and API**
  - Updated the filtering criteria in `member/views.py` to include "paused" status for active workout assignments.
  - Adjusted the logic in `workout/views.py` to ensure that 
    1. workout programs are sorted based on the user's current fitness goals first then by date.
    2. workout assignments sorted by status (in-progress, paused, completed) and then by due date.
- **Fix Program Name Update**
  - Ensured that the member's `program_name` is updated correctly when a workout assignment is deleted or changed.
- **Test Cases**
  - Added test cases in `backend/member/tests/test_workoutprogram.py` to verify that coaches can only view their created programs.
  - Added test cases in `backend/member/tests/test_foodcomment.py` to verify that both members and coaches can comment on FoodPosts, and the comments reflect the correct author information.

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
1. Test member can see their assignment's name updated when assignment is deleted or changed.
2. Test existing functionalities to ensure no regressions (e.g., coach comments on FoodPost, member completes program and gain bonus point etc.).