from typing import Any

HTTP_100_CONTINUE = 100
HTTP_101_SWITCHING_PROTOCOLS = 101
HTTP_102_PROCESSING = 102
HTTP_103_EARLY_HINTS = 103
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_202_ACCEPTED = 202
HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203
HTTP_204_NO_CONTENT = 204
HTTP_205_RESET_CONTENT = 205
HTTP_206_PARTIAL_CONTENT = 206
HTTP_207_MULTI_STATUS = 207
HTTP_208_ALREADY_REPORTED = 208
HTTP_226_IM_USED = 226
HTTP_300_MULTIPLE_CHOICES = 300
HTTP_301_MOVED_PERMANENTLY = 301
HTTP_302_FOUND = 302
HTTP_303_SEE_OTHER = 303
HTTP_304_NOT_MODIFIED = 304
HTTP_305_USE_PROXY = 305
HTTP_306_RESERVED = 306
HTTP_307_TEMPORARY_REDIRECT = 307
HTTP_308_PERMANENT_REDIRECT = 308
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_402_PAYMENT_REQUIRED = 402
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_406_NOT_ACCEPTABLE = 406
HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407
HTTP_408_REQUEST_TIMEOUT = 408
HTTP_409_CONFLICT = 409
HTTP_410_GONE = 410
HTTP_411_LENGTH_REQUIRED = 411
HTTP_412_PRECONDITION_FAILED = 412
HTTP_413_REQUEST_ENTITY_TOO_LARGE = 413
HTTP_414_REQUEST_URI_TOO_LONG = 414
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE = 416
HTTP_417_EXPECTATION_FAILED = 417
HTTP_418_IM_A_TEAPOT = 418
HTTP_421_MISDIRECTED_REQUEST = 421
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_423_LOCKED = 423
HTTP_424_FAILED_DEPENDENCY = 424
HTTP_425_TOO_EARLY = 425
HTTP_426_UPGRADE_REQUIRED = 426
HTTP_428_PRECONDITION_REQUIRED = 428
HTTP_429_TOO_MANY_REQUESTS = 429
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = 451
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_501_NOT_IMPLEMENTED = 501
HTTP_502_BAD_GATEWAY = 502
HTTP_503_SERVICE_UNAVAILABLE = 503
HTTP_504_GATEWAY_TIMEOUT = 504
HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505
HTTP_506_VARIANT_ALSO_NEGOTIATES = 506
HTTP_507_INSUFFICIENT_STORAGE = 507
HTTP_508_LOOP_DETECTED = 508
HTTP_509_BANDWIDTH_LIMIT_EXCEEDED = 509
HTTP_510_NOT_EXTENDED = 510
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511

# informational
CONTINUE = 100, "Continue", "Request received, please continue"
SWITCHING_PROTOCOLS = (101, "Switching Protocols", "Switching to new protocol; obey Upgrade header")
PROCESSING = 102, "Processing"
EARLY_HINTS = 103, "Early Hints"

# success
OK = 200, "OK", "Request fulfilled, document follows"
CREATED = 201, "Created", "Document created, URL follows"
ACCEPTED = (202, "Accepted", "Request accepted, processing continues off-line")
NON_AUTHORITATIVE_INFORMATION = (203, "Non-Authoritative Information", "Request fulfilled from cache")
NO_CONTENT = 204, "No Content", "Request fulfilled, nothing follows"
RESET_CONTENT = 205, "Reset Content", "Clear input form for further input"
PARTIAL_CONTENT = 206, "Partial Content", "Partial content follows"
MULTI_STATUS = 207, "Multi-Status"
ALREADY_REPORTED = 208, "Already Reported"
IM_USED = 226, "IM Used"

# redirection
MULTIPLE_CHOICES = (300, "Multiple Choices", "Object has several resources -- see URI list")
MOVED_PERMANENTLY = (301, "Moved Permanently", "Object moved permanently -- see URI list")
FOUND = 302, "Found", "Object moved temporarily -- see URI list"
SEE_OTHER = 303, "See Other", "Object moved -- see Method and URL list"
NOT_MODIFIED = (304, "Not Modified", "Document has not changed since given time")
USE_PROXY = (305, "Use Proxy", "You must use proxy specified in Location to access this resource")
TEMPORARY_REDIRECT = (307, "Temporary Redirect", "Object moved temporarily -- see URI list")
PERMANENT_REDIRECT = (308, "Permanent Redirect", "Object moved permanently -- see URI list")

