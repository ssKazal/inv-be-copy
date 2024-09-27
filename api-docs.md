# API Documentation
```
Some Api end require authentication token in request Header
```

### Goods
```
POST /goods/ [token_required]
    > name [text]
    > standard_quantity [integer]
    > current_quantity [integer]
    > measurement_type [text]

PUT /goods/<int:goods_id>/ [token_required]
    > name [text]
    > standard_quantity [integer]
    > current_quantity [integer]
    > measurement_type [text]

GET /goods/ [token_required]

DELETE /goods/<int:goods_id>/ [token_required]


```
### Goodslogs
```
POST /goods/<int:goods_id>/goods_log/ [token_required]
	> user_email [email]


```
### User
```
POST /api/token/
    > username
    > password
    
GET /user-info-from-token/ [token_required]
GET /verify-user-permission-from-token/ [token_required]
