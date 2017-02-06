# Botzilla

Botzilla is a simple Telegram bot that allows querying for Bugzilla data using simple text queries and getting a description of the bug and its corresponding link.
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
To containerize Botzilla do the following steps:

- Clone the bot: 
git pull https://github.com/pavelzag/BotZilla.git -f

- Edit the config.yml according to your Bugzilla and Telegram params
- Build the container:
docker build -t botzilla .
- Run the container:
docker run -tid botzilla

### Registration
 - It is possible to register your username that belongs to your organization to avoid using the 'user:' query.
 - For example: 'register john.doe' After registration it is possible to use the 'my' query instead of using 'user: john.doe' 

### Deregistration

- After registration, it is possible to unregister using the 'remove' query.
- For example: 'remove john.doe'. The user will need to provide the 'user' query to receive replies

### Query examples:

- user: bugzilla_user status: new
- component: Web_UI user: bugzilla_qa assigned_to: bugzilla_dev

<!--![My image](username.github.com/repository/img/image.jpg)-->
![My image](https://raw.githubusercontent.com/pavelzag/BotZilla/master/Screenshots/Screenshot1.png)
![My image](https://raw.githubusercontent.com/pavelzag/BotZilla/master/Screenshots/Screenshot2.png)
![My image](https://raw.githubusercontent.com/pavelzag/BotZilla/master/Screenshots/Screenshot3.png)


### License

Botzilla is free to use. Any feedback is welcome!
Feel free to ping me with any question or suggestion!
Pavel Zagalsky
@pavelzagalsky
