STATUS_OK = 200
STATUS_REDIRECT = 302
STATUS_BAD_REQUEST = 400
STATUS_NOT_FOUND = 404
STATUS_SERVER_ERROR = 500

REASON_PHRASES = {
    STATUS_OK: "OK",
    STATUS_REDIRECT: "Found",
    STATUS_BAD_REQUEST: "Bad Request",
    STATUS_NOT_FOUND: "File Not Found",
    STATUS_SERVER_ERROR: "Internal Server Error",
}
