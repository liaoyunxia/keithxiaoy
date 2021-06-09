# coding=utf-8
import gzip
import json
import mimetypes
import shutil
import sys
from datetime import datetime
from distutils import dir_util, file_util

import requests
from fabric.colors import blue, cyan, green, magenta, red, yellow
from fabric.context_managers import cd, path, prefix, quiet, settings
from fabric.contrib.files import exists
from fabric.decorators import roles, task
from fabric.operations import get, local, put, run, sudo
from fabric.state import env
from fabric.tasks import execute
from fabric.utils import _AttributeDict, puts
from pip._vendor.distlib.compat import raw_input

from jk_p2p_app.constants import *

###########
# manual settings #
###########
"""manual settings """
env.organization = 'backend'
env.domain_name = DOMAIN_NAME
env.email_host = 'pintuang.com'

env.git_host = 'git.qfin-asia.com'
env.proxy = '127.0.0.1:1087'
env.pypi_mirror = ' -i https://pypi.douban.com/simple/'

###########
# GLOBALS #
###########
env.project_name = os.path.basename(os.path.dirname(__file__))

env.project_path = '~/Git/{}'.format(env.project_name)
# others
env.repositories = {
    'django':
        'git@{0.git_host}:{0.organization}/{0.project_name}.git'.format(env)  #
}

cloud = _AttributeDict({'name': '', 'domain_name': '', 'region': ''})
cloud.name = 'aliyun'  # choices: aliyun, aws
cloud.region = 'oss-ap-southeast-5'
if cloud.name == 'aliyun':
    env.user = 'root'
    cloud.domain_name = 'aliyuncs.com'
elif cloud.name == 'aws':
    env.user = 'ubuntu'
    cloud.domain_name = 'amazonaws.com'
else:
    puts('no cloud')
# env.forward_agent = True  #
env.colorize_errors = True
env.output_prefix = False

@task
def testojk(branch='feature/ojk-fix'):
    """【auth测试环境】"""
    env.key_filename = '~/Documents/key/dokuin-app-test.pem'
    # env.key_filename = '~/Documents/key/aliyun_test.pem'  # gitlab
    env.branch = branch
    env.test = True
    env.roledefs = {
        #
        'django': ['147.139.161.20']
    }
    env.roledefs['static'] = [env.roledefs['django'][0]]
    env.STATIC_URL = 'https://{}.{}.{}/'.format(BUCKET_STATIC, cloud.region, cloud.domain_name)
    env.lb_https = False  # 负载均衡是否配置了https


@task
def test(branch='test'):
    """【auth测试环境】"""
    env.key_filename = '~/Documents/key/dokuin-app-test.pem'
    # env.key_filename = '~/Documents/key/aliyun_test.pem'  # gitlab
    env.branch = branch
    env.test = True
    env.roledefs = {
        #
        'django': ['147.139.161.20']
    }
    env.roledefs['static'] = [env.roledefs['django'][0]]
    env.STATIC_URL = 'https://{}.{}.{}/'.format(BUCKET_STATIC, cloud.region, cloud.domain_name)
    env.lb_https = False  # 负载均衡是否配置了https


@task
def prod(branch='master', ip='172.31.177.210'):
    """[prod]"""
    # env.key_filename = '~/Documents/key/yijoy.pem'
    # env.key_filename = '~/Documents/key/kredit-360.pem'.format(env.organization, cloud.name)
    env.key_filename = '/opt/deploy/keys/kredi-360.pem'
    env.branch = branch
    env.test = False
    env.roledefs = {  #
        'django': [ip]
    }
    env.roledefs['static'] = [env.roledefs['django'][0]]
    env.STATIC_URL = 'https://{}.{}.{}/'.format(BUCKET_STATIC, cloud.region, cloud.domain_name)
    env.lb_https = True  #
    env.environment = 'prod'

@task
def prod2(branch='master', ip='172.31.60.234'):
    """[prod2]"""
    # env.key_filename = '~/Documents/key/yijoy.pem'
    # env.key_filename = '~/Documents/key/kredit-360.pem'.format(env.organization, cloud.name)
    env.key_filename = '/opt/deploy/keys/kredi-360.pem'
    env.branch = branch
    env.test = False
    env.roledefs = {  #
        'django': [ip]
    }
    env.roledefs['static'] = [env.roledefs['django'][0]]
    env.STATIC_URL = 'https://{}.{}.{}/'.format(BUCKET_STATIC, cloud.region, cloud.domain_name)
    env.lb_https = True  #
    env.environment = 'prod2'

