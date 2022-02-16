# Base classes inheritance


## Intro

### Get user instance by request scope
> There are 3 stages to get user instance by request scope

#### Stages
1. Get token key string from the scope.
2. Parse token key from token key string.
3. Get user instance by token key.

#### Stages methods
1. "get_token_key_string(scope)" asynch method.
2. "parse_token_key(token_key_string)" method.
3. "get_user_instance(token_key)" asynch method.