# client error
BAD_REQUEST = (400, "Bad Request", "Bad request syntax or unsupported method")
UNAUTHORIZED = (401, "Unauthorized", "No permission -- see authorization schemes")
PAYMENT_REQUIRED = (402, "Payment Required", "No payment -- see charging schemes")
FORBIDDEN = (403, "Forbidden", "Request forbidden -- authorization will not help")
NOT_FOUND = (404, "Not Found", "Nothing matches the given URI")
METHOD_NOT_ALLOWED = (405, "Method Not Allowed", "Specified method is invalid for this resource")
NOT_ACCEPTABLE = (406, "Not Acceptable", "URI not available in preferred format")
PROXY_AUTHENTICATION_REQUIRED = (
  407,
  "Proxy Authentication Required",
  "You must authenticate with this proxy before proceeding",
)
REQUEST_TIMEOUT = (408, "Request Timeout", "Request timed out; try again later")
CONFLICT = 409, "Conflict", "Request conflict"
GONE = (410, "Gone", "URI no longer exists and has been permanently removed")
LENGTH_REQUIRED = (411, "Length Required", "Client must specify Content-Length")
PRECONDITION_FAILED = (412, "Precondition Failed", "Precondition in headers is false")
CONTENT_TOO_LARGE = (413, "Content Too Large", "Content is too large")
REQUEST_ENTITY_TOO_LARGE = CONTENT_TOO_LARGE
URI_TOO_LONG = (414, "URI Too Long", "URI is too long")
REQUEST_URI_TOO_LONG = URI_TOO_LONG
UNSUPPORTED_MEDIA_TYPE = (415, "Unsupported Media Type", "Entity body in unsupported format")
RANGE_NOT_SATISFIABLE = (416, "Range Not Satisfiable", "Cannot satisfy request range")
REQUESTED_RANGE_NOT_SATISFIABLE = RANGE_NOT_SATISFIABLE
EXPECTATION_FAILED = (417, "Expectation Failed", "Expect condition could not be satisfied")
IM_A_TEAPOT = (418, "I'm a Teapot", "Server refuses to brew coffee because it is a teapot.")
MISDIRECTED_REQUEST = (421, "Misdirected Request", "Server is not able to produce a response")
UNPROCESSABLE_CONTENT = 422, "Unprocessable Content"
UNPROCESSABLE_ENTITY = UNPROCESSABLE_CONTENT
LOCKED = 423, "Locked"
FAILED_DEPENDENCY = 424, "Failed Dependency"
TOO_EARLY = 425, "Too Early"
UPGRADE_REQUIRED = 426, "Upgrade Required"
PRECONDITION_REQUIRED = (428, "Precondition Required", "The origin server requires the request to be conditional")
TOO_MANY_REQUESTS = (
  429,
  "Too Many Requests",
  'The user has sent too many requests in a given amount of time ("rate limiting")',
)
REQUEST_HEADER_FIELDS_TOO_LARGE = (
  431,
  "Request Header Fields Too Large",
  "The server is unwilling to process the request because its header fields are too large",
)
UNAVAILABLE_FOR_LEGAL_REASONS = (
  451,
  "Unavailable For Legal Reasons",
  "The server is denying access to the resource as a consequence of a legal demand",
)

# server errors
INTERNAL_SERVER_ERROR = (500, "Internal Server Error", "Server got itself in trouble")
NOT_IMPLEMENTED = (501, "Not Implemented", "Server does not support this operation")
BAD_GATEWAY = (502, "Bad Gateway", "Invalid responses from another server/proxy")
SERVICE_UNAVAILABLE = (503, "Service Unavailable", "The server cannot process the request due to a high load")
GATEWAY_TIMEOUT = (504, "Gateway Timeout", "The gateway server did not receive a timely response")
HTTP_VERSION_NOT_SUPPORTED = (505, "HTTP Version Not Supported", "Cannot fulfill request")
VARIANT_ALSO_NEGOTIATES = 506, "Variant Also Negotiates"
INSUFFICIENT_STORAGE = 507, "Insufficient Storage"
LOOP_DETECTED = 508, "Loop Detected"
NOT_EXTENDED = 510, "Not Extended"
NETWORK_AUTHENTICATION_REQUIRED = (
  511,
  "Network Authentication Required",
  "The client needs to authenticate to gain network access",
)


class DomainException(Exception):
  def __init__(
    self,
    detail: str,
    status_code: int,
    default_message: str,
    extra_data: dict | None = None,
  ):
    self.detail = detail
    self.status_code = status_code
    self.default_message = default_message
    self.extra_data = extra_data or {}

  def to_dict(self) -> dict[str, Any]:
    return {
      "detail": self.detail,
      "status_code": self.status_code,
      "message": self.default_message,
      "extra_data": self.extra_data,
    }
