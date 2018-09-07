Feature: Absent resources return 404s.

  Scenario: A request for a known missing resource.
    When a GET is sent to `/users/ced7f0ac-f6f1-4f82-9890-f1dea2868ed9/time`
    Then the value of the response status is equal to `404`

  Scenario: A request for a known missing resource.
    When the request body is assigned:
      """
      {"name":"Jet Li",
      "timezone":"GMT",
      "skills":"Being the one, killing selves in the multiverse"}
      """
    And a PUT is sent to `/users/ced7f0ac-f6f1-4f82-9890-f1dea2868ed9`
    Then the value of the response status is equal to `404`