@task
def prod3(branch='master', ip='172.31.178.35'):
    """[prod2]"""
    # env.key_filename = '~/Documents/key/yijoy.pem'
    # env.key_filename = '~/Documents/key/kredit-360.pem'.format(env.organization, cloud.name)
    env.key_filename = '/opt/deploy/keys/kredi-360.pem'
    env.branch = branch
    env.test = False
    env.roledefs = {  #
        'django': [ip]
    }
    env.roledefs['static'] = [env.roledefs['django'][0]]
    env.STATIC_URL = 'https://{}.{}.{}/'.format(BUCKET_STATIC, cloud.region, cloud.domain_name)
    env.lb_https = True  #
    env.environment = 'prod3'

# =========
# = Hello =
# =========
@task(default=True, alias='other test')
def hello():
    puts('*' * 50)
    puts(cyan('  Fabric usage\n'))
    puts(green(' comnands: fab -l'))
    puts(green('  orders: fab -d order'))
    puts(yellow('  param orders: fab order:param'))
    puts(magenta('  manual settinf env.(organization, .domain_name, .email_host, .git_host, lb_https, roledefs)'))
    puts(blue('  fab prod env: fab prod deploy'))
    puts('  Project Name: {.project_name}'.format(env))  #
    puts('  Repositoreis: {}'.format(env.repositories))  #
    puts('*' * 50)


@task
def show_ssh():
    """show ssh"""
    puts('sudo ssh -i {} {}@{}'.format(env.key_filename, env.user, env.roledefs['django'][0]))


@task
def test_deprecation():
    local_workon('python -Wa manage.py test --settings={}.dev_settings'.format(env.project_name))


@task
def update_project():
    curl('-o .gitignore https://raw.githubusercontent.com/nyssance/Free/master/gitignore/Python.gitignore')
    curl('-O https://raw.githubusercontent.com/nyssance/Free/master/setup.cfg')


@task
@roles('gitlab')
def update_gitlab():  # https://about.gitlab.com/update/#ubuntu
    smartputs('● ├── backend GitLab CE')
    sudo('gitlab-rake gitlab:backup:create STRATEGY=copy')  # default path /var/opt/gitlab/backups
    sudo('apt update')
    smartputs('● ├── upgrade GitLab CE')
    sudo('apt install gitlab-ce')
    apt_upgrade()


@task
@roles('static')
def get_file(path='~/.bashrc'):
    if exists(path):
        get(path, 'downloads/{}'.format(os.path.basename(path)))
    else:
        puts('file ' + yellow(path) + ' not exist')


# =========
# = inilaze =
# =========
@task
@roles('django')
def init_django():
    # apt_upgrade()
    # logtail_install()
    sudo('apt install -y git libmysqlclient-dev python3-pip')
    sudo('apt install -y language-pack-zh-hans')  # aliyun ubuntu, python
    sudo('apt install -y language-pack-id')
    # sudo('apt install -y libjpeg-dev libfreetype6-dev libgif-dev tree')  # freetype6 png, tree
    sudo('pip3 install -U virtualenvwrapper{}'.format(env.pypi_mirror))
    sudo('pip3 install https://codeload.github.com/Supervisor/supervisor/zip/master')
    put('configs/{}.bashrc'.format(cloud.name), '~/.bashrc')
    init_code()
    run('mkvirtualenv {}'.format(env.project_name))  #
    with cd(env.project_path), prefix('workon {}'.format(env.project_name)):
        run('pip install -U -r requirements.txt{}'.format(env.pypi_mirror))
    init_nginx()


@task
@roles('django')
def init_code():
    """init_code"""
    safe_mkmir('~/.ssh')
    put('configs/id_rsa', '~/.ssh/id_rsa')
    put('configs/id_rsa.pub', '~/.ssh/id_rsa.pub')
    run('chmod 400 ~/.ssh/id_rsa')
    run('chmod 400 ~/.ssh/id_rsa.pub')
    if exists(env.project_path):
        smartputs('● ├── delete exist databases')
        run('rm -rf {}'.format(env.project_path))
    smartputs('● ├── create new db')
    run('git clone {0.repositories[django]} {0.project_path}'.format(env))
    smartputs('● ├── switch to {} branch'.format(env.branch))
    smartrun('git checkout {}'.format(env.branch))


