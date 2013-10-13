import logging

logger = logging.getLogger(__name__)


def __virtual__():
    return 'docker'


def image_managed(name):
    ret = {'name': name,
           'result': True,
           'changes': {},
           'comment': ''}


    if __opts__['test']:
        images = __salt__['docker.images']
        if name not in [i.Repositories for i in images]:
            ## TODO search registry for package and print result
            ret['changes'] = {
                'pulled {}'.format(name): {
                    'old': '',
                    'new': '',
                }
            }
            ret['comment'] = 'Pulling image from registry'
        return ret
