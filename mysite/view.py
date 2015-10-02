from django.http import HttpResponse
from django.shortcuts import render_to_response
from mysite.models import Sample,Compound
import simplejson
import string 
import time
import os
import settings
def index(requtest):
	# sampleList = [1,2,3,4,5]
	sampleList = Sample.objects.values_list('name', flat=True)
	print sampleList
	return render_to_response('index.html',{'sampleList':sampleList})

	# return HttpResponse("hello world")
def createSample(request):
	print "createSample"
	name = request.POST['name']
	testSample = Sample.objects.filter(name = name)
	# if len(testSample) !=0 :
	# 	sampleList = Sample.objects.values_list('name', flat=True)
	# 	return render_to_response('index.html',{'sampleList':sampleList,'state':'failed'})
	# else:
	origin = request.POST['origin']
	industryType = request.POST['industryType']
	water = request.POST['water']
	volatiles = request.POST['volatiles']
	carbon = request.POST['carbon']
	ash = request.POST['ash']
	elementType = request.POST['elementType']
	industryElementContent = request.POST['industryElementContent']
	industryScaleContent = request.POST['industryScaleContent']
	hotType = request.POST['hotType']
	highValue = request.POST['highValue'] 
	if highValue== "":
		highValue = 0
	lowValue = request.POST['lowValue']
	if lowValue =="":
		lowValue = 0
	gravityType = request.POST['gravityType']
	reactor= request.POST['reactor']
	temperatureSpeed = request.POST['temperatureSpeed']
	gas = request.POST['gas']
	print "gas: " + gas
	fileChunk = request.FILES["gravityData"]
	STORE_PATH = settings.STATIC_PATH+ "files/"
	filename = time.strftime("%Y%m%d%H%M%S")
	filename = filename + fileChunk.name[fileChunk.name.find('.'):]
	filename = STORE_PATH + filename
	print filename
	dest = open(filename, "wb")
	for chunk in fileChunk.chunks():
		dest.write(chunk)
	dest.close()
	print "save file success"		
	gravityData = filename
	s1 = Sample(name = name, origin = origin, industryType = industryType, water = water, volatiles = volatiles, carbon = carbon,ash = ash, elementType = elementType, industryElementContent = industryElementContent, industryScaleContent = industryScaleContent, hotType = hotType, highValue = highValue, lowValue = lowValue, gravityType = gravityType, reactor = reactor, temperatureSpeed = temperatureSpeed, gas = gas, gravityData = gravityData)
	s1.save()
	print "save success"
	sampleList = Sample.objects.values_list('name', flat=True)
	print sampleList
	return render_to_response('index.html',{'sampleList':sampleList,'state':'createSample'})
		# return HttpResponse(simplejson.dumps({"state": 'success'}), mimetype='application/json')

def search(request):
	print "search.html"
	sampleList = Sample.objects.values_list('name', flat=True)
	searchValue = request.GET["searchInput"]
	searchList = Sample.objects.filter(name__contains=searchValue)
	return render_to_response('index.html',{'searchValue':searchValue,'sampleList':sampleList,'searchList':searchList,'state':'search'})

from settings import eng
import matlab
def regression(request):
	print "search.html"
	sampleList = Sample.objects.values_list('name', flat=True)
	return render_to_response('regression.html',{'sampleList':sampleList})

def SampleRegression(request):
	print "SampleRegression"
	if request.method == 'POST':
		name=request.POST['sampleName']
		EStr = request.POST['ESamples']
		E= EStr.split(',')
		LB = request.POST['LB']
		UB = request.POST['UB']
		sampleIns = Sample.objects.get(name = name)
		print sampleIns.name
		XData = sampleIns.gravityData
		print XData
		X = eng.xlsread(XData.encode('utf-8'))
		EData = []
		for i in E:
			EData.append(int(i))
		E = matlab.int32(EData)
		print E
		LB = int(LB)
		UB = int(UB)
		ret = eng.Simu(X,E,LB,UB,nargout=4)
		regSample = {}
		regSample['cof_all'] = ret[0]
		regSample['cor_all'] = round(ret[3],4)
		regSample['Xcal'] = ret[1]
		regSample['X'] = ret[2]
		regSample['name'] = name
		# print regSample['Xcal']
		newList1 = []
		newList2 = []
		newList3 = []
		drawIntern = 0
		for tmp in regSample['cof_all']:
			for tmp2 in tmp:
				drawIntern = drawIntern +1
				newList3.append(round(tmp2,4))
		regSample['cof_all'] = newList3	
		drawIntern = 0
		for tmp in regSample['Xcal']:
			for tmp2 in tmp:
				drawIntern = drawIntern +1
				if(drawIntern % 10 == 0):
					newList1.append(tmp2)
		regSample['Xcal'] = newList1
		drawIntern = 0
		for tmp in regSample['X']:
			for tmp2 in tmp:
				drawIntern = drawIntern +1
				if(drawIntern % 10 == 0):
					newList2.append(tmp2)
		regSample['X'] = newList2
		regSample['T'] = range(100,1001,10)
		# print len(regSample['Xcal'])
		# regSample ={}
		# regSample['cof_all']  = [1,1,1,1,1,1,1,1,1,1]
		# regSample['cor_all'] = 1.0
		# regSample['Xcal'] = [1,2,3,4,5,6,7,8,9]
		# regSample['X'] = [2,3,4,5,6,7,8,9,10]
		# regSample['name'] = name
		sampleList = Sample.objects.values_list('name', flat=True)
		# print sampleList
		return render_to_response('regression.html',{'sampleList':sampleList,'regSample':regSample})
	else:
		print "GET COMPOUND"
		name=request.GET['name']
		print name
		EStr = request.GET['ESamples']
		E= EStr.split(',')
		LB = request.GET['LB']
		UB = request.GET['UB']
		sampleIns = Sample.objects.get(name = name)
		print sampleIns.name
		XData = sampleIns.gravityData
		print XData
		X = eng.xlsread(XData.encode('utf-8'))
		EData = []
		for i in E:
			EData.append(int(i))
		E = matlab.int32(EData)
		print E
		LB = int(LB)
		UB = int(UB)
		ret = eng.Simu(X,E,LB,UB,nargout=4)
		print "simu success"
		regSample = {}
		regSample['cof_all'] = ret[0]
		regSample['cor_all'] = round(ret[3],4)
		t = []
		for tmp in regSample['cof_all']:
			for tmp2 in tmp:
				t.append(round(tmp2,4))
		regSample['cof_all'] = t
		regSample['name'] = name
		regSample['scale'] = request.GET['scale']
		# print regSample['Xcal']
		print "success"
		# regSample ={}
		# regSample['cof_all']  = [1,1,1,1,1,1,1,1,1,1]
		# regSample['cor_all'] = 1.0
		# regSample['Xcal'] = [1,2,3,4,5,6,7,8,9]
		# regSample['X'] = [2,3,4,5,6,7,8,9,10]
		# regSample['name'] = name
		# sampleList = Sample.objects.values_list('name', flat=True)
		# print sampleList
		return HttpResponse(simplejson.dumps({'state':'success', 'regSample':regSample}), content_type='application/json')
	
	# return render_to_response('regression.html',{'sampleList':sampleList,'state':'createSample'})
