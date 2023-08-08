from sanic import Sanic, response
import aiofiles
import logging
logging.basicConfig(level=logging.INFO)
from sanic_httpauth import HTTPBasicAuth
import hashlib
import json
from werkzeug.utils import secure_filename


app = Sanic(__name__)
auth = HTTPBasicAuth()

app.config.FALLBACK_ERROR_FORMAT = "json"
#app.static('/files/', '/files/', directory_view=True)

f = open('config.json')
config = json.load(f)
username = config['username']
password = config['password']


async def write_file(path, body):
    async with aiofiles.open(path, 'wb') as f:
        await f.write(body)


def valid_file_size(file_body):
    if len(file_body) < 10485760:
        return True
    return False


def hash_password(salt, password):
    salted = password + salt
    return hashlib.sha512(salted.encode("utf8")).hexdigest()


app_salt = "s9VheSW6GqrQ2NmF4AszmrS2nCWVPZ87g5doglem"
users = {
    username: hash_password(app_salt, password),
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return users.get(username) == hash_password(app_salt, password)
    return False


@app.post('/')
@auth.login_required
async def upload_file(request):
    upload_file = request.files.get('file')

    if upload_file is not None:
        filename = secure_filename(upload_file.name)
        file_path = '/files/' + filename
        if valid_file_size(upload_file.body):
            await write_file(file_path, upload_file.body)

    return response.json(True)
