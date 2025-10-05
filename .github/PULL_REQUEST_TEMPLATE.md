## Description
This pull request includes the following changes:
- Fixes the coach certification upload and approval workflow.
- Refactors the coach registration and profile management components.
- Updates styles for better user experience in the coach portal.
- Ensures that approved coaches can create workout programs.
- Cleans up unused code and improves code readability.

## Type of Change
- [ ] feat (new functionality)
- [X] fix (non-breaking change that fixes an issue)
- [X] refactor (code restructuring without changing functionality)
- [ ] docs (updates to documentation or comments)
- [ ] test  (adding or updating tests)
- [X] style (code style improvements, formatting)
- [ ] chore (build process, dependency updates)

## Testing Checklist

### Coach Flow Testing
#### 1. Coach Registration & Certification Upload
- [ ] Coach signs in and completes profile (AboutYou.vue)
- [ ] Coach is redirected to Coach Portal
- [ ] Coach can upload certification PDF
- [ ] Status shows as "pending" after upload
- [ ] Refresh maintains pending status
- [ ] Logout and login again shows pending status
- [ ] Can resubmit certification file while pending

#### 2. Admin Approval Process
- [ ] Admin (Django admin) can approve coach status
- [ ] Coach status changes from "pending" to "approved" in admin

#### 3. Approved Coach Experience
- [ ] Coach logs in after approval
- [ ] Coach Dashboard shows approved status
- [ ] Can create workout programs in Dashboard
- [ ] In Coach Portal: status shows "approved"
- [ ] Can edit profile but cannot upload certification again

#### 4. Program Creation
- [ ] Coach can create new workout program
- [ ] Program saves successfully with all fields
- [ ] Program appears in coach's program list

### User Flow Testing
#### 1. User Onboarding
- [ ] User completes profile setup
- [ ] Redirected to main dashboard
- [ ] "Start Workout" button functions correctly
- [ ] Navbar navigation works properly

#### 2. Program Discovery
- [ ] User can browse available programs
- [ ] "View Program" button works correctly
- [ ] Program details display properly

#### 3. Workout Experience
- [ ] Workout plan displays day by day
- [ ] Daily workouts show correct information
- [ ] Video links  work properly

## Technical Checklist
- [ ] Code follows project style guidelines
- [ ] No console errors in browser developer tools
- [ ] API endpoints return expected status codes
- [ ] Database migrations (if any) work correctly
- [ ] No security vulnerabilities introduced
- [ ] Error handling implemented where needed

## Database Changes
- [ ] No changes to database schema
- [ ] New migrations added
- [ ] Existing migrations modified
- [ ] Data migrations needed