def addCompound(request):
	print "addCompound"
	name = request.POST["compoundName"]
	content = request.POST["compundContent"]
	scale = request.POST["compundScale"]
	s1 = Compound(name = name, content = content, scale = scale)
	s1.save()
	sampleList = Sample.objects.values_list('name', flat=True)
	return render_to_response('index.html',{'sampleList':sampleList,'state':'createSample'})
def getCompound(request):
	print "getCompound"
	compoundName = request.GET["compoundName"]
	compound = Compound.objects.get(name = compoundName)
	samples = compound.content.split(',')
	scales = compound.scale.split(',')
	compounds = []
	for i in range(0,len(samples)):
		sample = {}
		sample['name'] = samples[i]
		sample['scale'] = scales[i]
		compounds.append(sample)
	print compounds
	sampleList = Sample.objects.values_list('name', flat=True)
	compoundList = Compound.objects.values_list('name',flat=True)
	return render_to_response('compound.html',{'sampleList':sampleList,'compoundList':compoundList,'compound':compounds})
def compound(request):
	compoundList = Compound.objects.values_list('name',flat=True)
	sampleList = Sample.objects.values_list('name', flat=True)
	return render_to_response('compound.html',{'sampleList':sampleList,'compoundList':compoundList})
def mixCor(request):
	if request.method == 'POST':
		print "mixCor"
		re =  request.POST['re']
		cor = re.split(',')
		# print cor
		corNum = []
		for item in cor:
			corNum.append(float(item))
		corNum = matlab.double(corNum)
		print corNum
		ret = eng.Mix(corNum,nargout = 2)
		data = {}

		newList1 = []
		newList2 = []
		drawIntern = 0
		for tmp in ret[0]:
			for tmp2 in tmp:
				drawIntern = drawIntern +1
				if(drawIntern % 40 == 0):
					newList1.append(tmp2)
		drawIntern = 0
		for tmp in ret[1]:
			for tmp2 in tmp:
				drawIntern = drawIntern +1
				if(drawIntern % 40 == 0):
					newList2.append(tmp2)
		data['Xlin'] = newList1
		data['Xnon'] = newList2
		data["T"] = range(1,2500,40)
		return HttpResponse(simplejson.dumps({'state':'success','data':data}), content_type='application/json')
def removeItem(request):
	if request.method == "POST":
		print "removeITem"
		name = request.POST['name']
		print name
	 	sampleIns = Sample.objects.get(name = name)
	 	sampleIns.delete()
		# sampleList = Sample.objects.values_list('name', flat=True)
		# searchValue = request.POST["searchInput"]
		# searchList = Sample.objects.filter(name__contains=searchValue)
		# return render_to_response('index.html',{'searchValue':searchValue,'sampleList':sampleList,'searchList':searchList,'state':'search'})
		# print "xx"
		return HttpResponse(simplejson.dumps({'state':'success'}), content_type='application/json')
import xlrd
def getData(request):
	if request.method =="POST":
		print "getData"
		name = request.POST["name"]
		SampleIns = Sample.objects.get(name = name)
		print SampleIns.gravityData
		data = xlrd.open_workbook(SampleIns.gravityData)
		table = data.sheets()[0]  
		nrows = table.nrows
		ncols = table.ncols  
		result = [] 
		for i in range(0,nrows):
			tmp = []
			for j in range(0,ncols):
				tmp.append(table.cell(i,j).value)
			result.append(tmp)
		return HttpResponse(simplejson.dumps({"result":result}), content_type='application/json')
