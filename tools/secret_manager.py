import configparser
from cryptography.fernet import Fernet
import os


class SecretManager():
    """Class for managing passwords to teleserver
    """
    def __init__(self, secret_file='/usr/local/teleserver/secret.ini'):
        """Init method for SecretManager class

        :param secret_file: Absolut path to file where to store secrets
        :type: str
        """
        self.secret_file = secret_file

    def get_credentials(self):
        """Get list of credentials

        :return: List of credentials
                 Where [0] is user and [1] is password
        :type: list
        """
        if os.path.isfile(self.secret_file):
            config = configparser.ConfigParser()
            config.read(self.secret_file)
            key = config['KEY']['key']
            user_crypt = config['PASS']['user']
            pass_crypt = config['PASS']['pass']
            return [self.decrypt(key, user_crypt), self.decrypt(key, pass_crypt)]
        else:
            return ['', '']

    @staticmethod
    def decrypt(key, var):
        """Decrypt variable with a key

        :param key: key to decrypt
        :type: str
        :param var: variable to decrypt
        :type: str

        :return: decrypted variable
        :type: str
        """
        f = Fernet(key)
        return f.decrypt(bytes(var, 'utf-8')).decode('utf-8')

    def encrypt_credentials(self, user, password):
        """Encrypt credentials

        :param user: Username
        :type: str
        :param password: Password
        :type: str

        :return: Encrypted user and password with key
                 - encrypted user
                 - encrypted password
                 - key to decrypt user and password
        :type: str
        """
        key = Fernet.generate_key()
        user_crypt = self.encrypt(key, user)
        pass_crypt = self.encrypt(key, password)
        return user_crypt, pass_crypt, key.decode('utf-8')

    @staticmethod
    def encrypt(key, var):
        """Encrypt variable with key

        :param key: Key to use to encrypt
        :type: str
        :param var: Variable to encrypt
        :type: str

        :return: Encrypted variable
        :type: str
        """
        f = Fernet(key)
        return f.encrypt(bytes(var, 'utf-8')).decode('utf-8')

    def set_credentials(self, user, password, file_loc='/usr/local/teleserver/secret.ini'):
        """Set user, password credentials in file

        :param user: username
        :type: str
        :param password: password
        :type: str
        :param file_loc: Location of secret file
        :type: str
        """
        user_crypt, pass_crypt, key = self.encrypt_credentials(user, password)
        config = configparser.ConfigParser()
        config['PASS'] = {'user': user_crypt,
                          'pass': pass_crypt}
        config['KEY'] = {'key': key}
        with open(file_loc, 'w') as dest_file:
            config.write(dest_file)