@task
@roles('django')
def init_nginx():
    """init_nginx"""
    if env.lb_https:
        run('apt install -y nginx')
        with cd(env.project_path):
            put('configs/nginx.conf', '/etc/nginx/sites-enabled/{}.conf'.format(env.domain_name))
        run('sudo systemctl start nginx')
    if not env.lb_https:
        run('apt install -y nginx')
        with cd(env.project_path):
            put('configs/nginx_test.conf', '/etc/nginx/sites-enabled/{}.conf'.format(env.domain_name))
        run('sudo systemctl start nginx')


# ==========
# = Deploy =
# ==========
def apt_upgrade():
    smartputs('● ├── apt upgrade / install')
    sudo('apt update')
    sudo('apt upgrade -y')
    sudo('apt clean')


def logtail_install():
    # https://www.alibabacloud.com/help/zh/doc-detail/48932.htm
    smartputs('● ├── logtail install')
    if cloud.region == 'oss-cn-shanghai':
        run(
            'wget https://logtail-release-sh.vpc100-oss-cn-shanghai.aliyuncs.com/linux64/logtail.sh -O logtail.sh; chmod 755 logtail.sh; sh logtail.sh install cn-shanghai_vpc'
        )
    else:
        smartputs('logtail uninstall, please fix all region install  ')
    run('/etc/init.d/ilogtaild status')

    sudo('/etc/init.d/ilogtaild stop')
    sudo('/etc/init.d/ilogtaild stop')

    sudo('/etc/init.d/rsyslog restart')
    # run('tail -f /var/log/syslog')


@task
def deploy(mode=1, groups='all'):
    """deploy, model=0(open DEBUG), 1(default), 2(upgrade pip), 3(deploy static files), 4(upgrade server)"""
    env.groups = groups.split('/')
    print(groups)
    with settings(
        # hide('stdout'),
        warn_only=False
    ):
        if int(mode) > 2:
            local_deploy_static('img', 'vendor', 'images')
        execute(deploy_django, mode)  #


@roles('django')
# @parallel(pool_size=5)  # Windows has some problem
def deploy_django(mode=1):
    smartputs('🍺  start deploy')
    if int(mode) > 3:
        apt_upgrade()
        sudo('python3 -m pip install -U pip virtualenvwrapper{}'.format(env.pypi_mirror))
        sudo('python3 -m pip install -U https://codeload.github.com/Supervisor/supervisor/zip/master')
    constants = '{0.project_path}/{0.project_name}/constants.py'.format(env)
    settings = '{0.project_path}/{0.project_name}/settings.py'.format(env)
    run('sed -i "s/ENV = STAGE.TEST/ENV = STAGE.PROD/g" {}'.format(constants))  # reseting
    run('sed -i "s/DEBUG = True/DEBUG = False/g" {}'.format(settings))
    smartrun('git fetch --prune')
    smartputs('● ├── switch to {} branch'.format(env.branch))
    smartrun('git checkout {}'.format(env.branch))
    smartrun('git pull')
    smartrun('git clean -dfn')  # clean dir
    if env.test:
        run('sed -i "s/ENV = STAGE.PROD/ENV = STAGE.TEST/g" {}'.format(constants))
    if int(mode) < 1:
        run('sed -i "s/DEBUG = False/DEBUG = True/g" {}'.format(settings))
    with cd(env.project_path), prefix('workon {}'.format(env.project_name)):
        if int(mode) > 1:
            run('python3 -m pip install -U -r requirements.txt{}'.format(env.pypi_mirror))
            # Pillow reindtall
            run('python3 -m pip install -U Pillow --no-cache-dir{}'.format(env.pypi_mirror))
        run('python manage.py compilemessages')
        if env.test:
            run('python manage.py makemigrations')
            run('python manage.py migrate')
            smartputs('● ├── bacend migrations')
            with quiet():
                run('find . -name  migrations |xargs tar -cvf migrations.tgz')
            run('mv migrations.tgz ~/')
        else:
            puts(yellow('prod env migrations...'))

    if exists('/tmp/supervisor.sock'):
        supervisor_update()

        # fab test deploy:groups=all
        # all programs
        if 'all' in env.groups:
            smartputs('|--> Restart all services...')
            supervisor_restart('all')

        # django group
        if 'django' in env.groups:
            smartputs('|--> Restart django services...')
            supervisor_restart('gunicorn')

        # celery group
        if 'celery' in env.groups:
            smartputs('|--> Restart celery services...')
            supervisor_restart('celery_default')
            supervisor_restart('celery_beat')
            supervisor_restart('celery_message')
            supervisor_restart('celery_sync')
            # supervisor_restart('flower')

        # nameko group
        if 'nameko' in env.groups:
            smartputs('|--> Restart nameko services...')
            supervisor_restart('gunicorn')

    else:
        supervisor_conf()

    smartputs('🍻  finish deploy ({})'.format(datetime.now().strftime('%H:%m')))


