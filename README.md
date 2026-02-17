Project Overview

This project is a scalable UI automation framework built for the ixigo Bus module using Python, Selenium, and Pytest.
It follows industry-standard automation practices such as the Page Object Model (POM), explicit waits, logging, and data-driven testing.

This framework was developed as part of the Advanced Automation Testing Assignment.

Objective

To design and implement a production-ready UI automation framework for the ixigo Bus booking flow with:

Scalable architecture

Clean code structure

Reusable page objects

Robust wait mechanisms

Logging and screenshot capture

20+ independent test cases

Technology Stack

Tool	Usage
Python 3.x	Programming language
Selenium WebDriver	UI automation
Pytest	Test runner
Chrome	Browser for execution
Page Object Model	Design pattern
Logging	Python logging module
Test Data	JSON / YAML
Reporting	pytest-html
Version Control	Git & GitHub

Project Structure

ixigo-automation/
│
├── config/
│   └── config.yaml
│
├── data/
│   └── test_data.json
│
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── bus_results_page.py
│   └── bus_details_page.py
│
├── tests/
│   ├── test_e2e_flow.py
│   ├── test_filters_and_validations.py
│   ├── test_seat_selection.py
│   └── conftest.py
│
├── utils/
│   ├── driver_factory.py
│   ├── logger.py
│   ├── wait_utils.py
│   └── screenshot_utils.py
│
├── reports/
│   └── screenshots/
│
├── requirements.txt
└── README.md

Automated Test Coverage (20+ Test Cases)

1. Search & Basic Validations

Bus search with valid route

Results page load validation

Sort by price

Sort by departure time

AC filter application

2. Filters & Sorting

Sort then apply AC filter

Apply multiple filters

Re-sort results

Verify results after filter

Validate seat layout visibility

3. Seat Selection Flow

Open seat layout

Select available seat

Select boarding point

Select dropping point

Continue to next step

4. End-to-End Flow

Complete booking flow:

Search

Filter

Sort

Seat selection

Boarding & dropping selection

Continue to review

5. Negative Test Scenarios

Continue without seat selection

Boarding selected without seat

Incomplete booking flow validation