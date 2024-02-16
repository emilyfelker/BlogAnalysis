import os
import pytest
from BlogAnalysis.data import get_response_from_database, get_database, add_to_database

database_file = "../tests/test.db"


def database_connection():  # setup
    connection = get_database(database_file)
    return connection


def finalize():  # teardown
    if os.path.exists(database_file):
        os.remove(database_file)


def test_get_response_from_database_single_match():
    # Add a single record to the database
    add_to_database(database_connection(), 'test_query', 'test_model', 'test_response')

    # Retrieve the response
    response = get_response_from_database(database_connection(), 'test_query', 'test_model')

    finalize()

    # Assert that the response matches the one added
    assert response == 'test_response'


def test_get_response_from_database_multiple_matches():
    # Add multiple records with the same query and model to the database
    add_to_database(database_connection(), 'test_query', 'test_model', 'response1')
    add_to_database(database_connection(), 'test_query', 'test_model', 'response2')

    # Retrieve the response and expect a LookupError
    with pytest.raises(LookupError) as excinfo:
        get_response_from_database(database_connection(), 'test_query', 'test_model')

    finalize()

    # Assert that the function raises a LookupError with the expected message
    assert "Expected only 1 result but found 2" in str(excinfo.value)
