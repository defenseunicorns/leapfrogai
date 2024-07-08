# Testing Strategy

## Table of Contents

- [Testing Strategy](#Testing-Strategy)
  - [Table of Contents](#table-of-contents)
  - [Status](#status)
  - [Background](#background)
  - [Decisions](#decisions)
  - [Design](#Design)
  - [Alternatives](#alternatives)
  - [References](#references)
  - [Notes](#Notes)

## Status 
- PROPOSED

## Context
We need to have a consolidated and clearly defined approach to testing our systems. Currently, we don't have a clear definition of what features and functions should be tested at each level, and we mix some integration and system testing.

It is also currently difficult for new developers to spin up a test suite in a new environment. We should have tests work out of the box.

## Decisions

(1) We should clearly define the levels of testing that we want to do, and the features that we should test at each one.
* Unit Testing
* Integration Testing
* System Testing
* User Acceptance Testing

(2) We should not require 100% code coverage for testing.

**PROS**: 
Faster development, less redundant work.
Faster and leaner test runs.

**CONS**:
Coverage is up to devs and can lapse.

(3) Tests should be granular, and each test should test an individual feature. Avoid monolithic test functions.

(4) We should be testing for both success and failure cases. We do not need to create custom error codes or return types for each error, we just need to make sure we are testing for all edge cases.

(5) Tests should mock out the layers that they are not testing, to isolate the program code being tested. We can use utils like `unittest.mock.patch`, `unittest.mock.MagicMock`, `unittest.mock.AsyncMock`, and others

(6) We should use `pytest.mark.parametrize` to iterate over parameter lists for test function instead of creating iteration loops inside test code. This method will break out each test run by parameter combinations and makes it easier to find failing conditions.

(7) We should use `conftest.py` to set up the dev environment variables, and to create global test fixtures.

(8) We should consider all testing environments:
* Windows
* MacOS
* Linux
* Kubernetes

## Design

### Unit Testing
* Test individual functions and class methods.
* Test result of data transformations.
* Test result of call routing
* Test data validation
* Test exception handling

### Integration Testing
* API endpoints are up and respond to defined methods
* API endpoints require authentication
* API authentication works
* API can access the database
* Service A can access service B
* Database follows Role-Based Access Control (RBAC)
* Database CRUD on all tables

### System Testing 
* End-to-End testing
* Stress testing
* Response latency
* K8 node validation 
* Network testing
* RAG performance
* Model performance

### User Acceptance Testing
* Users test application for defined set of features
* Users test application usability and accessibility
* Users evaluate LLM output quality and relevance

## Alternatives
Supabase has it's own testing framework that we need to consider.

## References
* [Understanding the Python Mock Object Library](https://realpython.com/python-mock-library/)

* [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html)

## NOTES

We need to integrate UI testing strategy into this document.