@task
@roles('django')
def restart_gunicorn():
    smartputs('🍺  restart gunicorn')
    if exists('/tmp/supervisor.sock'):
        supervisor_update()
        supervisor_restart('gunicorn')
    else:
        supervisor_conf()
    smartputs('🍻  finish restart gunicorn')

@task
@roles('django')
def gunicorn_check():  # 检查项目状态
    supervisor_check()

@task
@roles('django')
def Offline():  # SLB下线节点(删除nginx-status文件)
    smartputs('🍺  offline this node')
    run('rm -f /etc/nginx/status || exit 1')
    smartputs('|--> Wait APP offline in 6 seconds...')
    run('sleep 6')

@task
@roles('django')
def Online():  # SLB上线节点(删除nginx-status文件)
    smartputs('🍺  online this node')
    run('touch -m /etc/nginx/status || exit 1')
    smartputs('|--> Wait APP online in 6 seconds...')
    run('sleep 6')

#########
# Backup#
#########
# ===========
# = 备份回滚 =
# ===========

@task
@roles('django')
def backup_django():
    smartputs('🍺  开始备份')
    run('rsync -az --exclude celery_log --exclude nameko_log --exclude log  ~/Git /opt/deploy/backup/$(date +%Y%m%d-%H%M%S)')  # 直接拷贝完整项目
    with cd('/opt/deploy/backup/'):
        run(''' ls -lt| awk '{if(NR>5){print "rm -rf " $9}}'|sh ''')  #只保留五个备份
        run(''' echo "项目保存在目录$(ls -lt| grep -v total | head -n 1 | awk '{print $9}')" ''')  # 只保留五个备份
    smartputs('🍻  完成备份')

@roles('django')
# @parallel(pool_size=5)  # Windows has some problem
def rollback_django(mode=1):
    smartputs('🍺  start deploy')
    if int(mode) > 3:
        apt_upgrade()
        sudo('python3 -m pip install -U pip virtualenvwrapper{}'.format(env.pypi_mirror))
        sudo('python3 -m pip install -U https://codeload.github.com/Supervisor/supervisor/zip/master')
    constants = '{0.project_path}/{0.project_name}/constants.py'.format(env)
    settings = '{0.project_path}/{0.project_name}/settings.py'.format(env)
    run('sed -i "s/ENV = STAGE.TEST/ENV = STAGE.PROD/g" {}'.format(constants))  # reseting
    run('sed -i "s/DEBUG = True/DEBUG = False/g" {}'.format(settings))
    smartrun('git fetch --prune')
    smartputs('● ├── switch to {} branch'.format(env.branch))
    smartrun('git checkout {}'.format(env.branch))
    smartrun('git pull')
    smartrun('git clean -dfn')  # clean dir
    if env.test:
        run('sed -i "s/ENV = STAGE.PROD/ENV = STAGE.TEST/g" {}'.format(constants))
    if int(mode) < 1:
        run('sed -i "s/DEBUG = False/DEBUG = True/g" {}'.format(settings))
    with cd(env.project_path), prefix('workon {}'.format(env.project_name)):
        if int(mode) > 1:
            run('python3 -m pip install -U -r requirements.txt{}'.format(env.pypi_mirror))
            # Pillow reindtall
            run('python3 -m pip install -U Pillow --no-cache-dir{}'.format(env.pypi_mirror))
        run('python manage.py compilemessages')
        if env.test:
            run('python manage.py makemigrations')
            run('python manage.py migrate')
            smartputs('● ├── bacend migrations')
            with quiet():
                run('find . -name  migrations |xargs tar -cvf migrations.tgz')
            run('mv migrations.tgz ~/')
        else:
            puts(yellow('prod env migrations...'))

    if exists('/tmp/supervisor.sock'):
        supervisor_update()
        supervisor_restart('all')
    else:
        supervisor_conf()

    smartputs('🍻  finish deploy ({})'.format(datetime.now().strftime('%H:%m')))

