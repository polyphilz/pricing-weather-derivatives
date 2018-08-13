library(readxl)
library(TSA)
library(tseries)
library(vars)
library(forecast)

data_weather <- read_excel("~/data_weather.xls")
plot(data_weather)

dts <- ts(data_weather$mean,frequency=365)

plot(dts)

#testing for stationarity
Box.test(dts, type = 'Ljung-Box') # p < 2.2e-16
adf.test(dts) #p < 0.01 - don't have to difference for stationarity

acf(dts) #gradual
pacf(dts) #ehhh
eacf(dts) #test: (2,2), (4,1)

m = arima(dts,order=c(1,0,4)) #l4035
m2 = arima(dts,order=c(4,0,1)) #14031
m3 = Arima(dts,order=c(2,0,2)) #14030

#attempt to difference
difDts = diff(dts)
plot(difDts)
acf(difDts)
pacf(difDts)
eacf(difDts)
McLeod.Li.test(y=difDts) #all correlated
adf.test(difDts) #significantly stationary

m1 = Arima(dts,order=c(1,1,1)) #14430
m2 = Arima(dts,order=c(1,1,2)) #14039

#pacf shows seasonal difference
m3 = Arima(dts,order=c(1,1,2),seasonal=c(0,1,0)) #14039

resid = m$residuals
resid2 = m2$residuals
resid3 = m3$residuals

acf(resid)

plot(m4$x,col="red",xlim=c(1,9),ylim=c(40,90))
lines(m4$fitted,col="blue")
plot(forecast(m3,h=20),xlim=c(8.5,9,2))
f = forecast(m3)
lines(f$Forecast)

m5 = arima(dts,order=c(1,1,2),seasonal=list(order=c(0,1,0))) #13891
f5 = forecast(m5,h=365)
p5 = predict(m4,n.ahead = 365)
fGiven = forecast(Arima(dts,order=c(1,1,2),seasonal=list(order=c(0,1,0))),h=365) #variance=13.3
temperatures = fAuto$fitted

r = 1.91
n1 = 0
n2 = 30
tref = 65
sdv = 3.6469

K = 55

hdd = 0
cdd = 0
mean = 0
sum = 0
tick = 20

for (i in n1:n2){
  hdd = hdd + max(0, tref-fGiven$fitted[i])
  cdd = cdd + max(0, fGiven$fitted[i]-tref)
}


sum = sum(fGiven$fitted[n1:n2])
mea = sum/(n2-n1)

price = tick*cdd
sdd=sd(fGiven$fitted[n1:n2])

cdfv1 = pnorm((K-mea)/sdd)
cdfv2 = pnorm(K,mean=mea,sd=sdd) #distribution of possible temperatures in range of days

#c = exp(-r*(n2-n1)*(mean-K*cdfv) + sdd/(2*pi)*exp(-()))
