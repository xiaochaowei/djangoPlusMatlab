import matlab.engine
eng = matlab.engine.start_matlab()
filename = u'C:/Users/PTL/Desktop/project/project/mysite/mysite/statics/files/20150814163420.xlsx'
X = eng.xlsread(filename.encode('utf-8'))
E = matlab.int32([1,1,1,0,0,0,0,0,0,0])
UB = 600
LB = 200
ret = eng.Simu(X,E,LB,UB,nargout=4)

print ret[0]