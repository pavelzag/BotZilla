# Botzilla

Botzilla is a simple Telegram bot that allows querying for Bugzilla data using simple text queries.
Currently available the following query fields:

 - user
 - assigned_to
 - status
 - component

### Dependencies:
The following are required for Botzilla:
```
$ pip install python-bugzilla
```

```
$ pip install pyyaml
```
### Config file
In order to work, Botzilla requires the following keys:

- bugzilla-creds:
    - user: '<yourbugzillauser@domain.com>'
    - password: '<yourbugzillappassword>'
    - domain: '@domain.com'
    - bugzilla-url: 'bugzilla-url.domain.com'

- telegram-creds:
    - token: '<telegramtoken>'
    
- default-params:
  - default_product: '<default_product>'
  - default_component: '<default_component>'


### Containerize Botzilla
To containerize Botzilla do te following steps:

- Clone the bot: 
git pull https://github.com/pavelzag/BotZilla.git -f

- Edit the config.yml according to your Bugzilla and Telegram params
- Build the container:
docker build -t botzilla .
- Run the container:
docker run -tid botzilla

### Query examples:

user: bugzilla_user status: new
component: Web_UI user: bugzilla_qa assigned_to: bugzilla_dev

### License

Botzilla is free to use. Any feedback is welcome!
Feel free to ping me with any question, suggestion!
Pavel Zagalsky
@pavelzagalsky
