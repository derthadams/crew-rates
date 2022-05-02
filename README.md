# Crew Rates
Live at [crewrates.org](https://crewrates.org) (user account required to sign in)

<div align="center">
<img src="https://user-images.githubusercontent.com/39425112/166316498-8c7e9f78-bea5-4ebc-bbda-0c0b459afbc8.png" width="320">
</div>

## Introduction
It can be hard for crew members on film and TV productions to effectively negotiate their pay
and know their market value. They want to know what their peers are currently getting paid,
but there's no scalable, anonymous way to trade that information.

- They can communicate with each other individually, but that method has limited reach.
- Private groups on social media platforms allow for sharing information, but people are
often reluctant to share when their name is attached to a post.
- Large commercial salary-sharing platforms allow for anonymous sharing, but they're designed
primarily for salaried office workers, so they don't provide an effective format for
workers who are paid by the hour or the day on a per-project basis for many different employers.

Crew Rates provides a platform that's invitation-only and anonymous, so users can be sure that
information they share stays within their community and can't be tied to their identity. It uses
a questionnaire format that's specifically designed to capture the information that's relevant to
the types of jobs they do.

## Design

The app is built on the Django framework with a Postgres database and uses django-allauth for 
authentication. The frontend uses a hybrid Django/React model: authentication pages,
user account setting pages, the contact form and static pages are rendered by Django using its 
templating system, while the Discover and Add a Rate pages are single-page React apps that 
communicate with the backend using Django Rest Framework APIs.

The questionnaire uses DRF APIs to populate options lists for autocomplete searches from the database,
and integrates with the Google Places API to validate location information.

I've deployed the app on AWS using Elastic Beanstalk, which makes it easy to push incremental
changes to production. Static files are served using Cloudfront, and transactional email is handled
by Simple Email Service.

Recently I invited a small group of people to use the app as Beta testers so that I can identify
any usability issues, and to find out how the app performs under load. I've instrumented the app
using New Relic and have been checking the logs to see if there are any slow database queries or
other bottlenecks.

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

| ![Add a Rate form, page one](https://user-images.githubusercontent.com/39425112/166316082-310e41f1-91d6-4aa5-bcc3-6df753fe03f2.gif) |
| :----: |
| **Add a Rate form, page one: autocomplete options are provided from the database, and the location field is integrated with Google Places API.** |

</div>

<div align="center">

| ![Add a Rate form, page two](https://user-images.githubusercontent.com/39425112/166316302-901dd9b2-c28b-4bfa-8946-ad2c0ebbda0a.gif) |
| :----: |
| **Add a Rate form, page two: captures whether user attempted to negotiate a higher rate, and if so, how much of an increase they received.** |

</div>
