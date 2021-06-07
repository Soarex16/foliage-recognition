const STATUS_UNPROCESSABLE_ENTITY = 422;

/**
 * Sends request to backend for image recognition
 * @param apiUrl - backend url
 * @param formData - data to send
 * @return {Promise<any>} - promise that resolves with request result
 * @throws {AppError} - request error if happens
 */
export async function recognize(apiUrl, formData) {
    const response = await fetch(`${apiUrl}/recognize/json`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        let respErr = await tryFormatError(response);
        throw new AppError(respErr);
    }

    const parsedResponse = await response.json();

    return parsedResponse;
}

export class AppError extends Error {
    constructor(err) {
        super();
        this.details = err;
    }
}

/**
 * Helper function for error formatting
 * @param response {Response} - API response
 * @return {Promise<string|{errorText, errorBody}>}
 */
async function tryFormatError(response) {
    let responseMessage;
    try {
        responseMessage = await response.json();

        if (response.status === STATUS_UNPROCESSABLE_ENTITY)
            return formatValidationError(responseMessage);
    } catch (e) {
        responseMessage = await response.text();
    }

    return responseMessage || response.statusText;
}

function formatValidationError(err) {
    const errorTitle = err.error;
    const errorBody = err.detail.map(err => [err.loc[1], err.msg]);
    return {
        errorTitle,
        errorBody
    };
}
