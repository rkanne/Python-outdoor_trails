from django.shortcuts import render, redirect
from .models import Users, Trips, Join, State, Messages, Comments
from django.contrib import messages

import unirest 

# Create your views here.
def index(request):
	if request.method == "GET":
		trip = Trips.tripsMgr.all().order_by('trip_start')[:3]
		arr = []
		for x in trip:
  			start = x.trip_start
  			end = x.trip_end
  			days = end-start
  			arr.append(str(days))
	
		context={
		'trip':trip,
		'days': arr
		}

	return render(request, 'trails/index.html',context)

def insert(request):
	if request.method == "GET":
		return render(request, 'trails/register.html')
	if request.method == "POST":
		result = Users.registerMgr.register(request.POST['f_name'],request.POST['l_name'],request.POST['username'],request.POST['email'],request.POST['password'],request.POST['confirm_password'])
		# print "result===",result
	 	if result[0]:
	 		# print result[0], "="*20,result[1].name
	 		request.session['name'] = result[1].first_name
	 		request.session['user_id'] = result[1].id
	 		return redirect('/search')
	 	else:
	 		# print result[0], "="*20
	 		for x in xrange(len(result[1])):
	 			print x
	 			messages.error(request, result[1][x])

	 		return redirect('/insert')

def add_state(request):
	if request.method == "POST":
		# print "result===",result

	 	state = State.stateMgr.create(abbreviation=request.POST['abbreviation'],state_name=request.POST['state_name'])
	 	state.save()
	 	return redirect('/')

def login(request):
	if request.method == "GET":
		return render(request, 'trails/login.html')
	if request.method == "POST":
		result = Users.loginMgr.login(request.POST['username_login'],request.POST['password_login'])
		login = Users.loginMgr.filter(username=request.POST['username_login'])
		trips = Trips.tripsMgr.all()

		users = Users.registerMgr.all()
		if len(login)> 0:
			login = login[0].id, login[0].first_name
			request.session['user_id'] = login
		if result[0]:
	 		# print result[0], "="*20,result[1].name
	 		request.session['name'] = result[1].first_name
	 		request.session['user_id'] = result[1].id
	 		return redirect('/search')
	 	else:
	 		# print result[0], "="*20
	 		# request.session['message'] =result[1]
	 		for x in xrange(len(result[1])):
	 			# print x
	 			messages.error(request, result[1][x])
	 		return redirect('/login')

def search(request):
	if request.method == "GET":
		# print request.session.get('user_id')
		state = State.stateMgr.all()
		context={'state':state}
		
		return render(request, 'trails/trail.html', context)

	if request.method == "POST":
		name = request.POST['name']
		state = State.stateMgr.all()
		state_cont = str(request.POST.get('state'))
		request.session['state'] = state_cont
		print state_cont

		url = "https://trailapi-trailapi.p.mashape.com/?q[activities_activity_name_cont]="+name+"&q[activities_activity_type_name_eq]=hiking&q[country_cont]=United+States&q[state_cont]="+state_cont
		response = unirest.get(url , headers={"X-Mashape-Key": "4WeSG9pQNTmsh9NLmPBC6uUZkFybp1Udo57jsncHiMxxZy7lxx",
	    "Accept": "text/plain"
	  	})

		result = response.body
		result = result['places']
		for x in result:
			print x['unique_id']
			unique = x['unique_id']
			joins = Join.joinsMgr.all()
			trip = Trips.tripsMgr.all()
			print "unique=====",unique, type(unique)
			if x in trip:
				print "Trip====", x
			if len(trip)> 0 :
				unique_id = trip[0].unique_id
				print '='*50
				print len(unique_id)
				total_join = len(joins)
				print '='*50
				print total_join

				if unique == int(unique_id):
					total_join = len(joins)
					print "match"
					print unique_id, type(int(unique_id))
					print unique_id, type(unique)

				else:
					total_join = len(joins)
					print "not match"
					print unique_id, type(int(unique_id))
					print unique_id, type(unique)


		context={
		'result':result,
		'name': name,
		'state':state
		# 'total_join': total_join
		
		}
		return render(request, 'trails/trail.html', context)

def trails_detail(request, id):
	url = "https://trailapi-trailapi.p.mashape.com/?q[activities_activity_name_cont]=&q[activities_activity_type_name_eq]=hiking&q[country_cont]=United+States&q[state_cont]="+request.session['state']	
	response = unirest.get(url , headers={"X-Mashape-Key": "4WeSG9pQNTmsh9NLmPBC6uUZkFybp1Udo57jsncHiMxxZy7lxx",
    "Accept": "text/plain"
  })
	result = response.body
	result = result['places']
	trail_id = int(id)
	request.session['trail_id']= trail_id
	return redirect ('/trail_info')
