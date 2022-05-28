APPLICATION_DOMAIN=${APPLICATION_DOMAIN:-https://app.dev.dzhurybida.com}
USER_NAME=${USER_NAME:-testing1@gmail.com}
USER_PASSWORD=${USER_PASSWORD:-ohmygoodlook123}
REGISTRATION_URL=$(curl $APPLICATION_DOMAIN/api/kratos/self-service/registration/api | jq -r .ui.action)
echo $REGISTRATION_URL
curl -X POST $REGISTRATION_URL \
  -d '{"traits.email":"'$USER_NAME'","password":"'$USER_PASSWORD'", "method": "password"}' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

LOGIN_URL=$(curl $APPLICATION_DOMAIN/api/kratos/self-service/login/api | jq -r .ui.action)
echo $LOGIN_URL
curl -X POST $LOGIN_URL \
  -d '{"identifier":"'$USER_NAME'","password":"'$USER_PASSWORD'", "method": "password"}' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' | jq .session_token
