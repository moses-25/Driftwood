"""
Standardized response formatters
Provides consistent API response format across all endpoints
"""
from flask import jsonify
from math import ceil


def success_response(data=None, message=None, status_code=200):
    """
    Standard success response

    Args:
        data: Response data payload
        message: Success message
        status_code: HTTP status code (default: 200)

    Returns:
        tuple: (flask Response, status_code)
    """
    response = {'success': True}

    if message:
        response['message'] = message

    if data is not None:
        response['data'] = data

    return jsonify(response), status_code


def created_response(data=None, message='Resource created successfully'):
    """
    Standard created response (201)

    Args:
        data: Response data payload
        message: Success message

    Returns:
        tuple: (flask Response, 201)
    """
    return success_response(data=data, message=message, status_code=201)


def error_response(error, status_code=400):
    """
    Standard error response

    Args:
        error: Error message or dict of errors
        status_code: HTTP status code (default: 400)

    Returns:
        tuple: (flask Response, status_code)
    """
    response = {
        'success': False,
        'error': error
    }

    return jsonify(response), status_code


def not_found_response(resource='Resource'):
    """
    Standard not found response (404)

    Args:
        resource: Name of the resource not found

    Returns:
        tuple: (flask Response, 404)
    """
    return error_response(f'{resource} not found', 404)


def forbidden_response(message='Insufficient permissions'):
    """
    Standard forbidden response (403)

    Args:
        message: Error message

    Returns:
        tuple: (flask Response, 403)
    """
    return error_response(message, 403)


def unauthorized_response(message='Authentication required'):
    """
    Standard unauthorized response (401)

    Args:
        message: Error message

    Returns:
        tuple: (flask Response, 401)
    """
    return error_response(message, 401)


def validation_error_response(errors):
    """
    Standard validation error response (400)

    Args:
        errors: Validation error messages (dict or list)

    Returns:
        tuple: (flask Response, 400)
    """
    return error_response(errors, 400)


def paginated_response(items, page, per_page, total, message=None):
    """
    Standard paginated response

    Args:
        items: List of items for current page
        page: Current page number
        per_page: Items per page
        total: Total number of items
        message: Optional success message

    Returns:
        tuple: (flask Response, 200)
    """
    total_pages = ceil(total / per_page) if per_page > 0 else 0

    response = {
        'success': True,
        'data': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }

    if message:
        response['message'] = message

    return jsonify(response), 200