# 	# print "trail_id====",trail_id
# 	request.session['trail_id']= trail_id
# 	for x in result:
# 		lat = str(x['lat'])
# 		lon = str(x['lon'])
# 		# print "=LAT=====",lat
# 		# print "=LON=====",lon
# 		# print "=unique_id=====",x['unique_id']
# 		# print "=trail_id=====",trail_id
# 		if x['unique_id'] == trail_id:
# 			# print "======LAT=====",lat
# 			# print "======LON=====",lon
# 			input_lat = lat
# 			input_lon = lon

# 	url = "https://simple-weather.p.mashape.com/weatherdata?lat="+input_lat+"&lng="+input_lon
# 	weather_response = unirest.get(url , headers={"X-Mashape-Key": "4WeSG9pQNTmsh9NLmPBC6uUZkFybp1Udo57jsncHiMxxZy7lxx",
#     "Accept": "text/plain"
#   }
# )

# 	weather = weather_response.body
# 	weather = weather['query']
# 	if weather.has_key('results'):
#   		# print weather['results']
#   		today_weather = weather['results']
#   		# print "today_weather", today_weather
#   		if today_weather == None:
#   			print 'not found'
#   			channel = ""
#   			atmosphere= ""
#   			humidity = ""
#   			visibility= ""
#   			item =""
#   			forecast=""
#   			text = ""
#   			temp =""
#   			city =""
#   		else:
#   			print  'found'
#   			if 'channel' in today_weather: 
# 	  			# print today_weather['channel']
# 	  			channel = today_weather['channel']
# 	  			if 'atmosphere' in channel and 'item' in channel and 'location' in channel and 'image' in channel :
# 	  				atmosphere = channel['atmosphere']
# 	  				item = channel['item']
# 	  				image = channel['image']
# 	  				location = channel['location']
# 	  				if 'city' in location: 
# 	  						city = location['city']
# 	  				if 'forecast' in item:
# 	  					forecast = item['forecast'] 
# 	  					for x in forecast:
# 	  						x['high']= int(x['high'])*9/5+32
# 	  						x['low']= int(x['low'])*9/5+32

# 	  				if 'condition' in item:
# 	  					condition = item['condition']
# 	  					if "text" in condition and "temp" in condition:
# 	  						text = condition['text']
# 	  						temp = condition['temp']
# 	  						temp = int(temp)*9/5+32


# 	  				if 'humidity' in atmosphere and 'visibility' in atmosphere :
# 	  					humidity = atmosphere['humidity'] 
# 	  					visibility = atmosphere['visibility']
#   			else:
#   				print 'not found'
# 	else:
# 		print 'not found'

# 	# for x in weather:
# 	# 	print x
# 	messages = Messages.messageMgr.all()
# 	comments= Comments.commentMgr.all()
# 	print "message=====" ,len(messages)
# 	print "comments=====" ,len(comments)

# 	context={
# 	'today_weather':today_weather,
# 	'result':result,
# 	'weather':weather,
# 	'trail_id': trail_id,
# 	"channel": channel,
# 	'atmosphere':atmosphere,
# 	'humidity':humidity,
# 	'visibility':visibility,
# 	'item':item,
# 	'forecast':forecast,
# 	'text':text,
# 	'temp':temp,
# 	'city': city,
# 	'messages':messages,
# 	'comments': comments
# 	}
# 	return render(request, 'trails/trail_detail.html', context)