#########
# Local #
#########
@task
def local_init_mysql():
    auth = '-uroot -p123456'
    local('mysqldump {} {}_default -d > default.sql'.format(auth, env.project_name))
    for i in range(4):
        local(
            'mysql {} -e "CREATE SCHEMA IF NOT EXISTS \`{}_{}\` DEFAULT CHARACTER SET utf8mb4 ;"'.format(
                auth, env.project_name, i
            )
        )
        local('mysql {} {}_{} < migrate/shard.sql'.format(auth, env.project_name, i))


@task
def local_createsuperuser(username='admin'):
    local_workon(
        'python manage.py createsuperuser --username {0} --email {0}@{1} --settings={2}.dev_settings'.format(
            username, env.email_host, env.project_name
        )
    )


@task
def local_startapp(appname):
    local_workon('python manage.py startapp {0} --settings={1}.dev_settings'.format(appname, env.project_name))


@task
def local_shell():
    local_workon('python manage.py shell  --settings={0}.dev_settings'.format(env.project_name))


@task
def local_install(pypi_mirror=env.pypi_mirror):
    local('sudo -H python3 -m pip install -U pip{}'.format(pypi_mirror))
    local('sudo -H python3 -m pip install -U Fabric3 requests{}'.format(pypi_mirror))
    local('sudo -H python3 -m pip install -U virtualenvwrapper{}'.format(pypi_mirror))

    if not os.path.exists(os.path.expanduser('~/Envs/{}'.format(env.project_name))):
        with settings(warn_only=True):
            local('export WORKON_HOME=~/Envs && mkdir -p $WORKON_HOME')
            local('export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 && source /usr/local/bin/virtualenvwrapper.sh')
            local('/bin/bash -lc "mkvirtualenv {}"'.format(env.project_name))
    local_workon('sudo -H python3 -m pip install -U -r requirements/dev.txt{}'.format(pypi_mirror))
    puts(green('finish upgrade package, use empty param local_install: xxx'))
    puts(green('create databases'))
    if not os.path.exists('/tmp/mysql.sock'):
        local('brew services start mysql')
    auth = '-uroot -p123456'
    local(
        'mysql {} -e "CREATE SCHEMA IF NOT EXISTS \`{}_default\` DEFAULT CHARACTER SET utf8mb4 ;"'.format(
            auth, env.project_name
        )
    )
    local_compilemessages()


@task
def local_install_railguns_develop(pypi_mirror=env.pypi_mirror):
    local(
        'sudo -H python3 -m pip install -U https://codeload.github.com/nyssance/railguns/zip/develop{}'.
        format(pypi_mirror)
    )


@task
def local_reinstall(pypi_mirror=env.pypi_mirror):
    local('/bin/bash -lc "rmvirtualenv {}"'.format(env.project_name))
    local('sudo rm -rf ~/Envs/{}/'.format(env.project_name))  # python's shutil.rmtree and os.chmod
    # local('sudo rm Pipfile Pipfile.lock')
    local_install(pypi_mirror)


@task
def local_create_schema():
    auth = '-uroot -p123456'
    local('mysql {} -e "DROP SCHEMA IF EXISTS \`{}_default\` ;"'.format(auth, env.project_name))
    local('mysql {} -e "CREATE SCHEMA \`{}_default\` DEFAULT CHARACTER SET utf8mb4 ;"'.format(auth, env.project_name))
    local_makemigrations()
    local_migrate()
    local_createsuperuser()


# ===========
# = defaut =
# ===========
@task
def local_runserver(port='8000', migrate='yes', ssl=''):
    """choices param <port><is migrate> example: local_runserver:8001, waring ''"""
    # branch = local('git status', True).split('\n')[0].replace('On branch ', '')
    # if branch in ['develop', 'master']:
    #     puts('don't change {} branch code '.format(yellow(branch)))
    #     return
    if not os.path.exists('/tmp/mysql.sock'):
        # local('mysql.server start')
        local('brew services start mysql')
        local('brew services start redis')
    local('brew services list')
    if migrate and port != 'go':
        local_makemigrations()
        local_migrate()
    if port == 'go':
        local_workon('python manage.py runserver --settings={}.dev_settings'.format(env.project_name))
    if port == 'warning':
        local_workon('python -Wd manage.py run{}server 0:8000 --settings={}.dev_settings'.format(ssl, env.project_name))
    else:
        local_workon('python manage.py run{}server 0:{} --settings={}.dev_settings'.format(ssl, port, env.project_name))


