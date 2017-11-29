# reidi
It allows managing sub-domain requests from a previously specified root URL



# permisos en postgres para reidi_user
```bash
# up
GRANT ALL ON ALL TABLES IN SCHEMA public TO reidi_user;
# down
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM reidi_user;


#up
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO reidi_user;
#down
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM reidi_user;

```