def trail_info(request):
	url = "https://trailapi-trailapi.p.mashape.com/?q[activities_activity_name_cont]=&q[activities_activity_type_name_eq]=hiking&q[country_cont]=United+States&q[state_cont]="+request.session['state']	
	response = unirest.get(url , headers={"X-Mashape-Key": "4WeSG9pQNTmsh9NLmPBC6uUZkFybp1Udo57jsncHiMxxZy7lxx",
    "Accept": "text/plain"
  })
	result = response.body
	result = result['places']
	trail_id = request.session.get('trail_id')
	unique_trail_id = unicode(trail_id)
	print "+++++Trail_id====",trail_id
	print "+++++User_id====",request.session.get('user_id')
	print "+++++unique_trail_id====",unique_trail_id

	
	# request.session['trail_id']= trail_id
	for x in result:
		lat = str(x['lat'])
		lon = str(x['lon'])
		# print "=LAT=====",lat
		# print "=LON=====",lon
		# print "=unique_id=====",x['unique_id']
		# print "=trail_id=====",trail_id
		if x['unique_id'] == trail_id:
			# print "======LAT=====",lat
			# print "======LON=====",lon
			input_lat = lat
			input_lon = lon

	url = "https://simple-weather.p.mashape.com/weatherdata?lat="+input_lat+"&lng="+input_lon
	weather_response = unirest.get(url , headers={"X-Mashape-Key": "4WeSG9pQNTmsh9NLmPBC6uUZkFybp1Udo57jsncHiMxxZy7lxx",
    "Accept": "text/plain"
  }
)

	weather = weather_response.body
	weather = weather['query']
	if weather.has_key('results'):
  		# print weather['results']
  		today_weather = weather['results']
  		# print "today_weather", today_weather
  		if today_weather == None:
  			print 'not found'
  			channel = ""
  			atmosphere= ""
  			humidity = ""
  			visibility= ""
  			item =""
  			forecast=""
  			text = ""
  			temp =""
  			city =""
  		else:
  			print  'found'
  			if 'channel' in today_weather: 
	  			# print today_weather['channel']
	  			channel = today_weather['channel']
	  			if 'atmosphere' in channel and 'item' in channel and 'location' in channel and 'image' in channel :
	  				atmosphere = channel['atmosphere']
	  				item = channel['item']
	  				image = channel['image']
	  				location = channel['location']
	  				if 'city' in location: 
	  						city = location['city']
	  				if 'forecast' in item:
	  					forecast = item['forecast'] 
	  					for x in forecast:
	  						x['high']= int(x['high'])*9/5+32
	  						x['low']= int(x['low'])*9/5+32

	  				if 'condition' in item:
	  					condition = item['condition']
	  					if "text" in condition and "temp" in condition:
	  						text = condition['text']
	  						temp = condition['temp']
	  						temp = int(temp)*9/5+32


	  				if 'humidity' in atmosphere and 'visibility' in atmosphere :
	  					humidity = atmosphere['humidity'] 
	  					visibility = atmosphere['visibility']
  			else:
  				print 'not found'
	else:
		print 'not found'

	messages = Messages.messageMgr.all()
	comments= Comments.commentMgr.all()
	

	# print "message=====" ,len(messages)
	# print "comments=====" ,len(comments)

	context={
	'today_weather':today_weather,
	'result':result,
	'weather':weather,
	'trail_id': trail_id,
	"channel": channel,
	'atmosphere':atmosphere,
	'humidity':humidity,
	'visibility':visibility,
	'item':item,
	'forecast':forecast,
	'text':text,
	'temp':temp,
	'city': city,
	'messages':messages,
	'comments': comments,
	'unique_trail_id':unique_trail_id
	}
	return render(request, 'trails/trail_detail.html', context)

	return render('/')
	
def process(request):

	if len(request.POST['message']) < 1:
		print "Please insert your message!"
		print "trail_id==========",request.session.get('trail_id'), type(request.session.get('trail_id'))
		print "user_id==========",request.session.get('user_id'), type(request.session.get('user_id'))

		return redirect('/trail_info') 
	else:
		print "trail_id==========",request.session.get('trail_id'), type(request.session.get('trail_id'))
		print "user_id==========",request.session.get('user_id'), type(request.session.get('user_id'))
		message = Messages.messageMgr.create(user_id=request.session.get('user_id'),rating=request.POST['rating'],message=request.POST['message'],unique_trail_id=request.session.get('trail_id'))
	 	message.save()
	 	print "Save"

		print request.POST['message']
		return redirect('/trail_info') 
  
def process2(request):
	#print "COMMENT"	
	if len(request.POST['comment']) < 1:
		print "Please insert your comment!"
		return redirect('/trail_info') 
	else:
		print request.POST['comment']
		comment = Comments.commentMgr.create(user_id=request.session.get('user_id'),message_id=request.POST['message_id'],comment=request.POST['comment'])
	 	comment.save()
		return redirect('/trail_info') 


def add_trips(request, id):

	if request.method == "GET":
		request.session['unique_id'] = id 
		# print "++++++++USER_ID++++++++++",request.session.get('user_id')
		# print "++++++++unique_id++++++++++",request.session.get('unique_id')
		print request.session.get('name')
		return redirect('/insert_trips')
		
