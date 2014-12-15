### What is Nodjango?

Simply adds WebSockets functionality to Django applications by proxying Django behind a Nodejs/SocketIO server.

TODO: Add a SocketIoCallbacksFinder that searchs each app in `INSTALLED_APPS` and adds Socket.io callback namespaces defined in `app_name/socketio` folders.

### Usage

```
    python manage.py runserverjs <hostname> <public port> <proxy port> <socket port>
```

In any Django template that you want a Socket IO connection, add this templatetag to your HEAD:

```
{% load nodjango %}
<!doctype html>
<html>
<head>
    <script type="text/javascript" src="//code.jquery.com/jquery-2.1.1.min.js"></script>
    {% nodjango_head_scripts %}
</head>
<body>
    <button>Click Me</button>
    <script type="text/javascript">
        nodjango.on('orm_callback', function(data){
            alert(JSON.stringify(data));
        });

        $('button').on('click', function(){
            nodjango.emit('orm', {
                'callback': 'orm_callback',
                'app': 'core',
                'model': 'User',
                'kwargs': {
                    'id': 1
                }
            });
        });
    </script>
</body>
</html>
```

### Installation

```
    pip install nodjango
```

### Under the hood

*   [virtual-node](https://github.com/elbaschid/virtual-node) for installing [node.js](http://nodejs.org/) in a Python virtualenv.
*   [Django](https://www.djangoproject.com/) web framework