# Crew Rates
Live at [crewrates.org](https://crewrates.org) (user account required to sign in)

<div align="center">
<img src="https://user-images.githubusercontent.com/39425112/166316498-8c7e9f78-bea5-4ebc-bbda-0c0b459afbc8.png" width="320">
</div>

## Introduction
It can be hard for crew members on film and TV productions to get rate information to help them 
effectively negotiate their pay and know their market value.

- They can communicate with each other individually, but that method has limited reach
- Private groups on social media platforms allow for sharing information, but people are
often reluctant to share when their name is attached to a post, and there's no easy way to search 
historical data or analyze trends
- Large commercial salary-sharing platforms allow for anonymous sharing, but they're designed
primarily for salaried office workers, so they don't provide an effective format for
workers who are paid by the hour or the day on a per-project basis for many employers

Crew Rates provides a platform that's invitation-only and anonymous, so users can be sure that
information they share stays within their community and can't be tied to their identity. It uses
a questionnaire format that's specifically designed to capture the information that's relevant to
the types of jobs they do.

The questionnaire also asks whether the user attempted to negotiate a rate higher than the one that
was offered — this provides a "nudge" that normalizes negotiating as a routine part
of booking a job, and allows other users to see how much of an increase was gained.

Users can view a reverse-chronological scroll of submitted rates, or filter and search by a variety 
of attributes like date, union status and genre. If a user filters on job title, they get a histogram
chart showing the distribution of rates for that job title.

## Design

The app is built on the Django framework and uses django-allauth for authentication and Postgres
as a database. The frontend uses a hybrid Django/React model: authentication pages,
user account setting pages, the contact form and static pages are rendered by Django using its
templating system, while the Discover and Add a Rate pages are single-page React apps that
communicate with the backend using Django Rest Framework APIs.

The questionnaire uses DRF APIs to populate options lists for autocomplete searches from the database,
and integrates with the Google Places API to validate location information.

I've deployed the app on AWS using Elastic Beanstalk, which makes it easy to push incremental
changes to production. Static files are served using Cloudfront, and transactional email is handled
by Simple Email Service.

After beta testing the app with a small group of users, I launched it in the summer of 2022, and it
quickly gained traction with its target audience.

I'm continuing to refine the app and develop new features, including:

- Web push notifications
- More flexible filtering and histogram charts

## UI Demos

UI design for the app is mobile-first, since most crew members will be using it while working on
set.

<div align="center">

| ![Sign in page](https://user-images.githubusercontent.com/39425112/166314491-bc307c91-e3d2-4c6a-ab30-b42922a108b2.gif) |
| :----: |
| **Sign in page with social and email options leads to the Discover page with a reverse-chronological scroll of recent rate submissions.** |

</div>

<div align="center">

| ![Filter rates by company](https://user-images.githubusercontent.com/39425112/166315199-0ae87b69-fc2f-441b-947b-d191dec44f15.gif) |
| :----: |
| **Users can filter rates by show, company, network, or job title.** |

</div>

<div align="center">

| ![Job Title Summary](https://user-images.githubusercontent.com/39425112/166315843-803d59b9-d404-4cd1-a092-1d076e73baf0.gif) |
| :----: |
| **When a user filters rates by job title, a summary chart appears which can be further refined by date, union status or genre.** |

</div>
<div align="center">

| ![Add a Rate form, page one](https://user-images.githubusercontent.com/39425112/235544859-68d9c78b-e273-446d-99f3-2702fb8a7542.gif) |
| :----: |
| **Add a Rate form, page one: autocomplete options are provided from the database, and the location field is integrated with Google Places API.** |

</div>

<div align="center">

| ![Add a Rate form, page two](https://user-images.githubusercontent.com/39425112/166316302-901dd9b2-c28b-4bfa-8946-ad2c0ebbda0a.gif) |
| :----: |
| **Add a Rate form, page two: captures whether user attempted to negotiate a higher rate, and if so, how much of an increase they received.** |

</div>
