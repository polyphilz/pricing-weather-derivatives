library(rsconnect)
library(readxl)
library(TSA)
library(tseries)
library(vars)
library(forecast)
library(shiny)

start = as.Date("2010-07-30")
startForecast = as.Date("2018-07-30")

ui <- fluidPage(
  
  titlePanel("Pricing Weather Derivatives"),
  br(),
  sidebarLayout(
    
    sidebarPanel(
      
      sliderInput("yr","Year Range:",
                  min = 2011, max = 2018,
                  value = c(start,startForecast)),
      selectInput(inputId = "type",
                  label = "Derivative Underlying:",
                  choices = c("Heating Degree Days", "Cooling Degree Days")),
      dateRangeInput('dateRange',
                     label = 'Contract Range:',
                     start = as.Date("2018-07-30"), end = as.Date("2018-08-29")),
      numericInput(inputId = "tick",
                   label = "Tick:",
                   value = 20)
    ),
    
    mainPanel(
      tabsetPanel(type = "tabs",
                  tabPanel("Historical", plotOutput("plot")),
                  tabPanel("Forecast", plotOutput("forecast")),
                  tabPanel("Price", htmlOutput("price"))
      )
    )
  )
)



data_weather <- read_excel("data_weather.xls")
inds <- seq(start, as.Date("2015-07-30"), by = "day")
dts <- ts(data_weather$mean,frequency=365,start=c(2010, as.numeric(format(inds[1], "%j"))))

#fGiven = forecast(Arima(dts,order=c(1,1,2),seasonal=list(order=c(0,1,0))),h=365) #variance=13.3
f0 = read.csv("fGiven.csv")
inds1 <- seq(startForecast, as.Date("2019-07-30"), by = "day")
frcst <- ts(f0$Point.Forecast,frequency=365,start=c(2018, as.numeric(format(inds1[1], "%j"))))

server <- function(input, output) {
  d <- reactive({
    dist <- switch(input$dist,
                   norm = rnorm,
                   unif = runif,
                   lnorm = rlnorm,
                   exp = rexp,
                   rnorm)
    dist(input$n)
  })
  
  output$plot <- renderPlot({
    plot(dts,main="Daily Mean Temps (Historical and Forecasted)",ylab="Mean Temperature (F)",xlim=c(input$yr[1],input$yr[2]))
  })
  
  output$forecast <- renderPlot({
    plot(dts,main="Daily Mean Temps (Historical and Forecasted)",ylab="Mean Temperature (F)",xlab="Year",xlim=c(input$yr[1],input$yr[2]+1))
    lines(frcst,col='blue')
 })
  
  output$price <- renderUI({
    
    n2 = input$dateRange[2] - startForecast
    n1 = input$dateRange[1] - startForecast
    hdd = 0
    cdd = 0
    val = 0
    tref = 65

    for (i in n1:n2){
      hdd = hdd + max(0, tref-frcst[i])
      cdd = cdd + max(0, frcst[i]-tref)
    }
    
    if(input$type == 'Heating Degree Days') {
      val = hdd
    }
    else {
      val = cdd
    }

    price = input$tick * val

    HTML(paste0('<br/>',h3(input$type), val, '<br/>',h3("Price"),'$',price))
    
  })
  
}

shinyApp(ui, server)