@task
def local_stopserver():
    """stop all services"""
    local('brew services stop --all')


@task
def local_makemessages(location='file'):
    ignores = ['*/accounts/*.html', 'change_list_generate.html', 'verify_phone_number.html']

    with path('/usr/local/opt/gettext/bin'):
        local_workon(
            'python manage.py makemessages -l en -i={} --no-wrap --add-location {} --settings={}.dev_settings'.format(
                ' -i='.join(ignores), location, env.project_name
            )
        )
        local_workon(
            'python manage.py makemessages -l zh_Hans -i={} --no-wrap --add-location {} --settings={}.dev_settings'.
            format(' -i='.join(ignores), location, env.project_name)
        )
        local_workon(
            'python manage.py makemessages -l id -i={} --no-wrap --add-location {} --settings={}.dev_settings'.format(
                ' -i='.join(ignores), location, env.project_name
            )
        )
        # local_workon('python manage.py makemessages -d djangojs --no-wrap')
    puts(green('finish,  localhost:8000/rosetta/ transfer to english then transifex_sync'))


@task
def local_compilemessages():
    """compilemessages"""
    puts(green('compilemessages'))
    with path('/usr/local/opt/gettext/bin'):
        local_workon('python manage.py compilemessages --settings={}.dev_settings'.format(env.project_name))


@task
def local_makemigrations(app=''):
    local_workon('python manage.py makemigrations --settings={}.dev_settings {}'.format(env.project_name, app))


@task
def local_migrate():
    local_workon('python manage.py migrate --settings={}.dev_settings'.format(env.project_name))


@task
def local_sendtestemail(email):
    local_workon('python manage.py sendtestemail {}'.format(email))


# ===========
# = deploy staticfile =
# ===========
@task
def local_collectstatic(*args):
    """collectstatic"""
    exclude = [
        'img', 'vendor', 'cloudfile',
        'admin', 'django_extensions', 'drf-yasg', 'import_export', 'rest_framework', 's3direct',
        'suit', 'ckeditor'
    ]  # yapf: disable
    # exclude += ['railguns']

    ignores = ['debug_toolbar', 'favicon'] + ([] if args == ('all', ) else [x for x in exclude if x not in args])
    local_workon(
        'python manage.py collectstatic --no-input -i {} --settings={}.dev_settings'.format(
            ' -i '.join(ignores), env.project_name
        )
    )
    icons_dir = '{}/static/favicon/{}'.format(env.project_name, 'test' if env.test else 'prod')
    for icon in os.listdir(icons_dir):
        copy(os.path.join(icons_dir, icon), 'static/{}'.format(icon))


@task
def local_deploy_static(*args):
    """choices params all(all) :img,vendor(img, vendor), """
    local_collectstatic(*args)
    top = 'static/'
    tmp = 'tmp/'
    tmp_static = os.path.join(tmp, 'static')
    for dirpath, dirnames, filenames in os.walk(top):
        for filename in filenames:
            if filename.startswith('.'):
                continue
            path = os.path.join(dirpath, filename)
            content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            # process css and js
            if not path.startswith('vendor/') and content_type in ['text/css', 'application/javascript']:
                css_in = open(path, 'r')
                try:
                    old = css_in.read()
                    # new = old.replace('url(/static/', 'url({}'.format(env.STATIC_URL))
                    new = old.replace('/static/', env.STATIC_URL)
                    if old != new:
                        css_out = open(path, 'w')
                        css_out.write(new)
                        css_out.close()
                finally:
                    css_in.close()
            out_path = path
            is_gzip = content_type.startswith('text/') or content_type in ['application/javascript', 'application/json']
            dest_name = path[len(top):]  # include path
            if is_gzip:
                out_path = os.path.join(tmp_static, dest_name)
                safe_local_makedirs(os.path.dirname(out_path))
                f_in = open(path, 'rb')
                f_out = open(out_path, 'wb')
                try:
                    f_out = gzip.GzipFile(fileobj=f_out)
                    f_out.write(f_in.read())
                finally:
                    f_out.close()
                    f_in.close()
            params_url = 'http://localhost:8000/upload_params/{}/?filename={}&bucket={}'.format(
                cloud.name, dest_name, BUCKET_STATIC
            )
            if is_gzip:
                params_url = '{}&content_encoding=gzip'.format(params_url)
            if path.startswith('static/vendor'):
                pass
                # params_url = '{}&cache_control=public,max-age=864000'.format(params_url)
            data = requests.get(params_url).text
            response = requests.post(env.STATIC_URL, files={'file': open(out_path, 'rb')}, data=json.loads(data))
            if 200 < response.status_code < 300:
                puts(green(dest_name))
            else:
                puts(red('{}----{}'.format(response.status_code, response.text)))
    safe_local_delete(top)
    safe_local_delete(tmp)


