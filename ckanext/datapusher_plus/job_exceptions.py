class DataTooBigError(Exception):
    pass


class JobError(Exception):
    """The exception type that jobs raise to signal failure.

    Also exported as utils.JobError, which is the name most of the codebase
    uses. It has to be a single class: HTTPError below is declared a JobError,
    and if the two names were different classes, `except utils.JobError` would
    not catch it.
    """

    def __init__(self, message):
        """Initialize a JobError with the given error message string.
        The error message string that you give here will be returned to the
        client site in the job dict's "error" key.
        """
        super(JobError, self).__init__(message)
        self.message = message

    def as_dict(self):
        """Return a dictionary representation of this JobError object.
        Returns a dictionary with a "message" key whose value is a string error
        message - suitable for use as the "error" key in a ckanserviceprovider
        job dict.
        """
        return {"message": self.message}

    def __str__(self):
        return self.message


class FileCouldNotBeLoadedError(Exception):
    pass


class HTTPError(JobError):
    """Exception that's raised if a job fails due to an HTTP problem."""

    def __init__(self, message, status_code, request_url, response):
        """Initialise a new HTTPError.
        :param message: A human-readable error message
        :type message: string
        :param status_code: The status code of the errored HTTP response,
            e.g. 500
        :type status_code: int
        :param request_url: The URL that was requested
        :type request_url: string
        :param response: The body of the errored HTTP response as unicode
            (if you have a requests.Response object then response.text will
            give you this)
        :type response: unicode
        """
        super(HTTPError, self).__init__(message)
        self.status_code = status_code
        self.request_url = request_url
        self.response = response

    def as_dict(self):
        """The status code and URL are returned as their own keys.

        The resource_data template prints "message" as the error and lists
        every other key beneath it, so they show up as labelled details rather
        than being crammed into the message.
        """
        error_dict = {"message": self.message}
        if self.status_code is not None:
            error_dict["status_code"] = self.status_code
        if self.request_url:
            error_dict["request_url"] = self.request_url
        return error_dict

    def __str__(self):
        details = []
        if self.status_code is not None:
            details.append("status={}".format(self.status_code))
        if self.request_url:
            details.append("url={}".format(self.request_url))
        if details:
            return "{} ({})".format(self.message, ", ".join(details))
        return str(self.message)


class LoaderError(JobError):
    """Exception that's raised if a load fails"""

    pass


class InvalidErrorObjectError(Exception):
    pass
