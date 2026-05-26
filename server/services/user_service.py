"""
User service layer
Handles business logic for user management
"""
from models.user import User
from models.order import Order
from extensions import db


class UserService:
    """Service class for user operations"""

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get a single user by ID

        Args:
            user_id: The user's ID

        Returns:
            tuple: (user_dict, error_message, status_code)
        """
        try:
            user = User.query.get(user_id)

            if not user:
                return None, "User not found", 404

            return user.to_dict(include_sensitive=True), None, 200

        except Exception as e:
            return None, str(e), 500

    @staticmethod
    def get_user_by_email(email):
        """
        Get a user by email

        Args:
            email: The user's email

        Returns:
            tuple: (user_dict, error_message, status_code)
        """
        try:
            user = User.query.filter_by(email=email).first()

            if not user:
                return None, "User not found", 404

            return user.to_dict(include_sensitive=True), None, 200

        except Exception as e:
            return None, str(e), 500

    @staticmethod
    def get_user_orders(user_id, page=1, per_page=20, status=None):
        """
        Get all orders for a user

        Args:
            user_id: The user's ID
            page: Page number for pagination
            per_page: Number of items per page
            status: Filter by order status (optional)

        Returns:
            tuple: (orders_list, pagination_info, error_message, status_code)
        """
        try:
            query = Order.query.filter_by(user_id=user_id)

            if status:
                query = query.filter_by(status=status)

            query = query.order_by(Order.created_at.desc())

            paginated = query.paginate(page=page, per_page=per_page, error_out=False)

            orders_list = [order.to_dict() for order in paginated.items]

            pagination_info = {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev
            }

            return orders_list, pagination_info, None, 200

        except Exception as e:
            return None, None, str(e), 500

    @staticmethod
    def update_user_profile(user_id, data):
        """
        Update a user's profile

        Args:
            user_id: The user's ID
            data: Dictionary containing updated profile data

        Returns:
            tuple: (user_dict, error_message, status_code)
        """
        try:
            user = User.query.get(user_id)

            if not user:
                return None, "User not found", 404

            # Update fields if provided
            if 'first_name' in data:
                user.first_name = data['first_name']

            if 'last_name' in data:
                user.last_name = data['last_name']

            if 'phone' in data:
                user.phone = data['phone']

            if 'address' in data:
                user.address = data['address']

            if 'username' in data and data['username'] != user.username:
                existing = User.query.filter_by(username=data['username']).first()
                if existing:
                    return None, "Username already taken", 409
                user.username = data['username']

            db.session.commit()

            return user.to_dict(), None, 200

        except Exception as e:
            db.session.rollback()
            return None, str(e), 500

    @staticmethod
    def list_users(page=1, per_page=20, role=None, is_active=None, search=None):
        """
        List all users with filtering and pagination (Admin only)

        Args:
            page: Page number for pagination
            per_page: Number of items per page
            role: Filter by role (optional)
            is_active: Filter by active status (optional)
            search: Search by username or email (optional)

        Returns:
            tuple: (users_list, pagination_info, error_message, status_code)
        """
        try:
            query = User.query

            if role:
                query = query.filter_by(role=role)

            if is_active is not None:
                query = query.filter_by(is_active=is_active)

            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    db.or_(
                        User.username.ilike(search_term),
                        User.email.ilike(search_term),
                        User.first_name.ilike(search_term),
                        User.last_name.ilike(search_term)
                    )
                )

            query = query.order_by(User.created_at.desc())

            paginated = query.paginate(page=page, per_page=per_page, error_out=False)

            users_list = [user.to_dict() for user in paginated.items]

            pagination_info = {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev
            }

            return users_list, pagination_info, None, 200

        except Exception as e:
            return None, None, str(e), 500

    @staticmethod
    def deactivate_user(user_id):
        """
        Deactivate a user account (Admin only)

        Args:
            user_id: The user's ID

        Returns:
            tuple: (success, error_message, status_code)
        """
        try:
            user = User.query.get(user_id)

            if not user:
                return False, "User not found", 404

            if user.role == 'admin':
                return False, "Cannot deactivate admin users", 400

            user.is_active = False
            db.session.commit()

            return True, None, 200

        except Exception as e:
            db.session.rollback()
            return False, str(e), 500

    @staticmethod
    def delete_user(user_id):
        """
        Permanently delete a user (Admin only)

        Args:
            user_id: The user's ID

        Returns:
            tuple: (success, error_message, status_code)
        """
        try:
            user = User.query.get(user_id)

            if not user:
                return False, "User not found", 404

            if user.role == 'admin':
                return False, "Cannot delete admin users", 400

            db.session.delete(user)
            db.session.commit()

            return True, None, 200

        except Exception as e:
            db.session.rollback()
            return False, str(e), 500
