library(tidyverse)
library(caret)
library(readxl)
library(forcats)

setwd("/Users/miss_viktoriia/Documents/CheapTrip")
#-------------------------------------------------------------------------------
bus_valid <- read_excel("buses_valid_trips.xlsx")
bus_invalid <- read_excel("buses_invalid_trips.xlsx")
bus_min_price <- bus_valid %>%
  group_by(from_id, to_id) %>%
  summarise(price_min_EUR = min(price_min_EUR)) %>%
  ungroup()
bus_valid_min <- inner_join(bus_min_price, bus_valid,
                            by=c("from_id", "to_id", "price_min_EUR")) 

bus <- rbind(bus_valid_min, bus_invalid)
countries <- read_excel("Full_list_with_countries.xlsx", 
                        range = "A1:H775", 
                        col_names = FALSE) %>%
  rename(id_city = ...1, 
         city = ...2, 
         id_country = ...3, 
         country = ...8,
         latitude = ...4,
         longitude = ...5) %>%
  select(id_city, 
         city, 
         id_country, 
         country, 
         latitude, 
         longitude)
locations_from <- countries %>%
  rename(from_id = id_city, from_city = city,
         from_country_id = id_country, from_country = country,
         from_latitude = latitude, from_longitude = longitude)
locations_to <- countries %>%
  rename(to_id = id_city, to_city = city,
         to_country_id = id_country, to_country = country,
         to_latitude = latitude, to_longitude = longitude)
connection_from <- left_join(bus, locations_from, by = c("from_id" = "from_id"))
connection_to <- left_join(connection_from, locations_to, by = c("to_id" = "to_id"))
bus <- connection_to %>%
  select(price_min_EUR,
         duration_min,
         from_latitude,
         from_longitude,
         to_latitude,
         to_longitude,
         Predicted_Outcome)

bus <- bus %>%
  mutate(log_price = log(price_min_EUR),
         log_duration = log(duration_min)) %>%
  select(-price_min_EUR,
         -duration_min)



lat <- preProcess(bus[,c(1,3)], method = "range",
                  rangeBounds = c(0.49, 1.01))
bus[,c(1,3)] <- predict(lat, newdata = bus[,c(1,3)])
long <- preProcess(bus[,c(2,4)], method = "range",
                   rangeBounds = c(-0.15, 0.66))
bus[,c(2,4)] <- predict(long, newdata = bus[,c(2,4)])

valid <- bus %>%
  filter(Predicted_Outcome == 0) %>%
  select(-Predicted_Outcome)
invalid <- bus %>%
  filter(Predicted_Outcome == 1) %>%
  select(-Predicted_Outcome)
#-------------------------------------------------------------------------------
#Split
set.seed(147)
i <- createDataPartition(valid$log_price, p = .8, list = FALSE)
train <- valid[ i,]
test  <- valid[-i,]

scale_logs <- preProcess(train[, 6], method = c("center", "scale"))
train[,6] <- predict(scale_logs, newdata = train[,6])
test[,6] <- predict(scale_logs, newdata = test[,6])
invalid[,6] <- predict(scale_logs, newdata = invalid[,6])
#-------------------------------------------------------------------------------
train <- train %>%
  filter(log_price >= mean(log_price) - 3*sd(log_price)) %>%
  filter(log_price <= mean(log_price) + 3*sd(log_price)) %>%
  filter(log_duration >= mean(log_duration) - 3*sd(log_duration)) %>%
  filter(log_duration <= mean(log_duration) + 3*sd(log_duration))
#-------------------------------------------------------------------------------
#Modeling
model_lr <- train(log_price ~ ., 
                  data = train, 
                  method = "penalized",
                  tuneGrid = data.frame(lambda1 = 1.9,
                                        lambda2 = 1.9))
forecast::accuracy(as.vector(exp(predict(model_lr, test))), exp(test$log_price))

#Prediction
predict_invalid <- exp(predict(model_lr, invalid))
bus_invalid <- bus_invalid %>%
  mutate(predicted_price = predict_invalid)


