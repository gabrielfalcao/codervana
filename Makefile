deploy:
	@git push heroku master
	@heroku config:add RELEASE=`git rev-parse HEAD`