# ===========
# = tool func =
# ===========
@task
def local_cleanmigrations():
    local('for dir in `find . -type d -name migrations`;do find $dir -type f |grep -v "__init__.py" ;done |xargs rm -f')


@task
def local_diffsettings():
    local_workon('python manage.py diffsettings --output=unified')


@task
def local_clearpyc():
    local_workon('python manage.py clean_pyc --settings={}.dev_settings'.format(env.project_name))


@task
def local_format():
    """format code """
    ignore = ['.git', 'node_modules', '**/migrations']
    local('isort -rc . -s {}'.format(' -s '.join(ignore)))
    local('yapf -irp . -e {}'.format(' -e '.join(ignore)))


@task
def gulp():
    local('npm link browser-sync gulp')
    local('gulp')


@task
def update_railguns(action='push'):
    """udpate railguns"""
    railguns = '/Users/NY/Projects/eclipse-workspace/railguns/railguns'
    dict = {
        'railguns/cloudfile': 'cloudfile',
        'railguns/django': 'django',
        'railguns/rest_framework': 'rest_framework',
        'railguns/tools': 'tools',
        'railguns/urls.py': 'urls.py',
        os.path.join(env.project_name, 'static/vendor'): 'static/vendor',
        os.path.join(env.project_name, 'static/railguns'): 'static/railguns',
        os.path.join(env.project_name, 'templates/railguns'): 'templates/railguns'
    }
    for key, value in dict.items():
        local = key
        remote = os.path.join(railguns, value)
        if action == 'push':
            copy(local, remote)
        else:
            copy(remote, local)


@task
def local_update_vendor():
    """update_vendor"""
    filenames = [
        'axios.js', 'axios.min.js', 'vue.js', 'vue.min.js', 'material-components-web.min.css',
        'material-components-web.min.js'
    ]
    for filename in filenames:
        curl(
            'https://unpkg.com/{0}@latest/dist/{1} > {2}/static/vendor/{1}'.format(
                filename.split('.')[0], filename, env.project_name
            )
        )


def local_workon(command):
    local('/bin/bash -lc "workon {} && {}"'.format(env.project_name, command))


# =======
# = git =
# =======
@task
def commit_and_sync(comment=None):
    """git commit and sync"""
    output_list = local('git status', True).split('\n')
    branch = output_list[0].replace('On branch ', '')
    if branch in ['develop', 'master']:
        puts(
            'not permit change {} branch, please use {} command to operate'.format(yellow(branch), get_function_name())
        )
    elif 'nothing to commit' in output_list[-1]:
        puts('there is no change in {} branch, you do not need to submit'.format(yellow(branch)))
        if 'is ahead of' in output_list[1]:
            puts('upgrade {} branch'.format(yellow(branch)))
            local('git push')
    else:
        local('git reset')
        delete_files = [x.strip() for x in output_list if x.find('deleted:') != -1]
        for file in delete_files:
            filename = file.split(':')[1].strip()
            local('git rm {}'.format(filename))
        local('git add .')
        if not comment:
            comment = raw_input('please input description: ')
        local('git status')
        local('git commit -m "{}"'.format(comment))
        local('git push')


@task
def update_from_develop():
    """update_from_develop"""
    output_list = local('git status', True).split('\n')
    branch = output_list[0].replace('On branch ', '')
    if branch in ['develop', 'master']:
        puts(
            'not permit change {} branch, please use {} command to operate'.format(yellow(branch), get_function_name())
        )
    elif 'nothing to commit' in output_list[-1]:
        local('git pull origin develop')
        local('git clean -dfn')
        local_compilemessages()
    else:
        local('git status')
        puts(
            'there is some change unsubmit in current {} branch, please do fab commit_and_sync to submit'.format(
                yellow(branch)
            )
        )