def insert_trips(request):
	if request.method == "GET":
		print request.session.get('unique_id')
		if request.session.get('user_id') == None:
			return redirect('/login')
		else:
			return render(request, 'trails/add.html')
	elif request.method == "POST":
		print "POST"
		return render(request, 'trails/add.html')
	
def create(request):
	print "Create"
	print request.session.get('unique_id')
	# print "USER_ID++++++++++",request.session.get('user_id')
	trips = Trips.tripsMgr.add(destination=request.POST['txt_destination'],description=request.POST['txt_description'],trip_start=request.POST['txt_date_from'],trip_end=request.POST['txt_date_to'])
	if trips[0]:
		trips = Trips.tripsMgr.create(destination=request.POST['txt_destination'],description=request.POST['txt_description'],user_id =request.session.get('user_id'), unique_id=request.session.get('unique_id'), trip_start=request.POST['txt_date_from'],trip_end=request.POST['txt_date_to'])
		trips.save()
		print trips.id, "="*100
		join = Join.joinsMgr.create(trip_id=trips.id, user_id=request.session.get('user_id'))
				
		return redirect('/trips')
	else:
		print "FALSE"
		for x in xrange(len(trips[1])):
			print x
			messages.error(request, trips[1][x])
		return redirect('/insert_trips')

def trips(request):
	if request.method == "GET":
		print request.session.get('name') , request.session.get('user_id') 
		if request.session.get('name') == None and request.session.get('user_id') == None:
			print "GET"
			return redirect('/login')
		else:
			trip = Trips.tripsMgr.filter(user_id=request.session.get('user_id'))
			joins = Join.joinsMgr.filter(user_id=request.session.get('user_id'))
			trips_other = Trips.tripsMgr.exclude(user_id=request.session.get('user_id'))
			for x in joins:
				trips_other = trips_other.exclude(id = x.trip.id)
				# print '='*50, request.session.get('user_id')
			context = {
			'joins': joins,
			'trip' : trip,
			'trips_other': trips_other
			}
			return render(request, 'trails/my_trips.html',context)

def join(request, id):
	if request.method == "GET":
		# print "USER_ID===========" ,request.session.get('user_id')
		trip = Trips.tripsMgr.filter(id=id)
		check_trip_id = int(id)
		# print "JOin Count ===========", Join.joinsMgr.all().count()

		if Join.joinsMgr.all().count() == 0:
			result = Join.joinsMgr.create(user_id=request.session.get('user_id'),trip_id=check_trip_id)
			result.save()
			messages.error(request, 'Congratulation!! You have joined')
			return redirect('/trips')
			# return HttpResponse("Congratulation!! You have joined")
		elif Join.joinsMgr.all().count() > 0:
			join = Join.joinsMgr.filter(trip_id=check_trip_id).filter(user_id=request.session.get('user_id'))
			# join_user = Join.joinsMgr.filter(user_id=request.session.get('user_id'))
			if len(join)> 0 :
				join = join[0].trip_id, join[0].user_id
				# print "Join trip_id ======",join[0],"Join user_id ======", join[1]
				if join[0] == check_trip_id and join[1] == request.session.get('user_id'):					
					# print "Trip_ID====",join[0], "_TRIP_ID=====", check_trip_id, "user_id=====",join[1],"user_id_form",request.session.get('user_id')
					messages.error(request, 'You already joined this trip!!')
				return redirect('/trips')
				# return HttpResponse("You already joined this trip!!")
			else: 
				result = Join.joinsMgr.create(user_id=request.session.get('user_id'),trip_id=check_trip_id)
				result.save()
				messages.error(request, 'Congratulation!! You have joined')
				return redirect('/trips')
				# return HttpResponse("Congratulation!! You have joined")
	else:
		return redirect('/')

def user_destination(request, id):
	trip = Trips.tripsMgr.filter(id=id)
	join = Join.joinsMgr.filter()
	user= Users.registerMgr.all()


	context = {
	'trip':trip,
	'join': join,
	'user':user
	}
	return render(request , 'trails/user_detail.html', context)


def logout(request):
	# Messages.messageMgr.all().delete()
	# Comments.commentMgr.all().delete()
	request.session.pop('user_id')
	request.session.pop('name')
	# Join.joinsMgr.all().delete()
	# Users.loginMgr.all().delete()
	return redirect('/')

def delete(request, id):
	#join.joinsMgr.all().delete()
	Join.joinsMgr.filter(trip_id=id).delete()
	return redirect('/trips')

def remove_join(request, trip_id, id):
	Join.joinsMgr.filter(trip_id=trip_id).filter(user_id=id).delete()
	return redirect('/trips')



