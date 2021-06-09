
# ===========
# = Base Image
# ===========
#
FROM registry.ap-southeast-5.aliyuncs.com/360shuke/ubuntu-18.04-base:1.0

# ===========
# = Build Paraments
# ===========
# PROJECT_ENV    : DEV / TEST / PROD
# PROJECT_DEBUG  : False / Ture
#
ARG PROJECT_NAME
ARG PROJECT_ENV
ARG PROJECT_DEBUG

# ===========
# = Author
# ===========
#
MAINTAINER 360jinrong.net

# ===========
# = Environment
# ===========
# PROJECT_ENV    : DEV / TEST / PROD
# PROJECT_DEBUG  : False / Ture
#
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

# ===========
# = Initiate Project
# ===========
#
RUN mkdir -p /root/Git/${PROJECT_NAME}

ADD . /root/Git/${PROJECT_NAME}/

WORKDIR /root/Git/${PROJECT_NAME}

# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

RUN apt install net-tools \
	&& export WORKON_HOME=/root/Envs \
        && export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 \
        && source /usr/local/bin/virtualenvwrapper.sh \
        && source /root/.bashrc \
        && mkvirtualenv ${PROJECT_NAME} \
        && workon ${PROJECT_NAME} \
        && pip install setuptools-scm -i https://mirrors.aliyun.com/pypi/simple \
        && pip install -U -r ~/Git/${PROJECT_NAME}/requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
        && pip install -U Pillow --no-cache-dir  -i https://mirrors.aliyun.com/pypi/simple \
        && pip uninstall -y django \
        && pip install django==2.2.4 django-simpleui django-debug-toolbar django-haystack django-haystack-panel django-cors-headers django-rosetta   \
        whoosh jieba django-crispy-forms django_extensions django_redis celery celery_once stringcase rocketmq mysqlclient \
        mq-http-sdk==1.0.1 nameko==2.12.0 django-nameko==0.7.3 pandas scikit-learn paramiko django-ckeditor django_filter \
        pymysql -i https://mirrors.aliyun.com/pypi/simple \
        && sed -i "s/ENV = STAGE.TEST/ENV = STAGE.$PROJECT_ENV/g" ${PROJECT_NAME}/constants.py \
        && sed -i "s/DEBUG = True/DEBUG = $PROJECT_DEBUG/g" ${PROJECT_NAME}/constants.py \
        && mkdir log && mkdir celery_log && mkdir nameko_log \
	&& python manage.py compilemessages


# ===========
# = Run Project
# ===========
#
EXPOSE 22 8000

ENTRYPOINT ["/tini", "--", "/root/Git/jk_p2p_app/dockerRun.sh"]

# ===========
# = Commands
# ===========
#
#docker build -f Dockerfile --build-arg PROJECT_NAME=jk_p2p_app --build-arg PROJECT_ENV=TEST --build-arg PROJECT_DEBUG=False   -t jk_p2p_app:1.0 .
#docker run -d --name=$PROJECT_NAME  --privileged -p 8000:8000 -v /mnt/Git/jk_p2p_app/log:/root/Git/jk_p2p_app/log jk_p2p_app:1.0

