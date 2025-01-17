# PriceLab Blog Task
 This is the repo for the task that i was give for the internship role.

## Project Timeline
- **Start Time:** 2025-01-16 5:00 PM
- **Basic project setup with blogs app:** 5:20 PM
- **Wrote blogs Model and configured Django-debug-toolbar:** 5:35 PM
- **Setup authentication system :** 8:00 PM
- **Added Like, Comment[Create, Update] :** 2:40 AM
- **Complted Project, Passed pre-commit test:** 2025-01-17 1:09 PM

## Implemented Features
### 1. Authenticaiton
The default django authentication is implemented with some small changes in the path of the routing as asked in the task. User can route to `/register` `/login` `/logged_out`.
### 2. Blogs
The blog post has all the fields that is asked in the task and with addition feature like `like` and `comment`. All the comments and likes are using htmx to insure responsiveness.
Only logged in user can `like` and `comment` while other users can still read all `blogs` `likes` and `comments`
### 3. UI
Bootstrap is used with , `crispy-bootstrap-forms` to ensure consistency of the UI.

### Formatting
Pyton's flake8 formatting is used for the project.

**All the timestamps of the project is mentioned at the top of this documentation**