@task
def update_to_develop():
    """ update_to_develop """
    output_list = local('git status', True).split('\n')
    branch = output_list[0].replace('On branch ', '')
    if branch in ['develop', 'master']:
        puts(
            'not permit change {} branch, please use {} command to operate'.format(yellow(branch), get_function_name())
        )
    elif 'nothing to commit' in output_list[-1]:
        confirm = raw_input('is ready update_from_develop? [y/N]: '.format(yellow(branch)))
        if confirm.lower() in ['ok', 'y', 'yes']:
            puts('merge {} to develop'.format(yellow(branch)))
            local('git checkout -f develop')
            local('git pull')
            local('git clean -dfn')
            local('git merge {}'.format(branch))
            local('git push')
            local('git checkout {}'.format(branch))
    else:
        local('git status')
        puts(
            'there is some change unsubmit in current {} branch, please do fab commit_and_sync to submit'.format(
                yellow(branch)
            )
        )


# =============
# = Transifex =
# =============
@task
def transifex_sync():
    """upgrade to Transifex"""
    local('tx push -s')  # https://docs.transifex.com/client/push
    local('tx pull -a')  # https://docs.transifex.com/client/pull
    local_compilemessages()


# ==================
# = Configurations =
# ==================
# Supervisor
# --------------------------------------------------------------------------------
def supervisor_conf():
    if env.test:
        run('supervisord -c {}/etc/test/supervisord.conf'.format(env.project_path))
    else:
        run('supervisord -c {}/etc/{}/supervisord.conf'.format(env.project_path, env.environment)) # 配置好gunicorn的directory之后任意目录运行都行


def supervisor_unlink():  # stop supervisord
    run('unlink /tmp/supervisor.sock')


@task
@roles('django')
def supervisor_start(process='all'):  #
    with cd(env.project_path + '/etc/{}'.format('test' if env.test else env.environment)):
        smartrun('supervisorctl start {}'.format(process))


@task
@roles('django')
def supervisor_restart(process='all'):
    with cd(env.project_path + '/etc/{}'.format('test' if env.test else env.environment)):
        run('supervisorctl -u kartu -p Kartu@2018 restart {}'.format(process))


@task
@roles('django')
def supervisor_stop(process='all'):
    with cd(env.project_path + '/etc/{}'.format('test' if env.test else env.environment)):
        smartrun('supervisorctl -u kartu -p Kartu@2018 stop {}'.format(process))


@task
@roles('django')
def supervisor_reload():
    with cd(env.project_path + '/etc/{}'.format('test' if env.test else env.environment)):
        smartrun('supervisorctl -u kartu -p Kartu@2018 reload')


def supervisor_update():  #
    with cd(env.project_path + '/etc/{}'.format('test' if env.test else env.environment)):
        smartrun('supervisorctl -u kartu -p Kartu@2018 update')

@task
@roles('django')
def supervisor_check():  # 检查项目状态
    with cd(env.project_path + '/etc/{}'.format('test' if env.test else env.environment)):
        run('''[[ `/usr/local/bin/supervisorctl status | grep gunicorn | awk '{print $2}'` -eq "RUNNING" ]] && exit 0 || exit 1''')


# ===========
# = tool func =
# ===========
def curl(command=''):
    local('curl -fsSL{} {}'.format(' -x {}'.format(env.proxy) if env.proxy else '', command))


def copy(src, dst):
    # SO: https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
    if os.path.isdir(src):
        dir_util.copy_tree(src, dst)
    else:
        file_util.copy_file(src, dst)


def safe_mkmir(path):
    if not exists(path):
        run('mkdir {}'.format(path))


def safe_local_makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def safe_local_delete(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def smartrun(command):
    with cd(env.project_path):
        run(command)


def smartputs(prefix):
    if env.host_string in env.roledefs['django']:
        sputs(prefix, ('[Django web server][{}]'.format(env.host_string)))
    elif env.host_string in env.roledefs['gitlab']:
        sputs(prefix, magenta('[GitLab web server] [{}]'.format(env.host_string)))
    else:
        sputs(prefix, yellow('🌵 [unknown server type ] [{}]'.format(env.host_string)))


def sputs(prefix, text):
    puts(cyan(prefix) + ('[test]' if env.test else '') + cyan('env') + text + cyan(' --'), show_prefix=False)


def get_function_name():
    return sys._getframe(1).f_code.co_name
