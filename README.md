# Bank reader

[![Build Status](https://travis-ci.org/silvanocerza/bank-reader.svg?branch=master)](https://travis-ci.org/silvanocerza/bank-reader)
[![Coverage Status](https://coveralls.io/repos/github/silvanocerza/bank-reader/badge.svg?branch=master)](https://coveralls.io/github/silvanocerza/bank-reader?branch=master)

A scraper for my bank account.

# Getting started

To launch the project run `docker-compose up` in root directory.

# Testing

To launch tests a postgres DB is needed so first bring it up.

    docker-compose -f containers/services.yml up
    tox
