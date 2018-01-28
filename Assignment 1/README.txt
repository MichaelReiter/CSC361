University of Victoria
Spring 2018
CSC 361 Assignment 1
Michael Reiter
V00831568

--------------------------------------------------------------------------

Instructions for running (for use in a Unix environment)

- To run my code, simply execute `python3 smart_client.py <some url>` from the terminal.

--------------------------------------------------------------------------

Notes

- Python 3.6 or greater must be installed.
- This web client supports 6 HTTP status codes: 200, 404, 503, 505, 301 and 302
- Occasionally requests will fail for unknown reasons (likely packet loss or server-side issues). Simply retry a couple times and it should resolve itself.
