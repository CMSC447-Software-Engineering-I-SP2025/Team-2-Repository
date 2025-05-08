import server

# Dummy spoonacular query based on:
FAKE_SPOONACULAR_RESPONSE = {

}
def test_api_get_recipes():
    assert server.api_get_recipes() == []

'''
TODO
Use flask test client
simulates a client calling recipes route instead of needing backend hosted and accepting requests

Use mock to simulate querying from spponacular
'''

