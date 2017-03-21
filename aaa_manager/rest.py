"""
This file contains the AAA manager REST interface. The API allows to manage 
authentication, authorisation and accounting information.
"""
import logging

from aaa_manager import Route
from aaa_manager.authentication import AuthenticationManager, Auth
from pyramid.view import view_config

LOG = logging.getLogger(__name__)


class RestView:
    """
    Implements the main REST API.
    """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']
        self.authentication = AuthenticationManager()

    @view_config(route_name=Route.CHECKIN,
                 request_method='POST',
                 renderer='json')
    def checkin(self):
        """ 
        This method is called from **/engine/api/checkin_data**.
        This method is used to authentication user to access the application.

        Arguments:
            user (str): the username;
            pwd (str): the user password.

        Returns:
            success (bool): True if sucessfully authenticated and False
            otherwise;
            cancelled (bool): True if operation is cancelled by the user and
            False otherwise;
            user_info (dict): contains information about the user, such as
            the authentication token and username;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        usr = self.request.params['user']
        pwd = self.request.params['pwd']
        # TODO: aap_id = 2 is hardcoded
        user = self.authentication.access_app(
                2, 
                usr, 
                self.authentication._hash(pwd), 
                Auth.USERS)
        token = self.authentication.generate_token(user)
        response = self.authentication.insert_token(2, user, token)

        if user is not None:
            LOG.info('Successfully authenticated.')
            return {
                    'success': True, 
                    'cancelled': False, 
                    'user_info': {'user_token': token, 'user': user}, 
                    'error': ''
                    }
        else:
            LOG.info('User not authenticated.')
            return {
                    'success': False, 
                    'cancelled': False, 
                    'user_info': None, 
                    'error': 'Invalid username or password.'
                    }
        return {}

    @view_config(route_name=Route.CHECKOUT,
                 request_method='POST',
                 renderer='json')
    def checkout(self):
        """ 
        This method is called from **/engine/api/checkout_data**.
        This method is used to logout. It revocates current user token and
        logs the operation for accounting purposes. 

        Args:
            token (str): hexadecimal representation of user token.
        """
        token = self.request.params['token']
        self.authentication.remove_token(token)
        return {}

    @view_config(route_name=Route.VERIFY_TOKEN,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def verify_token(self):
        """ 
        This method is called from **/engine/api/verify_token**.
        Verify the validity of user token. 

        Args:
            token (str): hexadecimal representation of user token.

        Returns:
            response (str): username if token is valid and 'invalid token'
            otherwise. 
        """
        token = self.request.params['token']
        response = self.authentication.verify_token(2, token)
        return {'response': response}

    @view_config(route_name=Route.SIGNUP,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def signup(self):
        """ 
        This method is called from **/engine/api/signup**.
        Method used to register new user into the system.

        Args:
            user (str): username;
            pwd (str): user password;
            fname (str): user first name;
            lname (str): user last name;
            email (str): user email address. 
        """

        LOG.info('Awaits filling forms...')

        usr = self.request.params['user']
        pwd = self.request.params['pwd']
        fname = self.request.params['fname']
        lname = self.request.params['lname']
        email = self.request.params['email']

        user_info = {
                'username': usr, 
                'password': pwd, 
                'fname': fname, 
                'lname': lname,
                'email': email
                }
        # app_id = 2 is hardcoded for now.
        # TODO: remove hardcoded data
        result = self.authentication.insert_user(2, user_info)

        if result[0] is not None:
            LOG.info('User successfully registered.')
            return {'success': 'User signed up with success.'}
        else:
            LOG.info('Username already exists.')
            return {'error':\
                    'Username already exists. Please choose a different one.'
            }
        return {}

    
    @view_config(route_name=Route.UPDATE_USER,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def update_user(self):
        """ 
        This method is called from **/engine/api/update_user**.
        Method used to update user information on the system.

        Args:
            user (str): username;
            pwd (str): user password;
            fname (str): user first name;
            lname (str): user last name;
            email (str): user email address. 
        """

        usr = self.request.params['user']
        pwd = self.request.params['pwd']
        fname = self.request.params['fname']
        lname = self.request.params['lname']
        email = self.request.params['email']
            
        LOG.info('#### usr: %s' % usr)
        LOG.info('#### pwd: %s' % pwd)
        LOG.info('#### fname: %s' % fname)
        LOG.info('#### lname: %s' % lname)
        LOG.info('#### email: %s' % email)

        user_info = {
                'username': usr, 
                'password': pwd, 
                'fname': fname, 
                'lname': lname,
                'email': email 
                }
        result = self.authentication.update_user(2, user_info)
        LOG.info('#### result: %s' % result)
        if result > 0:
            msg = 'User information updated successfully.'
            LOG.info(msg)
            return {'success': msg}
        else:
            msg = 'Username does not exist.'
            LOG.info(msg)
            return {'error': msg}



