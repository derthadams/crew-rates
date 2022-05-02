# Crew Rates
Live at [crewrates.org](https://crewrates.org) (user account required)

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

One of the first things design considerations was the question of anonymity: how deep did it have
to go? Was it enough to just display shared rate information without names attached, or did the
backend design also have to mask the identities of contributors?

In the first iteration of the design, users were
invited using their email address, and could only register using social auth. Once they had 
registered,
the only identifying data retained about them in the application's database was their access 
token from their social auth provider.

After experimenting with the flow and talking to some potential users, I decided that while this 
did provide a higher degree of anonymity, it was a more brittle design that would provide fewer
fail-safes in case the user had problems with their account. Some potential users also said they 
preferred
to create their own app-specific credentials rather than using a social auth provider. Currently 
the design includes registration by both social auth and email/password.

The app is built on the Django framework with a Postgres database and uses django-allauth for 
authentication. The frontend uses a hybrid model between Django and React: authentication pages,
user account setting pages, the contact form and static pages are rendered by Django using its 
templating system, while the Discover and Add a Rate pages are single-page React apps that 
communicate with Django Rest Framework APIs.

The questionnaire uses Django API endpoints to populate options lists for autocomplete searches,
and integrates with the Google Places API to validate location information.

I've deployed the app on AWS using Elastic Beanstalk, which makes it easy to push incremental
changes to production. Static files are served using Cloudfront, and transactional email is handled
by Simple Email Service.

Recently I invited a small group of people to use the app as Beta testers so that I can identify
any usability issues, and so I can see how the app performs under load. I've instrumented the app
using New Relic and have been checking the logs to see if there are any slow database queries or
other bottlenecks.

## Screenshots

UI design for the app is mobile-first, since most crew members will be using it while working on
set.

<div align="center">

<video autoplay loop muted playsinline src="https://user-images.githubusercontent.com/39425112/166310613-37023283-926a-49bf-b24c-e8c940f2c24e.mp4" width="400"/>
**Sign in page with social and email options leads to the Discover page with a reverse-chronological scroll of recent rate submissions.**

</div>

<div align="center">

| ![Filter rates by company](https://user-images.githubusercontent.com/39425112/166304226-bbb87e59-2ec3-4719-b3df-e70d1c51f274.gif) |
| :----: |
| **Users can filter rates by show, company, network, or job title.** |

</div>

<div align="center">

| ![Job Title Summary](https://user-images.githubusercontent.com/39425112/166305338-e4bf97e8-ca89-4f6e-8731-4f8961df2400.gif) |
| :----: |
| **When a user filters by job title, a summary chart appears which can be further refined by date, union status or genre.** |

</div>
<div align="center">

| ![Add a Rate form, page one](https://user-images.githubusercontent.com/39425112/166305725-b8b42951-8854-4189-8a4e-d89bca3734bc.gif) |
| :----: |
| **Add a Rate form, page one: autocomplete options are provided from the database, and the location field is integrated with Google Places API.** |

</div>

<div align="center">

| ![Add a Rate form, page two](https://user-images.githubusercontent.com/39425112/166306020-7bb30ad5-2ce5-48af-a226-6961628dfbb9.gif) |
| :----: |
| **Add a Rate form, page two: captures whether user attempted to negotiate rate, and if so, how much of an increase they received.** |

</div>
