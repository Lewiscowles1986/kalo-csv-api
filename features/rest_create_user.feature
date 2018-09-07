Feature: Creating user resources.

  Scenario: A request for creating a resource with a known valid value.
    When the request body is assigned:
      """
      {"name":"Jet Li",
      "timezone":"GMT",
      "skills":"Being the one, killing selves in the multiverse"}
      """
    And a POST is sent to `/users`
    And the request header `Content-Type` is assigned `application/json`
    Then the value of the response status is equal to `201`
    And the value of the response body child `data` is including:
      """
      {"name":"Jet Li"}
      """
    And the value of the response body child `data` is including:
      """
      {"timezone":"GMT"}
      """
    And the value of the response body child `data.skills` is a valid `Array`
    And the value of the response body child `data.skills` is including:
      """
      "killing selves in the multiverse"
      """
    And the value of the response body child `data.skills` is including:
      """
      "Being the one"
      """
    And the value of the response body child `links` is a valid `Array`
    And the value of the response body child `links[0]` is including:
      """
      {"Rel": "time"}
      """
    And the value of the response body child `links[0]` is including:
      """
      {"Type": "GET"}
      """
    And the value of the response body child `links[1]` is including:
      """
      {"Rel": "listing"}
      """
    And the value of the response body child `links[1]` is including:
      """
      {"Type": "GET"}
      """

  Scenario: A request for creating a resource with a known valid value.
    When the request body is assigned:
      """
      {"name":"Jet Li",
      "timezone":"La la land",
      "skills":"@~#323weywdhsjn"}
      """
    And the request header `Content-Type` is assigned `application/json`
    And a POST is sent to `/users`
    Then the value of the response status is equal to `400`
    And the value of the response body child `errors` is a valid `Array`
