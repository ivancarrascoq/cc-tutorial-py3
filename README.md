FORK ME
Create a fork to complete the tutorial. Send us the location of your fork (make sure your fork is not private when submitting your work) so we can download, run and review.

Thank you!



Note this was built using python 3.10+ and Django 3.2. We use the long-term stable release of Django 3.2 at CouponCabin so use that version for this project.

https://docs.djangoproject.com/en/3.2/intro/overview/

We've set up the basic documents for the Django tutorial including a sqlite file with the basic models set up to help get you kickstarted. It's still a good idea to read through the tutorial, but this avoids having to type everything in.

The admin is also set up and the admin username and password are both: admin 
Kind of boring but very easy to remember.

There are some bugs that we'll need you to fix as well as some new features to add.

Update the polls app to use HTML templates and the Django template language and use the render_to_response shortcut.

Create a homepage so a user can access http://127.0.0.1:8000/ with links to the /admin/ homepage and /polls/ sections. Use Django URL reversing feature with named URLs.

Follow the help text in the polls:create_questions_and_choices management command to create the questions and polls so you have data to work with during the exercise.

Get the polls/choices view working.

Complete the polls/most_popular_choice view to return the choice(s) with the most votes.

Show a short messages if either choices or questions are not available in the polls/choices view.

Raise a 404 response if the polls/choices view is passed an invalid or nonexistent primary key.

Show all choices and its related question for each choice (if showing all) or the specified choice (if passing in the choice ID). Work to reduce the number of queries on the full listing page when showing all choices. Also, only show each question once.

There are two bugs in the polls/views.py question method. We want to see the pub_date in the HTML response and we want the default date to work regardless of how long the Web server has been running.

Update polls/question to covert the date passed via the URL to a datetime object.

Update polls/index to return both the question_text and pub_date attributes. Work to reduce the number of queries as much as possible.

Mock out a way to limit the poll answer to one user vote per day. This does not need to be completely secure but what ways can you limit a user to a single vote without having them create an account and login.

Fix the bug in the polls:fix_output_bug management command.

Update the HTML for polls/index to link to the admin page for each object with Django's URL reverser.

Update the polls/test to include some test data. Expand the existing tests to check for the existence of test data in the response.

Write tests for any bugs you found while running through the previous steps

Add a pip requirements file for any packages (including Django) that get added to the project.

Please fix any WARNINGS issued by Django while working through the project. The tutorial will start with a few warnings that need to be corrected. Everything works so the warnings will not stop you from starting the project up, but should be resolved as part of this task.

Pay attention to the general rules of pep8 when coding. At CouponCabin we do not enforce rule for maximum line length: https://www.python.org/dev/peps/pep-0008/#id19 but we try to heed other pep8 rules where possible.
