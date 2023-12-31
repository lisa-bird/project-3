# Milestone Project-3 Barbie Wiki

![Mock up](/flaskr/static/img/mock-up.jpg)

[Vist my website here](https://project-3-lb-cad35c2a8ec5.herokuapp.com/)

Milestone project three calls for a full-stack site that allows users to manage common dataset about a particular domain.
With the release of the highly anticipated new Barbie movie, I wanted to create a Barbie inspired wiki. Allowing users to read articles about all things Barbie, create their own articles and comment on others.

## Owners Goal

To create a community driven platform for Barbie fans, from long-term fans to new upcoming fans. These fans can contribute to the wiki by adding new articles, editing them where needed and participate in discussions. Ultimately creating a vibrant and welcoming wiki for users to enjoy.

## Audience

The audience will include male and female, young and mature. Barbie has been around for many years, since 1959, generating a plethera of fans.

# UX

## The Strategy

Business goals include gaining traffic to the website. The site will be very pink and all things Barbie related. To keep the audience engaged the articles will be current, fun and informative. There will be a wide range from the history of Barbie to the realease and cast of the new movie.
The website features include:

* User registration.
* Users that have not signed in will not be able to add new articles to the wiki.
* Log in / Log out.
* Create new article.
* Read the full article.
* Update/edit that article, only the articles author can edit.
* Delete their article.
* Comment on articles.

## The Scope

The Barbie wiki is designed for Barbie enthusiasts, collectors and fans of all ages. The wiki will cover a range of topics related to Barbie from the movie to dolls, to merchandise and history. The wiki will encourage collaborations and contributions from a diverse group of users, who share a common interest in Barbie.

## The Structure

The navigation is clear at the top of the page with register and login labelled. Once the user has registered and logged in. The articles are displayed on the landing page. The landing page displays a brief paragraph of what the site is about, informing users to register. Articles are displayed in cards showing the summary and the image. The detail button allows users to click and read the full article. Users can then comment on each others articles. The number of comments on each article is displayed on the summary card. Authors of the articles will have an 'edit' button appear. Here the user can update their article and save it. From here they can also delete their article.

## The Skeleton

The wiki site has a number of pages clearly labelled in the nav bar. Along with pink buttons to take users to the relevant page.
The wiki is responsive to be able to use on small and large devices.

[Wire Frames](https://www.figma.com/file/hSTlhp779Rip0GVPMj0gEr/Untitled?type=design&node-id=0-1&mode=design)



## The Surface

To maintain the Barbie theme, the site uses consistent colouring of pink shades. I have chosen a Google font that is similar to the Barbie official font for headings and the nav bar. For the text body a playful rounded font was chosen.

Heading Font
![Heading Font](/flaskr/static/img/h-font.jpg)

Body Font
![Body Font](/flaskr/static/img/body-font.jpg)

 The colours are consistent throughout the wiki. 

![Colour Palette](/flaskr/static/img/colour.jpg)

# Features left to implement

* Features that are left to implement include 'admin rights' and a search or filter option. Time constraints have prevented me from developing these. These may be added in the future.

# Technologies Used

To help me create this website I used these technologies:

* [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
* [Materialize 1.0.0](https://materializecss.com/)
* [W3Schools](https://www.w3schools.com/)
* [Google Fonts](https://fonts.google.com/)
* [Google Developer Tools](https://developer.chrome.com/docs/devtools/)
* [Github](https://github.com/)
* [W3C Markup Validation Service](https://validator.w3.org/)
* [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/validator)
* [Flask](https://flask.palletsprojects.com/en/2.3.x/)
* [Stack Overflow](https://stackoverflow.com/)
* [Heroku](https://heroku.com/)
* [ElephantSQL](https://api.elephantsql.com/)


# Data Schema

The data schema consists of tables. Each table is defined with spefic columns to store information related to users, articles and comments.
![User table](/flaskr/static/img/table-1.jpg)

As you can see from the screenshot above the 'id' is a unique identifier for each user. The username must be unique and cannot be Null.

![Article table](/flaskr/static/img/table-2.jpg)

Again a unique 'id' for each article. 'author_id': Foreign key referencing the 'id' column of the 'user' table, defining the author of the article. 'created' The timestamp of when the article was created, cannot be Null. 'title' 'summary' 'body' all cannot be Null. 'img' A field for storing the image associated with the article.

![Comments table](/flaskr/static/img/table-3.jpg)

Similar to the article table with the addition of 'article_id': Foreign key referencing the 'id' column of the article table. Identifying the article to which the comment belongs to.

# Testing

Tests are used in web development to ensure the code works as expected.
Tests have been created to cover:

* Basic functionality testing.
* User authentication and authorisation.
* Data retrieval and storage.
* Error hansdling.
* User interface and responsiveness.

The testing is comprised of unit test using Pytest and testing the whole application, simulating user interaction.

1.Functionality:

Verify that the home page displays correctly with the nar bar clearly showing navigation.
Confirm that clicking on register and log in are functioning.
Test the creating, updating, deleting and adding comments to articles.
Counts the number of comments attached to each article.

2.User Authentication:

Verify that registered users can log in and access articles. Authors of articles can edit and delete their article, whereas no one else can.
Check that unathorised users are directed to the registration page.
Ensure that users can view all articles but only edit their own.

3.Data Retrival and Storage

Test fetching articles and ensure their content is correct.
Verify that edits to articles are correctly stored in the database.

4.Error Handling

Test the behaviour when a user is already registered
Test handling of incorrect password
Test the behaviour when a user attempts to delete articles that are not their own.

5.UI and responsivness

Verify the responsiveness of the application on different devices and screen sizes.
Test user interactions, input fields and button clicks.

# Unit tests

![Unit testing](/flaskr/static/img/unit-test.jpg)

# Manual testing for my project

The project was tested on the browsers listed below:
 * Chrome *v.116.0.5845.111* 
 * Opera *v.102.0.4871.0*
 * Firefox *v.117.0*
 * Safari *v.16.6*
 * Edge *v.116.0.1938.62*

 When deploying the project I had some issues with Heroku. The main problem being that I did not have the correct file for Heroku to run the app. I added a run.py file to the project to include how the app runs, which solved the problem.

 During testing, once deployed, it become apparant that the users and the data being inserted into the app was not being saved. I was using SQLite for my database. Thorough reasearch led to reading Heroku's ephemeral file system makes it unsuitable for SQLite databases. Heroku's file system is read-only, and any changes made to the file system will be lost whenever the application is restarted or scaled up. I then changed my code to accomodate Postgresql, to finally get the deployment correct.

![Further testing](/flaskr/static/img/test-ex.jpg)

# User Stories

## User - 1

First time visitor wants to understand what the purpose of the website is.

* Landing page shows a large heading with paragraph, clear register tab in nav.

![Landing page](/flaskr/static/img/user-story-1.jpg)

## User - 2

First time visitor wants to be able to see some articles before they register. Articles are visible but user can not read them or add new article without registering and logging in.

![Landing page](/flaskr/static/img/user-story-2.jpg)

## User - 3

First time visitor has registered and logged in. They can add an article and read the existing articles, commenting if they wish.

![User-3](/flaskr/static/img/user-story-3.jpg)

## User - 4

The author of an article wants to update the information. This can only be done by the author, the edit button will be visible, taking the user to the correct view. The user can also delete the article form here.

![User-4](/flaskr/static/img/user-story-4a.jpg)

## User - 5

First time visitor wants to be able to read the full article and see when it was posted and by whom

![User-5](/flaskr/static/img/user-story-5.jpg)

## User - 6

First time users and existing users want to be able to comment on articles, developing a community. The comment button takes them to the comment view.

![User-6](/flaskr/static/img/user-story-6.jpg)

## User - 7

First time users and existing users want to delete the article they have posted.

![User-7](/flaskr/static/img/user-story-7.jpg)
# Validation

CSS

All CSS was passed through the W3C CSS Validation Service, no errors reported
![CSS](/flaskr/static/img/css-val1.jpg)

Lighthouse
![Lighthouse](/flaskr/static/img/lighthouse.jpg)

Pep8

All code is Pep8 compliant, no errors. [Pep8](https://peps.python.org/pep-0008/)

# Deployment

As part of the criteria for this project, the Barbie Wiki has to be deployed to Heroku.

To do this the following must be completed:

1. Create a requirements.txt file so Heroku can install the required dependencies to run the app. This can be done by typing in the terminal.
   * pip3 freeze --local > requirements.txt

2. Create a Procfile to tell Heroku what type of application is being deployed and how to run it.

   * echo web: python run.py > Procfile

3. Sign up and create a Heroku account. 

4. Select the 'New' tab and click create new app. Insert your app name and choose a region. Click create app.

5. Make your way to the Deploy tab. Select 'Connect to Github' for the deployment method. Select your correct repository and connect to it.

6. Before you click deploy, go to the Settings tab, click on the Reveal Config Vars tab to configure environmental variables. Insert the following
   * IP:  0,0,0,0
   * PORT:  5000
   * DATABASE_NAME:  *Your db name*
   * SECRET_KEY:  *Your own secret key*

7. Go back to the Deployment tab and select 'Deploy Branch'

8. You app should now be deployed.

