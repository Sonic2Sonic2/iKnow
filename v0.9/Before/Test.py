import argparse
import httplib2
from apiclient.discovery import build
from oauth2client import GOOGLE_TOKEN_URI
from oauth2client.client import OAuth2Credentials


def create_credentials(client_id, client_secret, refresh_token):
  """Create Google OAuth2 credentials.

  Args:
    client_id: Client id of a Google Cloud console project.
    client_secret: Client secret of a Google Cloud console project.
    refresh_token: A refresh token authorizing the Google Cloud console project
      to access the DS data of some Google user.

  Returns:
    OAuth2Credentials
  """
  return OAuth2Credentials(access_token=None,
                           client_id=client_id,
                           client_secret=client_secret,
                           refresh_token=refresh_token,
                           token_expiry=None,
                           token_uri=GOOGLE_TOKEN_URI,
                           user_agent=None)


def get_service(credentials):
  """Set up a new DoubleClick Search service.

  Args:
    credentials: An OAuth2Credentials generated with create_credentials, or
    flows in the oatuh2client.client package.
  Returns:
    An authorized Doubleclicksearch serivce.
  """
  # Use the authorize() function of OAuth2Credentials to apply necessary credential
  # headers to all requests.
  http = credentials.authorize(http = httplib2.Http())

  # Construct the service object for the interacting with the DoubleClick Search API.
  service = build('doubleclicksearch', 'v2', http=http)
  return service


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Sample DS API code.')
  parser.add_argument('--client_id', dest='c_id', action='store',
                      help=('Specifies the DS API client_id. Looks like: '
                            '1234567890.apps.googleusercontent.com'))
  parser.add_argument('--client_secret', dest='secret', action='store',
                      help=('Specifies the DS API client_secret. Looks like: '
                            '1ab2CDEfghigKlM3OPzyx2Q'))
  parser.add_argument('--refresh_token', dest='token', action='store',
                      help=('Specifies the DS API refresh_token. Looks like: '
                            '4/abC1ddW3WJURhF7DUj-6FHq8kkE'))
  args = parser.parse_args()

  creds = create_credentials(args.c_id, args.secret, args.token)
  service = get_service(creds)
