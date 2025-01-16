# Reelbugs Review App (Anonymous Reviews)

This is a Django-based web application that allows users to anonymously review movies, watch trailers, and view cast details. Each anonymous review is associated with a randomly generated profile, ensuring the anonymity of reviewers. Profile pictures are also dynamically created based on these random profiles.

## Features
- **Anonymous Reviews**: Users can review movies without creating an account. Reviews are attributed to randomly generated usernames.
- **Movie Trailers**: Watch trailers for movies directly within the app. Movie details are  fetched using TMDB API
- **Cast Details**: View detailed information about the cast of each movie.
- **Randomly Generated Profiles**: Each review is linked to a unique, randomly generated profile with a profile picture.
  
## Tech Stack
- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite 
- **Libraries/Tools**:
  - Django Rest Framework
  - Faker (for generating random user profiles)
  - Gravatar or a custom image generation method for profile pictures
